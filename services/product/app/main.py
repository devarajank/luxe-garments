from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import init_db
from app.routes import router
from app.seed import seed_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await seed_database()
    yield


app = FastAPI(title="Luxe Garments - Product Service", lifespan=lifespan)
app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "product"}
