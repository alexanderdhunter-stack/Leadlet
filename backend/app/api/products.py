"""Product API endpoints."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Product
from app.schemas.product import ProductResponse

router = APIRouter()


@router.get("/", response_model=list[ProductResponse])
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    company_id: Optional[str] = Query(None, description="Filter by company"),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search by name"),
    db: Session = Depends(get_db),
):
    """List all products with optional filtering."""
    query = db.query(Product)

    if company_id:
        query = query.filter(Product.company_id == company_id)

    if category:
        query = query.filter(Product.category == category)

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/categories")
async def list_categories(
    company_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Get all unique product categories."""
    query = db.query(Product.category).distinct()

    if company_id:
        query = query.filter(Product.company_id == company_id)

    categories = [row[0] for row in query.all() if row[0]]
    return {"categories": sorted(categories)}


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str,
    db: Session = Depends(get_db),
):
    """Get a product by ID."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
):
    """Delete a product."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}
