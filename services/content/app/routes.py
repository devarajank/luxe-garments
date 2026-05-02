from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
import httpx
import time
from app.database import get_db
from app.models import ContentSlot
from app.schemas import (
    ContentSlotResponse,
    CreateContentSlotRequest,
    UpdateContentSlotRequest,
    ContentSlotListResponse,
    PublicContentResponse,
)
from app.config import (
    CONTENTFUL_SPACE_ID,
    CONTENTFUL_ACCESS_TOKEN,
    CONTENTFUL_BASE_URL,
    CONTENTFUL_CACHE_TTL,
)

router = APIRouter(prefix="/api/content", tags=["content"])

# Simple in-memory cache to avoid burning Contentful API quota
_contentful_cache: dict = {"data": None, "ts": 0.0}


def slot_to_response(slot: ContentSlot) -> ContentSlotResponse:
    return ContentSlotResponse(
        id=slot.id,
        slot_key=slot.slot_key,
        slot_type=slot.slot_type,
        title=slot.title,
        subtitle=slot.subtitle,
        body_text=slot.body_text,
        image_url=slot.image_url,
        link_text=slot.link_text,
        link_action=slot.link_action,
        badge_text=slot.badge_text,
        display_order=slot.display_order,
        is_active=slot.is_active,
        metadata_json=slot.metadata_json,
        updated_at=slot.updated_at,
        created_at=slot.created_at,
    )


async def _fetch_from_contentful() -> Optional[PublicContentResponse]:
    """Fetch content slots from Contentful Delivery API with in-memory caching."""
    if not CONTENTFUL_SPACE_ID or not CONTENTFUL_ACCESS_TOKEN:
        return None

    now = time.monotonic()
    if _contentful_cache["data"] and now - _contentful_cache["ts"] < CONTENTFUL_CACHE_TTL:
        return _contentful_cache["data"]

    url = f"{CONTENTFUL_BASE_URL}/spaces/{CONTENTFUL_SPACE_ID}/entries"
    params = {
        "access_token": CONTENTFUL_ACCESS_TOKEN,
        "content_type": "contentSlot",
        "limit": 100,
        "order": "fields.displayOrder",
    }

    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

    slots: dict[str, ContentSlotResponse] = {}
    for item in data.get("items", []):
        fields = item.get("fields", {})
        slot_key = fields.get("slotKey")
        if not slot_key or not fields.get("isActive", True):
            continue
        slots[slot_key] = ContentSlotResponse(
            id=item["sys"]["id"],
            slot_key=slot_key,
            slot_type=fields.get("slotType", "text"),
            title=fields.get("title"),
            subtitle=fields.get("subtitle"),
            body_text=fields.get("bodyText"),
            image_url=fields.get("imageUrl"),
            link_text=fields.get("linkText"),
            link_action=fields.get("linkAction"),
            badge_text=fields.get("badgeText"),
            display_order=fields.get("displayOrder", 0),
            is_active=fields.get("isActive", True),
            metadata_json=fields.get("metadataJson"),
        )

    result = PublicContentResponse(slots=slots)
    _contentful_cache["data"] = result
    _contentful_cache["ts"] = now
    return result


# ── Public endpoints ──────────────────────────────────────────────────

@router.get("/slots", response_model=PublicContentResponse)
async def get_public_slots(db: AsyncSession = Depends(get_db)):
    """Return all active content slots as a dict keyed by slot_key.
    Uses Contentful if configured, falls back to local DB."""
    contentful_response = await _fetch_from_contentful()
    if contentful_response is not None:
        return contentful_response

    # DB fallback
    result = await db.execute(
        select(ContentSlot)
        .where(ContentSlot.is_active == True)
        .order_by(ContentSlot.display_order)
    )
    slots = result.scalars().all()
    return PublicContentResponse(
        slots={slot.slot_key: slot_to_response(slot) for slot in slots}
    )


# ── Admin endpoints ───────────────────────────────────────────────────

@router.get("/admin/slots", response_model=ContentSlotListResponse)
async def list_all_slots(
    x_user_role: Optional[str] = Header(None),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List all slots (active and inactive) with pagination."""
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    count_result = await db.execute(select(func.count(ContentSlot.id)))
    total = count_result.scalar()

    result = await db.execute(
        select(ContentSlot)
        .order_by(ContentSlot.display_order, ContentSlot.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )
    slots = result.scalars().all()

    return ContentSlotListResponse(
        slots=[slot_to_response(s) for s in slots],
        total=total,
    )


@router.get("/admin/slots/{slot_id}", response_model=ContentSlotResponse)
async def get_slot(
    slot_id: str,
    x_user_role: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    """Get one slot by ID."""
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    result = await db.execute(select(ContentSlot).where(ContentSlot.id == slot_id))
    slot = result.scalar_one_or_none()
    if not slot:
        raise HTTPException(status_code=404, detail="Content slot not found")
    return slot_to_response(slot)


@router.post("/admin/slots", response_model=ContentSlotResponse)
async def create_slot(
    req: CreateContentSlotRequest,
    x_user_role: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    """Create a new content slot."""
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    # Check for duplicate slot_key
    existing = await db.execute(select(ContentSlot).where(ContentSlot.slot_key == req.slot_key))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail=f"Slot key '{req.slot_key}' already exists")

    slot = ContentSlot(
        slot_key=req.slot_key,
        slot_type=req.slot_type,
        title=req.title,
        subtitle=req.subtitle,
        body_text=req.body_text,
        image_url=req.image_url,
        link_text=req.link_text,
        link_action=req.link_action,
        badge_text=req.badge_text,
        display_order=req.display_order,
        is_active=req.is_active,
        metadata_json=req.metadata_json,
    )
    db.add(slot)
    await db.commit()
    await db.refresh(slot)
    return slot_to_response(slot)


@router.put("/admin/slots/{slot_id}", response_model=ContentSlotResponse)
async def update_slot(
    slot_id: str,
    req: UpdateContentSlotRequest,
    x_user_role: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    """Update a content slot."""
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    result = await db.execute(select(ContentSlot).where(ContentSlot.id == slot_id))
    slot = result.scalar_one_or_none()
    if not slot:
        raise HTTPException(status_code=404, detail="Content slot not found")

    update_data = req.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(slot, field, value)

    await db.commit()
    await db.refresh(slot)
    return slot_to_response(slot)


@router.delete("/admin/slots/{slot_id}", response_model=ContentSlotResponse)
async def delete_slot(
    slot_id: str,
    x_user_role: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    """Soft delete: set is_active=False."""
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    result = await db.execute(select(ContentSlot).where(ContentSlot.id == slot_id))
    slot = result.scalar_one_or_none()
    if not slot:
        raise HTTPException(status_code=404, detail="Content slot not found")

    slot.is_active = False
    await db.commit()
    await db.refresh(slot)
    return slot_to_response(slot)
