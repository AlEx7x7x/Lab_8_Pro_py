from sqlalchemy import select
from sqlalchemy.orm import Session
from store_manager.models import Product, Category

class CategoryRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, name: str) -> Category:
        category = Category(name=name)
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category

    def get_by_name(self, name: str) -> Category | None:
        return self.session.scalar(select(Category).where(Category.name == name))

class ProductRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, product: Product) -> Product:
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def get_by_id(self, product_id: int) -> Product | None:
        return self.session.get(Product, product_id)

    def get_all(self) -> list[Product]:
        return list(self.session.scalars(select(Product)))

    def update_price(self, product_id: int, price: float) -> Product | None:
        product = self.get_by_id(product_id)
        if product:
            product.price = price
            self.session.commit()
            self.session.refresh(product)
        return product

    def update_quantity(self, product_id: int, quantity: int) -> Product | None:
        product = self.get_by_id(product_id)
        if product:
            product.quantity = quantity
            self.session.commit()
            self.session.refresh(product)
        return product

    def delete(self, product_id: int) -> bool:
        product = self.get_by_id(product_id)
        if product:
            self.session.delete(product)
            self.session.commit()
            return True
        return False