from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)
    description: str | None = None
    category_id: int = Field(gt=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    price: float | None = Field(default=None, gt=0)
    quantity: int | None = Field(default=None, ge=0)
    description: str | None = None
    category_id: int | None = Field(default=None, gt=0)

class ProductResponse(ProductBase):
    id: int
    model_config = {"from_attributes": True}

class PurchaseRequest(BaseModel):
    amount: int = Field(gt=0)