from jose import jwt, JWTError
from app.config import JWT_SECRET, JWT_ALGORITHM


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError:
        return None
