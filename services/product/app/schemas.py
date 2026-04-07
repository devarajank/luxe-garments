from pydantic import BaseModel
from typing import Optional


class ProductResponse(BaseModel):
    id: str
    name: str
    subtitle: str
    price: float
    original_price: Optional[float] = None
    image_url: str
    colors: list
    sizes: list
    badge: Optional[str] = None
    details: list
    category: str = ""
    subcategory: str = ""

    model_config = {"from_attributes": True}


class SubcategoryResponse(BaseModel):
    slug: str
    display_name: str
    product_count: int = 0

    model_config = {"from_attributes": True}


class CategoryResponse(BaseModel):
    slug: str
    name: str
    subcategories: list[SubcategoryResponse] = []

    model_config = {"from_attributes": True}


class ProductListResponse(BaseModel):
    products: list[ProductResponse]
    total: int
    page: int
    limit: int


class ProductCreate(BaseModel):
    id: str
    name: str
    subtitle: str = ""
    price: float
    original_price: Optional[float] = None
    image_url: str = ""
    colors: list = []
    sizes: list = []
    badge: Optional[str] = None
    details: list = []
    category: str
    subcategory: str


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    subtitle: Optional[str] = None
    price: Optional[float] = None
    original_price: Optional[float] = None
    image_url: Optional[str] = None
    colors: Optional[list] = None
    sizes: Optional[list] = None
    badge: Optional[str] = None
    details: Optional[list] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    is_active: Optional[bool] = None
