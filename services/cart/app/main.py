from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Luxe Garments - Cart Service")
app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "cart"}
