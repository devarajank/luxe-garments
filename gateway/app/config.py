import os

JWT_SECRET = os.getenv("JWT_SECRET", "luxe-garments-secret-key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

SERVICE_MAP = {
    "users": os.getenv("USER_SERVICE_URL", "http://user-service:8004"),
    "products": os.getenv("PRODUCT_SERVICE_URL", "http://product-service:8001"),
    "cart": os.getenv("CART_SERVICE_URL", "http://cart-service:8002"),
    "orders": os.getenv("ORDER_SERVICE_URL", "http://order-service:8003"),
    "promotions": os.getenv("PROMOTION_SERVICE_URL", "http://promotion-service:8005"),
    "content": os.getenv("CONTENT_SERVICE_URL", "http://content-service:8006"),
}

# Routes that don't need authentication
PUBLIC_ROUTES = [
    ("POST", "/api/users/register"),
    ("POST", "/api/users/login"),
    ("POST", "/api/users/forgot-password"),
    ("POST", "/api/users/reset-password"),
    ("GET", "/api/products"),
    ("GET", "/api/products/categories"),
    ("GET", "/api/products/search"),
    ("GET", "/api/products/"),
    ("POST", "/api/orders/"),
    ("POST", "/api/promotions/validate"),
    ("GET", "/api/content/slots"),
    ("GET", "/api/content/deals"),
]
