from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from datetime import datetime
from app.database import get_db
from app.models import Promotion, PromotionUsage
from app.schemas import (
    CreatePromotionRequest, UpdatePromotionRequest,
    ValidateRequest, ApplyRequest,
    PromotionResponse, PromotionListResponse, ValidateResponse,
)

router = APIRouter(prefix="/api/promotions", tags=["promotions"])


def promotion_to_response(p: Promotion) -> PromotionResponse:
    return PromotionResponse(
        id=p.id,
        code=p.code,
        description=p.description,
        discount_type=p.discount_type,
        discount_value=float(p.discount_value),
        min_order_value=float(p.min_order_value) if p.min_order_value is not None else None,
        max_discount=float(p.max_discount) if p.max_discount is not None else None,
        usage_limit=p.usage_limit,
        used_count=p.used_count,
        per_user_limit=p.per_user_limit,
        applicable_categories=p.applicable_categories,
        applicable_products=p.applicable_products,
        start_date=p.start_date,
        end_date=p.end_date,
        is_active=p.is_active,
        created_at=p.created_at,
    )


@router.post("/", response_model=PromotionResponse)
async def create_promotion(
    req: CreatePromotionRequest,
    x_user_role: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    # Check for duplicate code
    existing = await db.execute(select(Promotion).where(Promotion.code == req.code))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail=f"Promotion code '{req.code}' already exists")

    promotion = Promotion(
        code=req.code,
        description=req.description,
        discount_type=req.discount_type,
        discount_value=req.discount_value,
        min_order_value=req.min_order_value,
        max_discount=req.max_discount,
        usage_limit=req.usage_limit,
        per_user_limit=req.per_user_limit,
        applicable_categories=req.applicable_categories,
        applicable_products=req.applicable_products,
        start_date=req.start_date,
        end_date=req.end_date,
        is_active=req.is_active,
    )
    db.add(promotion)
    await db.commit()
    await db.refresh(promotion)
    return promotion_to_response(promotion)


@router.get("/", response_model=PromotionListResponse)
async def list_promotions(
    x_user_role: Optional[str] = Header(None),
    status: Optional[str] = Query(None, description="Filter: active, expired, all"),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    query = select(Promotion)
    count_query = select(func.count(Promotion.id))
    now = datetime.utcnow()

    if status == "active":
        query = query.where(Promotion.is_active == True, Promotion.end_date > now)
        count_query = count_query.where(Promotion.is_active == True, Promotion.end_date > now)
    elif status == "expired":
        from sqlalchemy import or_
        query = query.where(or_(Promotion.is_active == False, Promotion.end_date <= now))
        count_query = count_query.where(or_(Promotion.is_active == False, Promotion.end_date <= now))

    count_result = await db.execute(count_query)
    total = count_result.scalar()

    result = await db.execute(
        query.order_by(Promotion.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )
    promotions = result.scalars().all()

    return PromotionListResponse(
        promotions=[promotion_to_response(p) for p in promotions],
        total=total,
    )


@router.get("/{promotion_id}", response_model=PromotionResponse)
async def get_promotion(
    promotion_id: str,
    x_user_role: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    result = await db.execute(select(Promotion).where(Promotion.id == promotion_id))
    promotion = result.scalar_one_or_none()
    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return promotion_to_response(promotion)


@router.put("/{promotion_id}", response_model=PromotionResponse)
async def update_promotion(
    promotion_id: str,
    req: UpdatePromotionRequest,
    x_user_role: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    result = await db.execute(select(Promotion).where(Promotion.id == promotion_id))
    promotion = result.scalar_one_or_none()
    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")

    update_data = req.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(promotion, field, value)

    await db.commit()
    await db.refresh(promotion)
    return promotion_to_response(promotion)


@router.delete("/{promotion_id}", response_model=PromotionResponse)
async def deactivate_promotion(
    promotion_id: str,
    x_user_role: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    result = await db.execute(select(Promotion).where(Promotion.id == promotion_id))
    promotion = result.scalar_one_or_none()
    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")

    promotion.is_active = False
    await db.commit()
    await db.refresh(promotion)
    return promotion_to_response(promotion)


async def _validate_promotion(code: str, cart_total: float, user_id: str, cart_items: list, db: AsyncSession) -> tuple:
    """Validate a promotion code. Returns (promotion, discount_amount, message) or raises HTTPException."""
    result = await db.execute(select(Promotion).where(Promotion.code == code))
    promotion = result.scalar_one_or_none()

    if not promotion:
        return None, 0, "Invalid coupon code"

    if not promotion.is_active:
        return None, 0, "This coupon is no longer active"

    now = datetime.utcnow()
    if promotion.start_date and now < promotion.start_date:
        return None, 0, "This coupon is not yet valid"
    if promotion.end_date and now > promotion.end_date:
        return None, 0, "This coupon has expired"

    # Check usage limit
    if promotion.usage_limit is not None and promotion.used_count >= promotion.usage_limit:
        return None, 0, "This coupon has reached its maximum usage limit"

    # Check per-user limit
    if user_id:
        user_usage_result = await db.execute(
            select(func.count(PromotionUsage.id)).where(
                PromotionUsage.promotion_id == promotion.id,
                PromotionUsage.user_id == user_id,
            )
        )
        user_usage_count = user_usage_result.scalar()
        if user_usage_count >= promotion.per_user_limit:
            return None, 0, "You have already used this coupon"

    # Check min order value
    if promotion.min_order_value is not None and cart_total < promotion.min_order_value:
        return None, 0, f"Minimum order value of ${promotion.min_order_value:.2f} required"

    # Calculate discount
    discount_amount = 0.0

    if promotion.applicable_categories or promotion.applicable_products:
        # Apply discount only to eligible items
        eligible_total = 0.0
        categories = promotion.applicable_categories or []
        products = promotion.applicable_products or []

        for item in cart_items:
            is_eligible = False
            if categories and item.category and item.category in categories:
                is_eligible = True
            if products and item.product_id in products:
                is_eligible = True
            if not categories and not products:
                is_eligible = True
            if is_eligible:
                eligible_total += item.price * item.quantity

        if eligible_total == 0:
            return None, 0, "No eligible items in your cart for this coupon"

        if promotion.discount_type == "percentage":
            discount_amount = eligible_total * (promotion.discount_value / 100.0)
        else:
            discount_amount = min(promotion.discount_value, eligible_total)
    else:
        # Apply to entire cart
        if promotion.discount_type == "percentage":
            discount_amount = cart_total * (promotion.discount_value / 100.0)
        else:
            discount_amount = min(promotion.discount_value, cart_total)

    # Apply max discount cap for percentage discounts
    if promotion.discount_type == "percentage" and promotion.max_discount is not None:
        discount_amount = min(discount_amount, promotion.max_discount)

    discount_amount = round(discount_amount, 2)
    return promotion, discount_amount, "Coupon applied successfully"


@router.post("/validate", response_model=ValidateResponse)
async def validate_promotion(
    req: ValidateRequest,
    db: AsyncSession = Depends(get_db),
):
    promotion, discount_amount, message = await _validate_promotion(
        req.code, req.cart_total, req.user_id, req.cart_items, db
    )

    if not promotion:
        return ValidateResponse(
            valid=False,
            code=req.code,
            discount_amount=0,
            message=message,
        )

    return ValidateResponse(
        valid=True,
        code=promotion.code,
        discount_amount=discount_amount,
        discount_type=promotion.discount_type,
        discount_value=float(promotion.discount_value),
        description=promotion.description,
        message=message,
    )


@router.post("/apply", response_model=ValidateResponse)
async def apply_promotion(
    req: ApplyRequest,
    x_user_id: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    user_id = req.user_id or x_user_id
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    promotion, discount_amount, message = await _validate_promotion(
        req.code, req.cart_total, user_id, req.cart_items, db
    )

    if not promotion:
        return ValidateResponse(
            valid=False,
            code=req.code,
            discount_amount=0,
            message=message,
        )

    # Increment used_count and create usage record
    promotion.used_count += 1
    usage = PromotionUsage(
        promotion_id=promotion.id,
        user_id=user_id,
        order_id=req.order_id,
    )
    db.add(usage)
    await db.commit()

    return ValidateResponse(
        valid=True,
        code=promotion.code,
        discount_amount=discount_amount,
        discount_type=promotion.discount_type,
        discount_value=float(promotion.discount_value),
        description=promotion.description,
        message="Coupon applied successfully",
    )
