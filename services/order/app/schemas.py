from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ShippingAddress(BaseModel):
    line1: str
    line2: str = ""
    city: str
    state: str
    zip_code: str
    country: str = "US"


class CreateOrderRequest(BaseModel):
    shipping_address: ShippingAddress
    promotion_code: Optional[str] = None


class OrderItemResponse(BaseModel):
    product_id: str
    product_name: str
    product_image: str
    price: float
    size: str
    color: str
    quantity: int

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: str
    status: str
    total: float
    promotion_code: Optional[str] = None
    discount_amount: float = 0
    shipping_address: Optional[dict] = None
    items: list[OrderItemResponse] = []
    created_at: datetime

    model_config = {"from_attributes": True}


class OrderListResponse(BaseModel):
    orders: list[OrderResponse]
    total: int


class UpdateStatusRequest(BaseModel):
    status: str


class AdminOrderResponse(BaseModel):
    id: str
    user_id: str
    status: str
    total: float
    promotion_code: Optional[str] = None
    discount_amount: float = 0
    shipping_address: Optional[dict] = None
    items: list[OrderItemResponse] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class AdminOrderListResponse(BaseModel):
    orders: list[AdminOrderResponse]
    total: int
