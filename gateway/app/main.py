from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
import os

app = FastAPI(title="Luxe Garments - API Gateway")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(router)

# Serve frontend static files
STATIC_DIR = "/app/static"
if os.path.exists(STATIC_DIR):
    # Serve assets and other static files
    app.mount("/assets", StaticFiles(directory=os.path.join(STATIC_DIR, "assets")), name="assets")

    # Fallback: serve index.html for all non-API routes (SPA routing)
    @app.get("/{path:path}")
    async def serve_spa(path: str):
        # Don't intercept health checks
        if path == "health":
            return {"status": "ok", "service": "gateway"}

        file_path = os.path.join(STATIC_DIR, path)

        # If it's a file that exists, serve it
        if os.path.isfile(file_path):
            return FileResponse(file_path)

        # Otherwise, serve index.html for React Router SPA
        return FileResponse(os.path.join(STATIC_DIR, "index.html"))

    # Serve root
    @app.get("/")
    async def serve_index():
        return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/health")
async def health():
    return {"status": "ok", "service": "gateway"}
