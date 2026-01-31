"""API route definitions."""
from fastapi import APIRouter

from app.api import ingestion, companies, products, export

router = APIRouter()

router.include_router(ingestion.router, prefix="/ingestion", tags=["ingestion"])
router.include_router(companies.router, prefix="/companies", tags=["companies"])
router.include_router(products.router, prefix="/products", tags=["products"])
router.include_router(export.router, prefix="/export", tags=["export"])
