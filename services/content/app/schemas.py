from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class ContentSlotResponse(BaseModel):
    id: str
    slot_key: str
    slot_type: str
    title: Optional[str] = None
    subtitle: Optional[str] = None
    body_text: Optional[str] = None
    image_url: Optional[str] = None
    link_text: Optional[str] = None
    link_action: Optional[str] = None
    badge_text: Optional[str] = None
    display_order: int = 0
    is_active: bool = True
    metadata_json: Optional[dict[str, Any]] = None
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class CreateContentSlotRequest(BaseModel):
    slot_key: str
    slot_type: str
    title: Optional[str] = None
    subtitle: Optional[str] = None
    body_text: Optional[str] = None
    image_url: Optional[str] = None
    link_text: Optional[str] = None
    link_action: Optional[str] = None
    badge_text: Optional[str] = None
    display_order: int = 0
    is_active: bool = True
    metadata_json: Optional[dict[str, Any]] = None


class UpdateContentSlotRequest(BaseModel):
    slot_key: Optional[str] = None
    slot_type: Optional[str] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    body_text: Optional[str] = None
    image_url: Optional[str] = None
    link_text: Optional[str] = None
    link_action: Optional[str] = None
    badge_text: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None
    metadata_json: Optional[dict[str, Any]] = None


class ContentSlotListResponse(BaseModel):
    slots: list[ContentSlotResponse]
    total: int


class PublicContentResponse(BaseModel):
    slots: dict[str, ContentSlotResponse]
