from pydantic import BaseModel
from typing import Optional


class CartItemAdd(BaseModel):
    product_id: str
    qty: int = 1
    size: str = ""
    color: str = ""


class CartItemUpdate(BaseModel):
    qty: int


class CartItem(BaseModel):
    product_id: str
    qty: int
    size: str = ""
    color: str = ""
    name: str = ""
    price: float = 0
    image_url: str = ""


class CartResponse(BaseModel):
    items: list[CartItem]
    total: float
    item_count: int
