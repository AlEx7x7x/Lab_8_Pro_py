from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Generator
from store_manager.database import SessionLocal
from store_manager.models import Product
from store_manager.repositories import ProductRepository
from store_manager.services import StoreService
from store_manager.schemas import ProductCreate, ProductUpdate, ProductResponse, PurchaseRequest

app = FastAPI(title="Store Manager API", version="1.0.0")

def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.get("/products", response_model=list[ProductResponse])
async def get_products(session: Session = Depends(get_session)):
    return ProductRepository(session).get_all()

@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, session: Session = Depends(get_session)):
    product = ProductRepository(session).get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(data: ProductCreate, session: Session = Depends(get_session)):
    repo = ProductRepository(session)
    product = Product(
        name=data.name, price=data.price, quantity=data.quantity, 
        description=data.description, category_id=data.category_id
    )
    return repo.add(product)

@app.patch("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, data: ProductUpdate, session: Session = Depends(get_session)):
    repo = ProductRepository(session)
    product = repo.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(product, field, value)
    session.commit()
    session.refresh(product)
    return product

@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, session: Session = Depends(get_session)):
    repo = ProductRepository(session)
    if not repo.delete(product_id):
        raise HTTPException(status_code=404, detail="Product not found")

@app.post("/products/{product_id}/purchase", status_code=status.HTTP_200_OK)
async def purchase_product(product_id: int, request: PurchaseRequest, session: Session = Depends(get_session)):
    service = StoreService(session)
    try:
        service.purchase_product(product_id, request.amount)
        return {"message": "Purchase successful"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))