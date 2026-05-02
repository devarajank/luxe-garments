import uuid
import redis.asyncio as aioredis
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.database import get_db
from app.models import User, Address
from app.schemas import (
    RegisterRequest, LoginRequest, TokenResponse, UserResponse,
    ProfileUpdate, AddressCreate, AddressResponse,
    ForgotPasswordRequest, ResetPasswordRequest,
)
from app.auth import hash_password, verify_password, create_token, decode_token
from app.config import REDIS_URL, FRONTEND_URL
from app.email_utils import send_password_reset_email

RESET_TOKEN_TTL = 3600  # 1 hour


def get_redis():
    return aioredis.from_url(REDIS_URL, decode_responses=True)

router = APIRouter(prefix="/api/users", tags=["users"])


async def get_current_user(
    x_user_id: Optional[str] = Header(None),
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
) -> User:
    user_id = x_user_id
    if not user_id and authorization:
        token = authorization.replace("Bearer ", "")
        payload = decode_token(token)
        if payload:
            user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.post("/register", response_model=TokenResponse)
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where(User.email == req.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        email=req.email,
        password_hash=hash_password(req.password),
        first_name=req.first_name,
        last_name=req.last_name,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    token = create_token(user.id, user.role)
    return TokenResponse(access_token=token, user=UserResponse.model_validate(user))


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == req.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_token(user.id, user.role)
    return TokenResponse(access_token=token, user=UserResponse.model_validate(user))


@router.get("/profile", response_model=UserResponse)
async def get_profile(user: User = Depends(get_current_user)):
    return UserResponse.model_validate(user)


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    req: ProfileUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if req.first_name is not None:
        user.first_name = req.first_name
    if req.last_name is not None:
        user.last_name = req.last_name
    if req.phone is not None:
        user.phone = req.phone
    await db.commit()
    await db.refresh(user)
    return UserResponse.model_validate(user)


@router.get("/addresses", response_model=list[AddressResponse])
async def list_addresses(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Address).where(Address.user_id == user.id))
    return [AddressResponse.model_validate(a) for a in result.scalars().all()]


@router.post("/addresses", response_model=AddressResponse)
async def create_address(
    req: AddressCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    addr = Address(user_id=user.id, **req.model_dump())
    if req.is_default:
        await db.execute(
            Address.__table__.update()
            .where(Address.user_id == user.id)
            .values(is_default=False)
        )
    db.add(addr)
    await db.commit()
    await db.refresh(addr)
    return AddressResponse.model_validate(addr)


@router.delete("/addresses/{address_id}")
async def delete_address(
    address_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Address).where(Address.id == address_id, Address.user_id == user.id)
    )
    addr = result.scalar_one_or_none()
    if not addr:
        raise HTTPException(status_code=404, detail="Address not found")
    await db.delete(addr)
    await db.commit()
    return {"status": "deleted"}


@router.post("/forgot-password")
async def forgot_password(req: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == req.email))
    user = result.scalar_one_or_none()
    # Always return success to prevent email enumeration
    if user:
        token = str(uuid.uuid4())
        redis = get_redis()
        async with redis:
            await redis.setex(f"reset:{token}", RESET_TOKEN_TTL, user.id)
        reset_link = f"{FRONTEND_URL}/reset-password?token={token}"
        await send_password_reset_email(user.email, reset_link)
    return {"message": "If that email is registered, a reset link has been sent."}


@router.post("/reset-password")
async def reset_password(req: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    if len(req.new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    redis = get_redis()
    async with redis:
        user_id = await redis.get(f"reset:{req.token}")
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid or expired reset token")
        await redis.delete(f"reset:{req.token}")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    user.password_hash = hash_password(req.new_password)
    await db.commit()
    return {"message": "Password updated successfully"}
