import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from store_manager.models import Base, Product
from store_manager.repositories import CategoryRepository, ProductRepository
from store_manager.services import StoreService

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine, expire_on_commit=False)
    with TestSession() as session:
        yield session
    Base.metadata.drop_all(engine)

def test_add_product(session):
    cat_repo = CategoryRepository(session)
    prod_repo = ProductRepository(session)
    
    cat = cat_repo.add("Smartphones")
    product = Product(name="iPhone 15", price=1000.0, quantity=10, category_id=cat.id)
    saved = prod_repo.add(product)
    
    assert saved.id is not None
    assert saved.name == "iPhone 15"

def test_purchase_rollback(session):
    cat_repo = CategoryRepository(session)
    prod_repo = ProductRepository(session)
    service = StoreService(session)
    
    cat = cat_repo.add("Smartphones")
    product = prod_repo.add(Product(name="iPhone 15", price=1000.0, quantity=2, category_id=cat.id))
    
    # Спроба купити більше, ніж є на складі
    with pytest.raises(ValueError):
        service.purchase_product(product.id, 5)
        
    session.refresh(product)
    # Перевіряємо, що rollback спрацював і кількість не змінилася
    assert product.quantity == 2