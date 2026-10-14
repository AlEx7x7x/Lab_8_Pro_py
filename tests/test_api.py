from fastapi.testclient import TestClient
from store_manager.api import app

client = TestClient(app)

def test_get_products():
    response = client.get("/products")
    assert response.status_code == 200

def test_create_product_validation():
    # Відправка некоректних даних для перевірки валідації Pydantic
    response = client.post("/products", json={
        "name": "T", # Занадто коротке (min_length=2)
        "price": -10, # Негативна ціна (gt=0)
        "quantity": 5,
        "category_id": 1
    })
    assert response.status_code == 422 # 422 Unprocessable Entity