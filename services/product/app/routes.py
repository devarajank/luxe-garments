from fastapi import APIRouter, Depends, HTTPException, Query, Header, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from typing import Optional
import uuid
import os
from app.database import get_db
from app.models import Product, Category, Subcategory
from app.schemas import ProductResponse, CategoryResponse, SubcategoryResponse, ProductListResponse, ProductCreate, ProductUpdate

UPLOAD_DIR = "/app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

router = APIRouter(prefix="/api/products", tags=["products"])


def product_to_response(p: Product) -> ProductResponse:
    return ProductResponse(
        id=p.id,
        name=p.name,
        subtitle=p.subtitle,
        price=float(p.price),
        original_price=float(p.original_price) if p.original_price else None,
        image_url=p.image_url,
        colors=p.colors or [],
        sizes=p.sizes or [],
        badge=p.badge,
        details=p.details or [],
        category=p.subcategory.category.slug if p.subcategory else "",
        subcategory=p.subcategory.slug if p.subcategory else "",
    )


@router.get("/categories", response_model=list[CategoryResponse])
async def list_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Category).order_by(Category.id)
    )
    categories = result.scalars().all()
    response = []
    for cat in categories:
        await db.refresh(cat, ["subcategories"])
        subs = []
        for sub in cat.subcategories:
            count_result = await db.execute(
                select(func.count(Product.id)).where(Product.subcategory_id == sub.id, Product.is_active == True)
            )
            subs.append(SubcategoryResponse(
                slug=sub.slug, display_name=sub.display_name, product_count=count_result.scalar()
            ))
        response.append(CategoryResponse(slug=cat.slug, name=cat.name, subcategories=subs))
    return response


@router.get("/", response_model=ProductListResponse)
async def list_products(
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    badge: Optional[str] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = select(Product).where(Product.is_active == True).join(Subcategory).join(Category)

    if category:
        query = query.where(Category.slug == category)
    if subcategory:
        query = query.where(Subcategory.slug == subcategory)
    if badge:
        query = query.where(Product.badge == badge)
    if search:
        # PostgreSQL full-text search on name and subtitle
        query = query.where(
            text("to_tsvector('english', COALESCE(products.name, '') || ' ' || COALESCE(products.subtitle, '')) @@ plainto_tsquery('english', :search_query)").bindparams(search_query=search)
        )
    if min_price is not None:
        query = query.where(Product.price >= min_price)
    if max_price is not None:
        query = query.where(Product.price <= max_price)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Sort
    if sort_by == "price_asc":
        query = query.order_by(Product.price.asc())
    elif sort_by == "price_desc":
        query = query.order_by(Product.price.desc())
    else:
        query = query.order_by(Product.created_at.desc())

    # Paginate
    query = query.offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    products = result.scalars().all()

    # Eagerly load relationships for response
    items = []
    for p in products:
        await db.refresh(p, ["subcategory"])
        await db.refresh(p.subcategory, ["category"])
        items.append(product_to_response(p))

    return ProductListResponse(products=items, total=total, page=page, limit=limit)


@router.get("/deals", response_model=list[ProductResponse])
async def get_deals(
    limit: int = Query(8, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Get featured/discounted products for deals section."""
    result = await db.execute(
        select(Product)
        .where(Product.is_active == True)
        .order_by(Product.created_at.desc())
        .limit(limit)
    )
    products = result.scalars().all()
    items = []
    for p in products:
        await db.refresh(p, ["subcategory"])
        if p.subcategory:
            await db.refresh(p.subcategory, ["category"])
        items.append(product_to_response(p))
    return items


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await db.refresh(product, ["subcategory"])
    await db.refresh(product.subcategory, ["category"])
    return product_to_response(product)


@router.post("/", response_model=ProductResponse)
async def create_product(
    req: ProductCreate,
    x_user_role: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    # Look up subcategory by slug + category slug
    result = await db.execute(
        select(Subcategory).join(Category).where(
            Subcategory.slug == req.subcategory,
            Category.slug == req.category,
        )
    )
    subcategory = result.scalar_one_or_none()
    if not subcategory:
        raise HTTPException(status_code=400, detail=f"Subcategory '{req.subcategory}' in category '{req.category}' not found")

    # Check if product ID already exists
    existing = await db.execute(select(Product).where(Product.id == req.id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail=f"Product with ID '{req.id}' already exists")

    product = Product(
        id=req.id,
        subcategory_id=subcategory.id,
        name=req.name,
        subtitle=req.subtitle,
        price=req.price,
        original_price=req.original_price,
        image_url=req.image_url,
        colors=req.colors,
        sizes=req.sizes,
        badge=req.badge,
        details=req.details,
    )
    db.add(product)
    await db.commit()
    await db.refresh(product, ["subcategory"])
    await db.refresh(product.subcategory, ["category"])
    return product_to_response(product)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    req: ProductUpdate,
    x_user_role: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update subcategory if category/subcategory changed
    if req.category and req.subcategory:
        sub_result = await db.execute(
            select(Subcategory).join(Category).where(
                Subcategory.slug == req.subcategory,
                Category.slug == req.category,
            )
        )
        subcategory = sub_result.scalar_one_or_none()
        if not subcategory:
            raise HTTPException(status_code=400, detail="Subcategory not found")
        product.subcategory_id = subcategory.id

    if req.name is not None:
        product.name = req.name
    if req.subtitle is not None:
        product.subtitle = req.subtitle
    if req.price is not None:
        product.price = req.price
    if req.original_price is not None:
        product.original_price = req.original_price
    if req.image_url is not None:
        product.image_url = req.image_url
    if req.colors is not None:
        product.colors = req.colors
    if req.sizes is not None:
        product.sizes = req.sizes
    if req.badge is not None:
        product.badge = req.badge
    if req.details is not None:
        product.details = req.details
    if req.is_active is not None:
        product.is_active = req.is_active

    await db.commit()
    await db.refresh(product, ["subcategory"])
    await db.refresh(product.subcategory, ["category"])
    return product_to_response(product)


@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    x_user_role: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.is_active = False
    await db.commit()
    return {"status": "deleted", "id": product_id}


@router.post("/{product_id}/image", response_model=ProductResponse)
async def upload_product_image(
    product_id: str,
    file: UploadFile = File(...),
    x_user_role: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type. Allowed: jpg, jpeg, png, webp")

    filename = file.filename or ""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Invalid file extension. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")

    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Remove old local file if present
    if product.image_url and product.image_url.startswith("/uploads/"):
        old_path = os.path.join(UPLOAD_DIR, os.path.basename(product.image_url))
        if os.path.isfile(old_path):
            os.remove(old_path)

    short_uuid = uuid.uuid4().hex[:8]
    new_filename = f"{product_id}_{short_uuid}.{ext}"
    save_path = os.path.join(UPLOAD_DIR, new_filename)

    contents = await file.read()
    with open(save_path, "wb") as f:
        f.write(contents)

    product.image_url = f"/uploads/{new_filename}"
    await db.commit()
    await db.refresh(product, ["subcategory"])
    await db.refresh(product.subcategory, ["category"])
    return product_to_response(product)


@router.delete("/{product_id}/image", response_model=ProductResponse)
async def delete_product_image(
    product_id: str,
    x_user_role: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.image_url and product.image_url.startswith("/uploads/"):
        old_path = os.path.join(UPLOAD_DIR, os.path.basename(product.image_url))
        if os.path.isfile(old_path):
            os.remove(old_path)

    product.image_url = ""
    await db.commit()
    await db.refresh(product, ["subcategory"])
    await db.refresh(product.subcategory, ["category"])
    return product_to_response(product)
