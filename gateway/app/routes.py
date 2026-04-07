import httpx
from fastapi import APIRouter, Request, HTTPException, Response
from app.config import SERVICE_MAP, PUBLIC_ROUTES
from app.middleware.auth import decode_token

router = APIRouter()


def resolve_service(path: str) -> tuple[str, str]:
    """Given /api/products/..., return (base_url, full_path)."""
    parts = path.strip("/").split("/")
    if len(parts) < 2 or parts[0] != "api":
        raise HTTPException(status_code=404, detail="Unknown route")

    service_name = parts[1]  # users, products, cart, orders
    base_url = SERVICE_MAP.get(service_name)
    if not base_url:
        raise HTTPException(status_code=404, detail=f"Unknown service: {service_name}")

    return base_url, path


def is_public_route(method: str, path: str) -> bool:
    for pub_method, pub_path in PUBLIC_ROUTES:
        if method == pub_method and path.rstrip("/").startswith(pub_path.rstrip("/")):
            return True
    return False


def is_auth_optional(path: str) -> bool:
    """Cart endpoints work for both guests and authenticated users."""
    return "/api/cart" in path


async def proxy_request(request: Request, base_url: str, path: str, user_id: str = None, user_role: str = None):
    """Forward the request to the target service."""
    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("Host", None)

    if user_id:
        headers["x-user-id"] = user_id
    if user_role:
        headers["x-user-role"] = user_role

    body = await request.body()
    url = f"{base_url}{path}"
    if request.url.query:
        url += f"?{request.url.query}"

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=body,
                timeout=30,
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

    response_headers = dict(resp.headers)
    response_headers.pop("transfer-encoding", None)
    response_headers.pop("content-encoding", None)
    response_headers.pop("content-length", None)

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=response_headers,
        media_type=resp.headers.get("content-type"),
    )


@router.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway(request: Request, path: str):
    full_path = f"/api/{path}"
    base_url, target_path = resolve_service(full_path)

    user_id = None
    auth_header = request.headers.get("authorization", "")
    session_id = request.headers.get("x-session-id", "")

    user_role = None
    if auth_header.startswith("Bearer "):
        token = auth_header.replace("Bearer ", "")
        payload = decode_token(token)
        if payload:
            user_id = payload.get("sub")
            user_role = payload.get("role")

    # Check auth requirement
    if not is_public_route(request.method, full_path) and not is_auth_optional(full_path):
        if not user_id:
            raise HTTPException(status_code=401, detail="Authentication required")

    return await proxy_request(request, base_url, target_path, user_id, user_role)
