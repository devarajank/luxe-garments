# Luxe Garments - Access Guide

## Quick Start

```bash
cd ~/eCommerce/luxe-garments
docker compose up -d
```

---

## Frontend & Admin

| Component | URL | Port | Notes |
|-----------|-----|------|-------|
| **Main Site** | http://localhost:8000 | 8000 | Customer-facing storefront |
| **Admin Panel** | http://localhost:8000/admin | 8000 | Admin dashboard (route: /admin/orders, /admin/products, etc.) |

---

## API Gateway

| Service | URL | Port | Purpose |
|---------|-----|------|---------|
| **Gateway** | http://localhost:8000/api | 8000 | Routes all API requests to microservices |

### Gateway Routes

- `/api/products/` → Product Service (8001)
- `/api/cart/` → Cart Service (8002)
- `/api/orders/` → Order Service (8003)
- `/api/users/` → User Service (8004)
- `/api/promotions/` → Promotion Service (8005)
- `/api/content/` → Content Service (8006)

---

## Microservices

### Product Service
```
URL: http://localhost:8001
Port: 8001
Database: product_db (port 5432)
Endpoints:
  GET  /api/products/
  GET  /api/products/{id}
  GET  /api/products/categories
  GET  /api/products/deals
```

### Cart Service
```
URL: http://localhost:8002
Port: 8002
Database: cart_db (port 5432)
Endpoints:
  GET    /api/cart/
  POST   /api/cart/
  PUT    /api/cart/{item_id}
  DELETE /api/cart/{item_id}
```

### Order Service
```
URL: http://localhost:8003
Port: 8003
Database: order_db (port 5436)
Endpoints:
  GET    /api/orders/
  POST   /api/orders/
  GET    /api/orders/{order_id}
  GET    /api/orders/admin/all (requires x-user-role: admin)
  PUT    /api/orders/{order_id}/status
  PUT    /api/orders/{order_id}/cancel
```

### User Service
```
URL: http://localhost:8004
Port: 8004
Database: user_db (port 5432)
Endpoints:
  POST   /api/users/register
  POST   /api/users/login
  GET    /api/users/profile (requires authentication)
  PUT    /api/users/profile
```

### Promotion Service
```
URL: http://localhost:8005
Port: 8005
Database: promotion_db (port 5432)
Endpoints:
  POST   /api/promotions/validate
  POST   /api/promotions/apply
  GET    /api/promotions/
```

### Content Service
```
URL: http://localhost:8006
Port: 8006
Database: content_db (port 5432)
Endpoints:
  GET    /api/content/slots
  GET    /api/content/deals
```

---

## Databases

### Connection Details

**Host:** localhost (or service name inside Docker)
**Username:** luxe
**Password:** luxe123

### Database Ports & Names

| Service | Database Name | Port | Container Name |
|---------|---------------|------|-----------------|
| User | user_db | 5432 | user-db |
| Product | product_db | 5432 | product-db |
| Cart | cart_db | 5432 | cart-db |
| Order | order_db | 5436 | order-db |
| Promotion | promotion_db | 5432 | promotion-db |
| Content | content_db | 5432 | content-db |

### Access Database via psql

```bash
# Order DB (different port)
psql -h localhost -U luxe -d order_db -p 5436

# Other DBs (standard port 5432)
psql -h localhost -U luxe -d product_db

# Or via Docker
docker compose exec product-db psql -U luxe -d product_db
```

---

## Redis Cache

| Component | Location | Port |
|-----------|----------|------|
| **Redis** | http://localhost:6379 | 6379 |

Used for: Caching, sessions, real-time data

**Access via CLI:**
```bash
docker compose exec redis redis-cli
```

---

## Docker Commands

### View Running Services
```bash
docker compose ps
```

### View Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f product-service
docker compose logs -f order-service
docker compose logs -f gateway
```

### Restart Services
```bash
# All services
docker compose restart

# Specific service
docker compose restart product-service
```

### Stop & Start
```bash
docker compose down
docker compose up -d
```

---

## Useful API Examples

### Admin Orders Endpoint
```bash
curl -H "x-user-role: admin" http://localhost:8000/api/orders/admin/all
```

### Get Products
```bash
curl http://localhost:8000/api/products/?limit=10
```

### Create Order
```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -H "x-user-id: user-123" \
  -d '{"items": [...], "shipping_address": {...}}'
```

### Admin Update Order Status
```bash
curl -X PUT http://localhost:8000/api/orders/{order_id}/status \
  -H "x-user-role: admin" \
  -H "Content-Type: application/json" \
  -d '{"status": "shipped"}'
```

---

## Environment Variables

Located in: `.env`

```env
JWT_SECRET=luxe-garments-secret-key-change-in-production-2024
JWT_ALGORITHM=HS256
JWT_EXPIRY_HOURS=24

# Database URLs (Docker internal)
USER_DB_URL=postgresql+asyncpg://luxe:luxe123@user-db:5432/user_db
PRODUCT_DB_URL=postgresql+asyncpg://luxe:luxe123@product-db:5432/product_db
ORDER_DB_URL=postgresql+asyncpg://luxe:luxe123@order-db:5432/order_db
PROMOTION_DB_URL=postgresql+asyncpg://luxe:luxe123@promotion-db:5432/promotion_db
CONTENT_DB_URL=postgresql+asyncpg://luxe:luxe123@content-db:5432/content_db

# Redis
REDIS_URL=redis://redis:6379/0

# Service URLs (Docker internal)
PRODUCT_SERVICE_URL=http://product-service:8001
CART_SERVICE_URL=http://cart-service:8002
ORDER_SERVICE_URL=http://order-service:8003
USER_SERVICE_URL=http://user-service:8004
PROMOTION_SERVICE_URL=http://promotion-service:8005
CONTENT_SERVICE_URL=http://content-service:8006
```

---

## Project Structure

```
luxe-garments/
├── docker-compose.yml          # Container orchestration
├── gateway/                    # API Gateway (port 8000)
├── public/                     # Frontend static files (built)
├── frontend/                   # React frontend source
│   └── src/
│       ├── pages/             # Page components
│       ├── components/        # Reusable components
│       └── context/           # Context API
├── services/
│   ├── product/              # Product Service (8001)
│   ├── cart/                 # Cart Service (8002)
│   ├── order/                # Order Service (8003)
│   ├── user/                 # User Service (8004)
│   ├── promotion/            # Promotion Service (8005)
│   └── content/              # Content Service (8006)
├── .env                      # Environment variables
└── ACCESS_GUIDE.md          # This file
```

---

## Common Tasks

### View All Products
```bash
curl http://localhost:8000/api/products/?limit=100 | jq '.products[]'
```

### Check Service Health
```bash
curl http://localhost:8001/health  # Product
curl http://localhost:8003/health  # Order
```

### Clear Product Cache (if needed)
```bash
docker compose exec redis redis-cli FLUSHDB
```

### Rebuild Frontend
```bash
cd frontend
npm run build
```

### Access Admin Database
```bash
docker compose exec product-db psql -U luxe -d product_db
```

---

## Troubleshooting

### Services Not Starting
```bash
docker compose logs -f
docker compose restart
```

### Database Connection Issues
```bash
# Check if DB is healthy
docker compose ps

# Verify credentials in .env
cat .env | grep DB_URL
```

### Frontend Not Updating
```bash
# Clear browser cache (Ctrl+Shift+R)
# Or rebuild frontend
cd frontend && npm run build
```

### Images Not Loading
Check browser console (F12) for 404 errors on image URLs

---

## Important Headers

### User Authentication
```
x-user-id: user-123          # User identifier
x-session-id: session-abc    # Session token
Authorization: Bearer {jwt}  # JWT token
```

### Admin Access
```
x-user-role: admin           # Required for admin endpoints
```

---

## Contact & Notes

- **Stack:** Docker Compose, FastAPI, PostgreSQL, Redis, React
- **Node.js:** 20+ LTS
- **Python:** 3.11+
- **Database:** PostgreSQL 16

---

*Last Updated: 2026-04-11*
