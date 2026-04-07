import os

DATABASE_URL = os.getenv("PRODUCT_DB_URL", "postgresql+asyncpg://luxe:luxe123@localhost:5435/product_db")
