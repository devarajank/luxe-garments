import os

DATABASE_URL = os.getenv("CONTENT_DB_URL", "postgresql+asyncpg://luxe:luxe123@localhost:5438/content_db")

# Contentful Delivery API (optional — falls back to DB if not set)
CONTENTFUL_SPACE_ID = os.getenv("CONTENTFUL_SPACE_ID", "")
CONTENTFUL_ACCESS_TOKEN = os.getenv("CONTENTFUL_ACCESS_TOKEN", "")
CONTENTFUL_BASE_URL = "https://cdn.contentful.com"
CONTENTFUL_CACHE_TTL = 60  # seconds
