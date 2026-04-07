import httpx
from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from app.database import get_db
from app.models import Order, OrderItem
from app.schemas import CreateOrderRequest, OrderResponse, OrderItemResponse, OrderListResponse, UpdateStatusRequest, AdminOrderResponse, AdminOrderListResponse
from app.config import CART_SERVICE_URL, PROMOTION_SERVICE_URL

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse)
async def create_order(
    req: CreateOrderRequest,
    x_user_id: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    # Fetch cart from Cart Service
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                f"{CART_SERVICE_URL}/api/cart/",
                headers={"x-user-id": x_user_id},
                timeout=10,
            )
            if resp.status_code != 200:
                raise HTTPException(status_code=400, detail="Could not fetch cart")
            cart = resp.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Cart service unavailable")

    if not cart.get("items"):
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Apply promotion if provided
    total = cart["total"]
    discount_amount = 0.0
    promotion_code = None

    if req.promotion_code:
        cart_items_for_promo = [
            {"product_id": item["product_id"], "category": item.get("category", ""), "quantity": item.get("qty", 1), "price": item.get("price", 0)}
            for item in cart["items"]
        ]
        async with httpx.AsyncClient() as client:
            try:
                promo_resp = await client.post(
                    f"{PROMOTION_SERVICE_URL}/api/promotions/apply",
                    json={"code": req.promotion_code, "cart_total": total, "user_id": x_user_id, "cart_items": cart_items_for_promo},
                    headers={"x-user-id": x_user_id},
                    timeout=10,
                )
                if promo_resp.status_code == 200:
                    promo_data = promo_resp.json()
                    if promo_data.get("valid"):
                        discount_amount = promo_data["discount_amount"]
                        promotion_code = req.promotion_code.upper()
                        total = total - discount_amount
            except httpx.RequestError:
                pass  # Proceed without discount if promo service is down

    # Create order
    order = Order(
        user_id=x_user_id,
        total=total,
        shipping_address=req.shipping_address.model_dump(),
        promotion_code=promotion_code,
        discount_amount=discount_amount,
        status="confirmed",
    )
    db.add(order)
    await db.flush()

    # Create order items from cart
    for item in cart["items"]:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item["product_id"],
            product_name=item.get("name", ""),
            product_image=item.get("image_url", ""),
            price=item.get("price", 0),
            size=item.get("size", ""),
            color=item.get("color", ""),
            quantity=item.get("qty", 1),
        )
        db.add(order_item)

    await db.commit()
    await db.refresh(order, ["items"])

    # Clear the cart
    async with httpx.AsyncClient() as client:
        try:
            await client.delete(
                f"{CART_SERVICE_URL}/api/cart/",
                headers={"x-user-id": x_user_id},
                timeout=5,
            )
        except httpx.RequestError:
            pass  # Non-critical if cart clear fails

    return order_to_response(order)


@router.get("/", response_model=OrderListResponse)
async def list_orders(
    x_user_id: Optional[str] = Header(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    count_result = await db.execute(
        select(func.count(Order.id)).where(Order.user_id == x_user_id)
    )
    total = count_result.scalar()

    result = await db.execute(
        select(Order)
        .where(Order.user_id == x_user_id)
        .order_by(Order.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )
    orders = result.scalars().all()

    items = []
    for o in orders:
        await db.refresh(o, ["items"])
        items.append(order_to_response(o))

    return OrderListResponse(orders=items, total=total)


@router.get("/admin/all", response_model=AdminOrderListResponse)
async def list_all_orders(
    x_user_role: Optional[str] = Header(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    query = select(Order)
    count_query = select(func.count(Order.id))

    if status:
        query = query.where(Order.status == status)
        count_query = count_query.where(Order.status == status)

    count_result = await db.execute(count_query)
    total = count_result.scalar()

    result = await db.execute(
        query.order_by(Order.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )
    orders = result.scalars().all()

    items = []
    for o in orders:
        await db.refresh(o, ["items"])
        items.append(admin_order_to_response(o))

    return AdminOrderListResponse(orders=items, total=total)


@router.put("/{order_id}/status", response_model=AdminOrderResponse)
async def update_order_status(
    order_id: str,
    req: UpdateStatusRequest,
    x_user_role: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    valid_statuses = ["pending", "confirmed", "shipped", "delivered", "cancelled"]
    if req.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}")

    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = req.status
    await db.commit()
    await db.refresh(order, ["items"])
    return admin_order_to_response(order)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    x_user_id: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    result = await db.execute(
        select(Order).where(Order.id == order_id, Order.user_id == x_user_id)
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    await db.refresh(order, ["items"])
    return order_to_response(order)


@router.put("/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(
    order_id: str,
    x_user_id: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    result = await db.execute(
        select(Order).where(Order.id == order_id, Order.user_id == x_user_id)
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != "pending" and order.status != "confirmed":
        raise HTTPException(status_code=400, detail=f"Cannot cancel order with status '{order.status}'")

    order.status = "cancelled"
    await db.commit()
    await db.refresh(order, ["items"])
    return order_to_response(order)


def admin_order_to_response(order: Order) -> AdminOrderResponse:
    return AdminOrderResponse(
        id=order.id,
        user_id=order.user_id,
        status=order.status,
        total=float(order.total),
        promotion_code=order.promotion_code,
        discount_amount=float(order.discount_amount) if order.discount_amount else 0,
        shipping_address=order.shipping_address,
        items=[
            OrderItemResponse(
                product_id=i.product_id,
                product_name=i.product_name,
                product_image=i.product_image,
                price=float(i.price),
                size=i.size,
                color=i.color,
                quantity=i.quantity,
            )
            for i in order.items
        ],
        created_at=order.created_at,
        updated_at=order.updated_at,
    )


def order_to_response(order: Order) -> OrderResponse:
    return OrderResponse(
        id=order.id,
        status=order.status,
        total=float(order.total),
        promotion_code=order.promotion_code,
        discount_amount=float(order.discount_amount) if order.discount_amount else 0,
        shipping_address=order.shipping_address,
        items=[
            OrderItemResponse(
                product_id=i.product_id,
                product_name=i.product_name,
                product_image=i.product_image,
                price=float(i.price),
                size=i.size,
                color=i.color,
                quantity=i.quantity,
            )
            for i in order.items
        ],
        created_at=order.created_at,
    )
