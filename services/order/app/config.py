import os

DATABASE_URL = os.getenv("ORDER_DB_URL", "postgresql+asyncpg://luxe:luxe123@localhost:5436/order_db")
CART_SERVICE_URL = os.getenv("CART_SERVICE_URL", "http://localhost:8002")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://localhost:8001")
PROMOTION_SERVICE_URL = os.getenv("PROMOTION_SERVICE_URL", "http://localhost:8005")
