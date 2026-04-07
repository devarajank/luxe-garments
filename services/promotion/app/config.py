import os

DATABASE_URL = os.getenv("PROMOTION_DB_URL", "postgresql+asyncpg://luxe:luxe123@localhost:5437/promotion_db")
