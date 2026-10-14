import sqlite3
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from store_manager.models import Product

class StoreService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_stock_value(self) -> float:
        result = self.session.scalar(select(func.sum(Product.price * Product.quantity)))
        return float(result) if result else 0.0

    def get_most_expensive(self) -> Product | None:
        return self.session.scalar(select(Product).order_by(Product.price.desc()).limit(1))

    def purchase_product(self, product_id: int, amount: int) -> None:
        try:
            product = self.session.get(Product, product_id)
            if not product:
                raise ValueError("Товар не знайдено")
            if product.quantity < amount:
                raise ValueError("Недостатня кількість на складі")
            
            product.quantity -= amount
            self.session.commit()
        except Exception:
            self.session.rollback() # Відкіт транзакції у разі помилки (ACID)
            raise

# DB-API параметризований запит (без ORM)
def find_products_by_category_dbapi(db_path: str, category_name: str) -> list[tuple]:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT p.name, p.price, p.quantity 
            FROM products p
            JOIN categories c ON p.category_id = c.id
            WHERE c.name = ?
            """,
            (category_name,)
        )
        return cursor.fetchall()