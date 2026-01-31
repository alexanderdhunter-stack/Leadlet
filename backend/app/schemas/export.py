"""Export schemas for CSV generation."""
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class ExportFormat(str, Enum):
    """Supported export formats."""
    CSV = "csv"
    JSON = "json"


class CSVExportRequest(BaseModel):
    """Request to export data as CSV."""
    company_id: Optional[str] = Field(None, description="Export specific company")
    export_type: str = Field(..., description="Type: company_profile, products, claims, contacts, all")
    include_headers: bool = True


class CSVExportResponse(BaseModel):
    """Response with CSV data."""
    filename: str
    content_type: str = "text/csv"
    data: str  # CSV string


class CompanyProfileCSV(BaseModel):
    """CSV row schema for company profile export."""
    company_name_printed: str
    company_name_english: str = ""
    legal_entity: str = ""
    brand_names: str = ""  # Pipe-separated
    tagline: str = ""
    description: str = ""
    business_type: str = ""
    capabilities: str = ""  # Pipe-separated
    industries_served: str = ""  # Pipe-separated
    markets_served: str = ""  # Pipe-separated
    certifications: str = ""  # Pipe-separated
    key_differentiators: str = ""  # Pipe-separated
    addresses: str = ""  # Pipe-separated
    phones: str = ""  # Pipe-separated
    emails: str = ""  # Pipe-separated
    websites: str = ""  # Pipe-separated
    social_links: str = ""  # JSON string
    moq: str = ""
    lead_time: str = ""
    packaging_options: str = ""  # Pipe-separated
    notable_numbers: str = ""  # JSON string
    notes: str = ""
    source_images: str = ""  # Pipe-separated
    confidence: str = "Medium"


class ProductCSV(BaseModel):
    """CSV row schema for product export."""
    company_name: str
    product_name: str
    product_code: str = ""
    category: str = ""
    subcategory: str = ""
    description: str = ""
    key_specs: str = ""  # JSON string
    formats_variants: str = ""  # Pipe-separated
    ingredients: str = ""  # Pipe-separated
    claims: str = ""  # Pipe-separated
    applications: str = ""  # Pipe-separated
    target_customers: str = ""  # Pipe-separated
    certifications: str = ""  # Pipe-separated
    packaging: str = ""
    storage_shelf_life: str = ""
    origin: str = ""
    regulatory_notes: str = ""
    ordering_info: str = ""
    search_tags: str = ""  # JSON string
    source_images: str = ""  # Pipe-separated
    confidence: str = "Medium"


class ClaimCSV(BaseModel):
    """CSV row schema for claims export."""
    scope: str  # company or product
    item_name: str
    claim_or_cert_type: str
    claim_text: str
    standard_or_authority: str = ""
    source_images: str = ""  # Pipe-separated
    confidence: str = "Medium"


class ContactCSV(BaseModel):
    """CSV row schema for contact export."""
    company_name: str
    contact_type: str
    value: str
    context: str = ""
    source_images: str = ""  # Pipe-separated
    confidence: str = "Medium"
