from pydantic import BaseModel, EmailStr
from typing import Optional


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str = ""
    last_name: str = ""


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    phone: str
    role: str

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class ProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


class AddressCreate(BaseModel):
    label: str = "home"
    line1: str
    line2: str = ""
    city: str
    state: str
    zip_code: str
    country: str = "US"
    is_default: bool = False


class AddressResponse(BaseModel):
    id: str
    label: str
    line1: str
    line2: str
    city: str
    state: str
    zip_code: str
    country: str
    is_default: bool

    model_config = {"from_attributes": True}
