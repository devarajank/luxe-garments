# Luxe Garments - Server & Database Access Guide

## Overview
Complete access details for all microservices, databases, and cache layer in the Luxe Garments platform.

---

## Microservices

### 1. API Gateway
- **Port:** 8000
- **URL:** `http://localhost:8000`
- **Purpose:** Entry point for all API requests, request routing, and static file serving
- **Frontend Access:** `http://localhost:8000` (serves index.html, admin.html)
- **Dependencies:** All downstream services
- **Status:** `docker compose ps`

### 2. User Service
- **Port:** 8004
- **URL:** `http://localhost:8004`
- **Database:** `user-db` (PostgreSQL on port 5434)
- **Purpose:** User authentication, registration, profile management
- **Dependencies:** user-db, Redis
- **Key Endpoints:**
  - POST `/register` - User registration
  - POST `/login` - User login
  - GET `/profile/{user_id}` - Get user profile

### 3. Product Service
- **Port:** 8001
- **URL:** `http://localhost:8001`
- **Database:** `product-db` (PostgreSQL on port 5435)
- **Purpose:** Product catalog, inventory management
- **Dependencies:** product-db
- **Key Endpoints:**
  - GET `/products` - List all products
  - GET `/products/{product_id}` - Get product details
  - POST `/products` - Create product (admin)

### 4. Cart Service
- **Port:** 8002
- **URL:** `http://localhost:8002`
- **Cache:** Redis (port 6379)
- **Purpose:** Shopping cart management
- **Dependencies:** Redis, Product Service
- **Key Endpoints:**
  - GET `/cart/{user_id}` - Get user cart
  - POST `/cart/{user_id}/add` - Add item to cart
  - DELETE `/cart/{user_id}/remove` - Remove item from cart

### 5. Order Service
- **Port:** 8003
- **URL:** `http://localhost:8003`
- **Database:** `order-db` (PostgreSQL on port 5436)
- **Purpose:** Order processing, order history
- **Dependencies:** order-db, Cart Service, User Service
- **Key Endpoints:**
  - POST `/orders` - Create new order
  - GET `/orders/{user_id}` - Get user orders
  - GET `/orders/{order_id}` - Get order details

### 6. Promotion Service
- **Port:** 8005
- **URL:** `http://localhost:8005`
- **Database:** `promotion-db` (PostgreSQL on port 5437)
- **Purpose:** Discount codes, promotional campaigns, special offers
- **Dependencies:** promotion-db
- **Key Endpoints:**
  - GET `/promotions` - List active promotions
  - POST `/promotions` - Create promotion (admin)
  - POST `/validate-code` - Validate discount code

### 7. Content Service
- **Port:** 8006
- **URL:** `http://localhost:8006`
- **Database:** `content-db` (PostgreSQL on port 5438)
- **Purpose:** Blog posts, marketing content, static pages
- **Dependencies:** content-db
- **Key Endpoints:**
  - GET `/content` - List all content
  - GET `/content/{content_id}` - Get content details
  - POST `/content` - Create content (admin)

---

## Databases

All PostgreSQL databases use the same credentials:
- **Username:** `luxe`
- **Password:** `luxe123`

### 1. User Database
- **Container Name:** user-db
- **Port (Local):** 5434
- **Port (Container):** 5432
- **Database Name:** user_db
- **Connection String (Local):** `postgresql://luxe:luxe123@localhost:5434/user_db`
- **Connection String (Docker Network):** `postgresql+asyncpg://luxe:luxe123@user-db:5432/user_db`
- **Tables:** users, sessions, auth_tokens
- **Volume:** user_data

### 2. Product Database
- **Container Name:** product-db
- **Port (Local):** 5435
- **Port (Container):** 5432
- **Database Name:** product_db
- **Connection String (Local):** `postgresql://luxe:luxe123@localhost:5435/product_db`
- **Connection String (Docker Network):** `postgresql+asyncpg://luxe:luxe123@product-db:5432/product_db`
- **Tables:** products, categories, inventory
- **Volume:** product_data

### 3. Order Database
- **Container Name:** order-db
- **Port (Local):** 5436
- **Port (Container):** 5432
- **Database Name:** order_db
- **Connection String (Local):** `postgresql://luxe:luxe123@localhost:5436/order_db`
- **Connection String (Docker Network):** `postgresql+asyncpg://luxe:luxe123@order-db:5432/order_db`
- **Tables:** orders, order_items, order_status
- **Volume:** order_data

### 4. Promotion Database
- **Container Name:** promotion-db
- **Port (Local):** 5437
- **Port (Container):** 5432
- **Database Name:** promotion_db
- **Connection String (Local):** `postgresql://luxe:luxe123@localhost:5437/promotion_db`
- **Connection String (Docker Network):** `postgresql+asyncpg://luxe:luxe123@promotion-db:5432/promotion_db`
- **Tables:** promotions, discount_codes, campaign_rules
- **Volume:** promotion_data

### 5. Content Database
- **Container Name:** content-db
- **Port (Local):** 5438
- **Port (Container):** 5432
- **Database Name:** content_db
- **Connection String (Local):** `postgresql://luxe:luxe123@localhost:5438/content_db`
- **Connection String (Docker Network):** `postgresql+asyncpg://luxe:luxe123@content-db:5432/content_db`
- **Tables:** content, articles, pages
- **Volume:** content_data

---

## Cache Layer

### Redis
- **Container Name:** redis
- **Port:** 6379
- **URL (Local):** `redis://localhost:6379/0`
- **URL (Docker Network):** `redis://redis:6379/0`
- **Purpose:** Cart data caching, session storage, rate limiting
- **Volume:** redis_data
- **Persistence:** Enabled (AOF - Append Only File)

---

## Connection Examples

### Via Docker Network (Service-to-Service)
```python
# Inside a microservice container
import asyncpg

# PostgreSQL
conn = await asyncpg.connect('postgresql+asyncpg://luxe:luxe123@user-db:5432/user_db')

# Redis
import redis
r = redis.Redis(host='redis', port=6379, db=0)
```

### Via localhost (From Host Machine)
```python
import asyncpg
import redis

# PostgreSQL User DB
conn = await asyncpg.connect('postgresql://luxe:luxe123@localhost:5434/user_db')

# Redis
r = redis.Redis(host='localhost', port=6379, db=0)
```

---

## Environment Variables

All services use the `.env` file for configuration:

```
JWT_SECRET=luxe-garments-secret-key-change-in-production-2024
JWT_ALGORITHM=HS256
JWT_EXPIRY_HOURS=24

# Database URLs (internal Docker network)
USER_DB_URL=postgresql+asyncpg://luxe:luxe123@user-db:5432/user_db
PRODUCT_DB_URL=postgresql+asyncpg://luxe:luxe123@product-db:5432/product_db
ORDER_DB_URL=postgresql+asyncpg://luxe:luxe123@order-db:5432/order_db
PROMOTION_DB_URL=postgresql+asyncpg://luxe:luxe123@promotion-db:5432/promotion_db
CONTENT_DB_URL=postgresql+asyncpg://luxe:luxe123@content-db:5432/content_db

# Redis
REDIS_URL=redis://redis:6379/0

# Service URLs (internal Docker network)
PRODUCT_SERVICE_URL=http://product-service:8001
CART_SERVICE_URL=http://cart-service:8002
ORDER_SERVICE_URL=http://order-service:8003
USER_SERVICE_URL=http://user-service:8004
PROMOTION_SERVICE_URL=http://promotion-service:8005
CONTENT_SERVICE_URL=http://content-service:8006

# Postgres credentials
POSTGRES_USER=luxe
POSTGRES_PASSWORD=luxe123
```

---

## Startup & Management

### Start All Services
```bash
cd ~/eCommerce/luxe-garments
docker compose up -d
```

### Check Service Status
```bash
docker compose ps
```

### View Service Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f user-service
docker compose logs -f product-db
```

### Access PostgreSQL Directly
```bash
# User DB
psql -h localhost -p 5434 -U luxe -d user_db

# Product DB
psql -h localhost -p 5435 -U luxe -d product_db

# Order DB
psql -h localhost -p 5436 -U luxe -d order_db

# Promotion DB
psql -h localhost -p 5437 -U luxe -d promotion_db

# Content DB
psql -h localhost -p 5438 -U luxe -d content_db
```

### Access Redis CLI
```bash
redis-cli -h localhost -p 6379
```

### Stop All Services
```bash
docker compose down
```

### Reset Volumes (Clear All Data)
```bash
docker compose down -v
```

---

## Health Checks

All databases and Redis have health checks configured:
- **Interval:** 5 seconds
- **Timeout:** 3 seconds
- **Retries:** 5 attempts

View health status:
```bash
docker compose ps
```

---

## Network

All services communicate via the `luxe-net` Docker bridge network:
- Internal service-to-service communication uses container names (e.g., `http://user-service:8004`)
- External access from host uses localhost with mapped ports

---

## Security Notes

⚠️ **For Production:**
- Change all default passwords (currently `luxe123`)
- Update JWT_SECRET to a strong, unique value
- Use environment-specific .env files
- Enable SSL/TLS for database connections
- Implement proper secret management (AWS Secrets Manager, HashiCorp Vault, etc.)
- Set database user permissions appropriately

---

## Frontend Access

- **Main Store:** `http://localhost:8000`
- **Admin Panel:** `http://localhost:8000/admin.html`

Both are served by the API Gateway.
