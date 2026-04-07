import json
import httpx
from fastapi import APIRouter, Depends, HTTPException, Header
from redis.asyncio import Redis
from typing import Optional
from app.redis_client import get_redis
from app.schemas import CartItemAdd, CartItemUpdate, CartItem, CartResponse
from app.config import PRODUCT_SERVICE_URL

router = APIRouter(prefix="/api/cart", tags=["cart"])


def get_cart_key(user_id: Optional[str] = None, session_id: Optional[str] = None) -> str:
    if user_id:
        return f"cart:{user_id}"
    if session_id:
        return f"cart:guest:{session_id}"
    raise HTTPException(status_code=400, detail="No user_id or session_id")


async def fetch_product(product_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{PRODUCT_SERVICE_URL}/api/products/{product_id}", timeout=5)
            if resp.status_code == 200:
                return resp.json()
        except httpx.RequestError:
            pass
    return {}


@router.get("/", response_model=CartResponse)
async def get_cart(
    x_user_id: Optional[str] = Header(None),
    x_session_id: Optional[str] = Header(None),
    r: Redis = Depends(get_redis),
):
    key = get_cart_key(x_user_id, x_session_id)
    cart_data = await r.hgetall(key)

    items = []
    total = 0.0
    for product_id, item_json in cart_data.items():
        item_data = json.loads(item_json)
        product = await fetch_product(product_id)
        price = product.get("price", 0)
        cart_item = CartItem(
            product_id=product_id,
            qty=item_data["qty"],
            size=item_data.get("size", ""),
            color=item_data.get("color", ""),
            name=product.get("name", ""),
            price=price,
            image_url=product.get("image_url", ""),
        )
        items.append(cart_item)
        total += price * item_data["qty"]

    return CartResponse(items=items, total=round(total, 2), item_count=len(items))


@router.post("/items", response_model=CartItem)
async def add_item(
    item: CartItemAdd,
    x_user_id: Optional[str] = Header(None),
    x_session_id: Optional[str] = Header(None),
    r: Redis = Depends(get_redis),
):
    key = get_cart_key(x_user_id, x_session_id)

    # Validate product exists
    product = await fetch_product(item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if item already in cart
    existing = await r.hget(key, item.product_id)
    if existing:
        data = json.loads(existing)
        data["qty"] += item.qty
    else:
        data = {"qty": item.qty, "size": item.size, "color": item.color}

    await r.hset(key, item.product_id, json.dumps(data))
    await r.expire(key, 60 * 60 * 24 * 30)  # 30 days TTL

    return CartItem(
        product_id=item.product_id,
        qty=data["qty"],
        size=data.get("size", ""),
        color=data.get("color", ""),
        name=product.get("name", ""),
        price=product.get("price", 0),
        image_url=product.get("image_url", ""),
    )


@router.put("/items/{product_id}", response_model=CartItem)
async def update_item(
    product_id: str,
    update: CartItemUpdate,
    x_user_id: Optional[str] = Header(None),
    x_session_id: Optional[str] = Header(None),
    r: Redis = Depends(get_redis),
):
    key = get_cart_key(x_user_id, x_session_id)
    existing = await r.hget(key, product_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Item not in cart")

    if update.qty <= 0:
        await r.hdel(key, product_id)
        return CartItem(product_id=product_id, qty=0)

    data = json.loads(existing)
    data["qty"] = update.qty
    await r.hset(key, product_id, json.dumps(data))

    product = await fetch_product(product_id)
    return CartItem(
        product_id=product_id,
        qty=data["qty"],
        size=data.get("size", ""),
        color=data.get("color", ""),
        name=product.get("name", ""),
        price=product.get("price", 0),
        image_url=product.get("image_url", ""),
    )


@router.delete("/items/{product_id}")
async def remove_item(
    product_id: str,
    x_user_id: Optional[str] = Header(None),
    x_session_id: Optional[str] = Header(None),
    r: Redis = Depends(get_redis),
):
    key = get_cart_key(x_user_id, x_session_id)
    removed = await r.hdel(key, product_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Item not in cart")
    return {"status": "removed"}


@router.delete("/")
async def clear_cart(
    x_user_id: Optional[str] = Header(None),
    x_session_id: Optional[str] = Header(None),
    r: Redis = Depends(get_redis),
):
    key = get_cart_key(x_user_id, x_session_id)
    await r.delete(key)
    return {"status": "cleared"}


@router.post("/merge")
async def merge_cart(
    x_user_id: Optional[str] = Header(None),
    x_session_id: Optional[str] = Header(None),
    r: Redis = Depends(get_redis),
):
    """Merge guest cart into user cart after login."""
    if not x_user_id or not x_session_id:
        raise HTTPException(status_code=400, detail="Need both user_id and session_id")

    guest_key = f"cart:guest:{x_session_id}"
    user_key = f"cart:{x_user_id}"

    guest_items = await r.hgetall(guest_key)
    for product_id, item_json in guest_items.items():
        existing = await r.hget(user_key, product_id)
        if existing:
            user_data = json.loads(existing)
            guest_data = json.loads(item_json)
            user_data["qty"] += guest_data["qty"]
            await r.hset(user_key, product_id, json.dumps(user_data))
        else:
            await r.hset(user_key, product_id, item_json)

    await r.delete(guest_key)
    return {"status": "merged"}
