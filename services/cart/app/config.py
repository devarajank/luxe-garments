import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://localhost:8001")
