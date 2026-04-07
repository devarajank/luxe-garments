import os

DATABASE_URL = os.getenv("USER_DB_URL", "postgresql+asyncpg://luxe:luxe123@localhost:5434/user_db")
JWT_SECRET = os.getenv("JWT_SECRET", "luxe-garments-secret-key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRY_HOURS = int(os.getenv("JWT_EXPIRY_HOURS", "24"))
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
