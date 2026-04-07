from contextlib import asynccontextmanager
from fastapi import FastAPI
from datetime import datetime, timedelta
from app.database import init_db, async_session
from app.models import Promotion
from app.routes import router
from sqlalchemy import select


async def seed_promotions():
    """Seed default promotions if none exist."""
    async with async_session() as session:
        result = await session.execute(select(Promotion).limit(1))
        if result.scalar_one_or_none():
            return  # Already seeded

        now = datetime.utcnow()
        promotions = [
            Promotion(
                code="WELCOME10",
                description="10% off your first order",
                discount_type="percentage",
                discount_value=10.0,
                min_order_value=None,
                max_discount=50.0,
                usage_limit=None,
                per_user_limit=1,
                applicable_categories=None,
                applicable_products=None,
                start_date=now,
                end_date=now + timedelta(days=365),
                is_active=True,
            ),
            Promotion(
                code="SUMMER25",
                description="25% off summer sale - minimum order $100",
                discount_type="percentage",
                discount_value=25.0,
                min_order_value=100.0,
                max_discount=75.0,
                usage_limit=None,
                per_user_limit=3,
                applicable_categories=None,
                applicable_products=None,
                start_date=now,
                end_date=now + timedelta(days=90),
                is_active=True,
            ),
            Promotion(
                code="FLAT20",
                description="$20 off on orders over $80",
                discount_type="fixed",
                discount_value=20.0,
                min_order_value=80.0,
                max_discount=None,
                usage_limit=None,
                per_user_limit=2,
                applicable_categories=None,
                applicable_products=None,
                start_date=now,
                end_date=now + timedelta(days=180),
                is_active=True,
            ),
            Promotion(
                code="DENIM15",
                description="15% off all jeans",
                discount_type="percentage",
                discount_value=15.0,
                min_order_value=None,
                max_discount=None,
                usage_limit=None,
                per_user_limit=2,
                applicable_categories=["jeans"],
                applicable_products=None,
                start_date=now,
                end_date=now + timedelta(days=120),
                is_active=True,
            ),
        ]

        for p in promotions:
            session.add(p)
        await session.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await seed_promotions()
    yield


app = FastAPI(title="Luxe Garments - Promotion Service", lifespan=lifespan)
app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "promotion"}
