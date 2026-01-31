"""Product schemas for API validation."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """Base product schema with common fields."""
    name: str = Field(..., description="Product name")
    product_code: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    description: Optional[str] = None
    key_specs: dict[str, str] = Field(default_factory=dict)
    formats_variants: list[str] = Field(default_factory=list)
    ingredients: list[str] = Field(default_factory=list)
    claims: list[str] = Field(default_factory=list)
    applications: list[str] = Field(default_factory=list)
    target_customers: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    packaging: Optional[str] = None
    storage_shelf_life: Optional[str] = None
    origin: Optional[str] = None
    regulatory_notes: Optional[str] = None
    ordering_info: Optional[str] = None


class ProductCreate(ProductBase):
    """Schema for creating a product."""
    company_id: str
    search_tags: dict[str, list[str]] = Field(default_factory=dict)
    source_images: list[str] = Field(default_factory=list)
    confidence: str = "Medium"


class ProductResponse(ProductCreate):
    """Schema for product API responses."""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductCard(BaseModel):
    """Website-ready product card for display."""
    id: str
    name: str
    category: Optional[str] = None
    subcategory: Optional[str] = None
    short_description: str = ""
    key_specs: dict[str, str] = Field(default_factory=dict)
    formats: list[str] = Field(default_factory=list)
    claims: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    confidence: str = "Medium"


class ProductCatalogue(BaseModel):
    """Grouped product catalogue for website section."""
    company_id: str
    company_name: str
    categories: dict[str, list[ProductCard]] = Field(default_factory=dict)
    total_products: int = 0
