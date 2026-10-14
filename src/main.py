from store_manager.database import SessionLocal, engine
from store_manager.models import Base, Product
from store_manager.repositories import CategoryRepository, ProductRepository
from store_manager.services import StoreService, find_products_by_category_dbapi

def main():
    Base.metadata.create_all(engine)
    with SessionLocal() as session:
        cat_repo = CategoryRepository(session)
        prod_repo = ProductRepository(session)
        service = StoreService(session)

        # Створення категорії
        cat = cat_repo.get_by_name("Laptops")
        if not cat:
            cat = cat_repo.add("Laptops")
        
        # Додавання товару
        prod_repo.add(Product(name="MacBook Air", price=999.99, quantity=5, category_id=cat.id))
        
        print("Загальна вартість залишків:", service.get_stock_value())
        
        # Транзакція покупки
        print("\nКупуємо 1 MacBook Air...")
        macbook = prod_repo.get_all()[0]
        service.purchase_product(macbook.id, 1)
        
        print("Оновлена кількість на складі:", prod_repo.get_by_id(macbook.id).quantity)
        
        # Виклик чистого DB-API запиту
        print("\nПошук через DB-API (Laptops):")
        print(find_products_by_category_dbapi("store.db", "Laptops"))

if __name__ == "__main__":
    main()