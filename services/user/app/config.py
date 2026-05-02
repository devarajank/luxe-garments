import os

DATABASE_URL = os.getenv("USER_DB_URL", "postgresql+asyncpg://luxe:luxe123@localhost:5434/user_db")
JWT_SECRET = os.getenv("JWT_SECRET", "luxe-garments-secret-key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRY_HOURS = int(os.getenv("JWT_EXPIRY_HOURS", "24"))
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
SMTP_FROM = os.getenv("SMTP_FROM", "noreply@luxegarments.com")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
