"""Company API endpoints."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Company, Product
from app.schemas.company import CompanyResponse, CompanyOverview
from app.schemas.product import ProductCatalogue, ProductCard

router = APIRouter()


@router.get("/", response_model=list[CompanyResponse])
async def list_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    search: Optional[str] = Query(None, description="Search by name"),
    industry: Optional[str] = Query(None, description="Filter by industry"),
    db: Session = Depends(get_db),
):
    """List all companies with optional filtering."""
    query = db.query(Company)

    if search:
        query = query.filter(
            Company.name_printed.ilike(f"%{search}%") |
            Company.name_english.ilike(f"%{search}%")
        )

    if industry:
        # Filter by industry in JSON array
        query = query.filter(Company.industries_served.contains([industry]))

    companies = query.offset(skip).limit(limit).all()
    return companies


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: str,
    db: Session = Depends(get_db),
):
    """Get a company by ID."""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.get("/{company_id}/overview", response_model=CompanyOverview)
async def get_company_overview(
    company_id: str,
    db: Session = Depends(get_db),
):
    """Get website-ready company overview."""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # Build contact summary
    contact_summary = {}
    if company.emails:
        contact_summary["email"] = company.emails[0] if company.emails else None
    if company.phones:
        contact_summary["phone"] = company.phones[0] if company.phones else None
    if company.websites:
        contact_summary["website"] = company.websites[0] if company.websites else None

    return CompanyOverview(
        company_name=company.name_printed,
        tagline=company.tagline,
        short_description=company.description or "",
        business_type=company.business_type,
        core_capabilities=company.capabilities or [],
        industries_served=company.industries_served or [],
        markets_regions=company.markets_served or [],
        certifications=company.certifications or [],
        key_differentiators=company.key_differentiators or [],
        contact_summary=contact_summary,
    )


@router.get("/{company_id}/catalogue", response_model=ProductCatalogue)
async def get_product_catalogue(
    company_id: str,
    db: Session = Depends(get_db),
):
    """Get website-ready product catalogue grouped by category."""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    products = db.query(Product).filter(Product.company_id == company_id).all()

    # Group by category
    categories: dict[str, list[ProductCard]] = {}
    for product in products:
        category = product.category or "Uncategorized"
        if category not in categories:
            categories[category] = []

        categories[category].append(ProductCard(
            id=product.id,
            name=product.name,
            category=product.category,
            subcategory=product.subcategory,
            short_description=product.description or "",
            key_specs=product.key_specs or {},
            formats=product.formats_variants or [],
            claims=product.claims or [],
            certifications=product.certifications or [],
            confidence=product.confidence or "Medium",
        ))

    return ProductCatalogue(
        company_id=company.id,
        company_name=company.name_printed,
        categories=categories,
        total_products=len(products),
    )


@router.delete("/{company_id}")
async def delete_company(
    company_id: str,
    db: Session = Depends(get_db),
):
    """Delete a company and all associated data."""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    db.delete(company)
    db.commit()

    return {"message": "Company deleted successfully"}
