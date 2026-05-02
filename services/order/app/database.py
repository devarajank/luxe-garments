from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Add new columns to existing tables if they don't exist
        for col, definition in [
            ("return_reason", "TEXT"),
            ("refund_amount", "NUMERIC(10,2)"),
        ]:
            await conn.execute(__import__("sqlalchemy").text(
                f"ALTER TABLE orders ADD COLUMN IF NOT EXISTS {col} {definition}"
            ))
