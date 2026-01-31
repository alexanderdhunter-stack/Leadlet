"""Company schemas for API validation."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CompanyBase(BaseModel):
    """Base company schema with common fields."""
    name_printed: str = Field(..., description="Company name as printed on documents")
    name_english: Optional[str] = Field(None, description="English translation of company name")
    legal_entity: Optional[str] = Field(None, description="Legal entity name if different from brand")
    brand_names: list[str] = Field(default_factory=list, description="Associated brand names")
    tagline: Optional[str] = None
    description: Optional[str] = None
    business_type: Optional[str] = None
    capabilities: list[str] = Field(default_factory=list)
    industries_served: list[str] = Field(default_factory=list)
    markets_served: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    key_differentiators: list[str] = Field(default_factory=list)


class CompanyCreate(CompanyBase):
    """Schema for creating a company."""
    addresses: list[str] = Field(default_factory=list)
    phones: list[str] = Field(default_factory=list)
    emails: list[str] = Field(default_factory=list)
    websites: list[str] = Field(default_factory=list)
    social_links: dict[str, str] = Field(default_factory=dict)
    moq: Optional[str] = None
    lead_time: Optional[str] = None
    packaging_options: list[str] = Field(default_factory=list)
    notable_numbers: dict[str, str] = Field(default_factory=dict)
    notes: Optional[str] = None
    source_images: list[str] = Field(default_factory=list)
    confidence: str = "Medium"
    search_tags: dict[str, list[str]] = Field(default_factory=dict)
    retrieval_brief: Optional[str] = None


class CompanyResponse(CompanyCreate):
    """Schema for company API responses."""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CompanyOverview(BaseModel):
    """Website-ready company overview for display."""
    company_name: str
    tagline: Optional[str] = None
    short_description: str
    business_type: Optional[str] = None
    core_capabilities: list[str] = Field(default_factory=list)
    industries_served: list[str] = Field(default_factory=list)
    markets_regions: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    key_differentiators: list[str] = Field(default_factory=list)
    contact_summary: dict[str, str] = Field(default_factory=dict)


class IdentityResolution(BaseModel):
    """Document-level identity resolution result."""
    primary_company_name: str
    english_name: Optional[str] = None
    brand_vs_legal_entity: Optional[str] = None
    evidence_images: list[str] = Field(default_factory=list)
    is_ambiguous: bool = False
    primary_assumption: Optional[str] = None
    alternatives: list[str] = Field(default_factory=list)
    confirming_evidence_needed: Optional[str] = None


class CategoryTaxonomy(BaseModel):
    """Site-wide category taxonomy."""
    top_level_categories: list[str] = Field(default_factory=list, max_length=12)
    subcategories: dict[str, list[str]] = Field(default_factory=dict)
    rationale: str = ""
