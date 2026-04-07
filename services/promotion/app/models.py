import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Promotion(Base):
    __tablename__ = "promotions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    discount_type: Mapped[str] = mapped_column(String(20), nullable=False)  # "percentage" or "fixed"
    discount_value: Mapped[float] = mapped_column(Float, nullable=False)
    min_order_value: Mapped[float] = mapped_column(Float, nullable=True)
    max_discount: Mapped[float] = mapped_column(Float, nullable=True)
    usage_limit: Mapped[int] = mapped_column(Integer, nullable=True)  # null = unlimited
    used_count: Mapped[int] = mapped_column(Integer, default=0)
    per_user_limit: Mapped[int] = mapped_column(Integer, default=1)
    applicable_categories: Mapped[dict] = mapped_column(JSON, nullable=True)  # list of category slugs
    applicable_products: Mapped[dict] = mapped_column(JSON, nullable=True)  # list of product IDs
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    usages: Mapped[list["PromotionUsage"]] = relationship(back_populates="promotion", cascade="all, delete-orphan")


class PromotionUsage(Base):
    __tablename__ = "promotion_usages"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    promotion_id: Mapped[str] = mapped_column(String(36), ForeignKey("promotions.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    order_id: Mapped[str] = mapped_column(String(36), nullable=True)
    used_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    promotion: Mapped["Promotion"] = relationship(back_populates="usages")
