from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text
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
        # Create full-text search index on products
        try:
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_product_search
                ON products
                USING GIN(to_tsvector('english', COALESCE(name, '') || ' ' || COALESCE(subtitle, '')))
            """))
        except Exception:
            pass  # Index may already exist
