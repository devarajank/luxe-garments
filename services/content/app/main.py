from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db, async_session
from app.models import ContentSlot
from app.routes import router
from sqlalchemy import select


DEFAULT_SLOTS = [
    {
        "slot_key": "promo_bar",
        "slot_type": "promo_bar",
        "title": "FREE SHIPPING ON ORDERS OVER $100 | USE CODE: LUXE2026",
        "is_active": True,
        "display_order": 0,
    },
    {
        "slot_key": "hero_banner",
        "slot_type": "hero",
        "badge_text": "Spring / Summer 2026",
        "title": "THE NEW\nDENIM ERA",
        "body_text": "Crafted for comfort. Designed for style. Our latest collection blends heritage craftsmanship with modern innovation.",
        "image_url": "",
        "link_text": "SHOP MEN",
        "link_action": "showCategory('men')",
        "is_active": True,
        "display_order": 0,
        "metadata_json": {
            "secondary_link_text": "SHOP WOMEN",
            "secondary_link_action": "showCategory('women')",
        },
    },
    {
        "slot_key": "category_tile_1",
        "slot_type": "category_tile",
        "title": "MEN",
        "subtitle": "Jeans, Jackets, Shirts & More",
        "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&q=80",
        "link_action": "showCategory('men')",
        "is_active": True,
        "display_order": 1,
    },
    {
        "slot_key": "category_tile_2",
        "slot_type": "category_tile",
        "title": "WOMEN",
        "subtitle": "Jeans, Jackets, Tops & Dresses",
        "image_url": "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=600&q=80",
        "link_action": "showCategory('women')",
        "is_active": True,
        "display_order": 2,
    },
    {
        "slot_key": "category_tile_3",
        "slot_type": "category_tile",
        "title": "KIDS",
        "subtitle": "Jeans, T-Shirts & Jackets",
        "image_url": "https://images.unsplash.com/photo-1503919545889-aef636e10ad4?w=600&q=80",
        "link_action": "showCategory('kids')",
        "is_active": True,
        "display_order": 3,
    },
    {
        "slot_key": "featured_banner",
        "slot_type": "banner",
        "title": "BUILT TO LAST",
        "body_text": "Every stitch tells a story. Premium denim crafted with care, designed to get better with age.",
        "link_text": "EXPLORE WOMEN'S",
        "link_action": "showCategory('women')",
        "is_active": True,
        "display_order": 0,
    },
    {
        "slot_key": "collection_1",
        "slot_type": "collection_card",
        "title": "TRUCKER JACKET",
        "subtitle": "The icon. Reimagined for 2026.",
        "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&q=80",
        "link_text": "SHOP JACKETS",
        "link_action": "showCategory('men','jackets')",
        "is_active": True,
        "display_order": 1,
    },
    {
        "slot_key": "collection_2",
        "slot_type": "collection_card",
        "title": "DRESSES",
        "subtitle": "From day to night, effortlessly.",
        "image_url": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800&q=80",
        "link_text": "SHOP DRESSES",
        "link_action": "showCategory('women','dresses')",
        "is_active": True,
        "display_order": 2,
    },
    {
        "slot_key": "footer_tagline",
        "slot_type": "text",
        "title": "LUXE GARMENTS",
        "body_text": "Crafted for those who value quality, style, and authenticity. Premium denim and fashion since 1987.",
        "is_active": True,
        "display_order": 0,
    },
]


async def seed_content_slots():
    """Seed default content slots if none exist."""
    async with async_session() as session:
        result = await session.execute(select(ContentSlot).limit(1))
        if result.scalar_one_or_none():
            return  # Already seeded

        for slot_data in DEFAULT_SLOTS:
            slot = ContentSlot(**slot_data)
            session.add(slot)
        await session.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await seed_content_slots()
    yield


app = FastAPI(title="Luxe Garments - Content Service", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "content"}
