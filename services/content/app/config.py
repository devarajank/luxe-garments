import os

DATABASE_URL = os.getenv("CONTENT_DB_URL", "postgresql+asyncpg://luxe:luxe123@localhost:5438/content_db")
