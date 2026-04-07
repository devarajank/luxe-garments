from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class CreatePromotionRequest(BaseModel):
    code: str
    description: str = ""
    discount_type: str  # "percentage" or "fixed"
    discount_value: float
    min_order_value: Optional[float] = None
    max_discount: Optional[float] = None
    usage_limit: Optional[int] = None
    per_user_limit: int = 1
    applicable_categories: Optional[list[str]] = None
    applicable_products: Optional[list[str]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: bool = True

    @field_validator("code", mode="before")
    @classmethod
    def uppercase_code(cls, v):
        return v.strip().upper() if v else v

    @field_validator("discount_type")
    @classmethod
    def validate_discount_type(cls, v):
        if v not in ("percentage", "fixed"):
            raise ValueError("discount_type must be 'percentage' or 'fixed'")
        return v


class UpdatePromotionRequest(BaseModel):
    description: Optional[str] = None
    discount_type: Optional[str] = None
    discount_value: Optional[float] = None
    min_order_value: Optional[float] = None
    max_discount: Optional[float] = None
    usage_limit: Optional[int] = None
    per_user_limit: Optional[int] = None
    applicable_categories: Optional[list[str]] = None
    applicable_products: Optional[list[str]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None

    @field_validator("discount_type")
    @classmethod
    def validate_discount_type(cls, v):
        if v is not None and v not in ("percentage", "fixed"):
            raise ValueError("discount_type must be 'percentage' or 'fixed'")
        return v


class CartItem(BaseModel):
    product_id: str
    category: Optional[str] = None
    quantity: int = 1
    price: float = 0


class ValidateRequest(BaseModel):
    code: str
    cart_total: float
    user_id: Optional[str] = None
    cart_items: list[CartItem] = []

    @field_validator("code", mode="before")
    @classmethod
    def uppercase_code(cls, v):
        return v.strip().upper() if v else v


class ApplyRequest(BaseModel):
    code: str
    cart_total: float
    user_id: str
    order_id: Optional[str] = None
    cart_items: list[CartItem] = []

    @field_validator("code", mode="before")
    @classmethod
    def uppercase_code(cls, v):
        return v.strip().upper() if v else v


class PromotionResponse(BaseModel):
    id: str
    code: str
    description: str
    discount_type: str
    discount_value: float
    min_order_value: Optional[float] = None
    max_discount: Optional[float] = None
    usage_limit: Optional[int] = None
    used_count: int = 0
    per_user_limit: int = 1
    applicable_categories: Optional[list[str]] = None
    applicable_products: Optional[list[str]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: bool = True
    created_at: datetime

    model_config = {"from_attributes": True}


class PromotionListResponse(BaseModel):
    promotions: list[PromotionResponse]
    total: int


class ValidateResponse(BaseModel):
    valid: bool
    code: str
    discount_amount: float = 0
    discount_type: str = ""
    discount_value: float = 0
    description: str = ""
    message: str = ""
