from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import select
from app.database import init_db, async_session
from app.models import User
from app.auth import hash_password
from app.routes import router


async def seed_admin():
    """Create default admin user if it doesn't exist."""
    async with async_session() as db:
        result = await db.execute(select(User).where(User.email == "admin@luxegarments.com"))
        if not result.scalar_one_or_none():
            admin = User(
                email="admin@luxegarments.com",
                password_hash=hash_password("admin123"),
                first_name="Admin",
                last_name="User",
                role="admin",
            )
            db.add(admin)
            await db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await seed_admin()
    yield


app = FastAPI(title="Luxe Garments - User Service", lifespan=lifespan)
app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "user"}
