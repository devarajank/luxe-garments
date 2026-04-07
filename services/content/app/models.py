import uuid
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Boolean, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class ContentSlot(Base):
    __tablename__ = "content_slots"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    slot_key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    slot_type: Mapped[str] = mapped_column(String(30), nullable=False)  # hero, banner, category_tile, collection_card, text, promo_bar
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    subtitle: Mapped[str] = mapped_column(String(500), nullable=True)
    body_text: Mapped[str] = mapped_column(Text, nullable=True)
    image_url: Mapped[str] = mapped_column(Text, nullable=True)
    link_text: Mapped[str] = mapped_column(String(100), nullable=True)
    link_action: Mapped[str] = mapped_column(String(255), nullable=True)
    badge_text: Mapped[str] = mapped_column(String(50), nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
