"""Ingestion schemas for API validation."""
from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field
from enum import Enum

from app.schemas.company import CompanyCreate, IdentityResolution, CategoryTaxonomy
from app.schemas.product import ProductCreate


class IngestionStatusEnum(str, Enum):
    """Status of an ingestion session."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ImageData(BaseModel):
    """Image data for processing."""
    filename: str
    content_type: str
    base64_data: str
    image_order: int = 0


class IngestionRequest(BaseModel):
    """Request to ingest multiple images as a document bundle."""
    images: list[ImageData] = Field(..., min_length=1, description="List of images to process")
    treat_as_single_bundle: bool = Field(True, description="Treat all images as one document")
    existing_company_id: Optional[str] = Field(None, description="Link to existing company if known")


class ClaimExtracted(BaseModel):
    """Extracted claim or certification."""
    scope: str  # "company" or "product"
    item_name: str
    claim_or_cert_type: str
    claim_text: str
    standard_or_authority: Optional[str] = None
    source_images: list[str] = Field(default_factory=list)
    confidence: str = "Medium"


class ContactExtracted(BaseModel):
    """Extracted contact information."""
    contact_type: str  # email, phone, address, website, social
    value: str
    context: Optional[str] = None
    source_images: list[str] = Field(default_factory=list)
    confidence: str = "Medium"


class DataQualityReport(BaseModel):
    """Data quality and gap report."""
    missing_expected_info: list[str] = Field(default_factory=list)
    unclear_items: list[str] = Field(default_factory=list)
    cut_off_pages: list[str] = Field(default_factory=list)
    suspected_ocr_errors: list[str] = Field(default_factory=list)


class TraceabilityEntry(BaseModel):
    """Maps image to extracted elements."""
    image_id: str
    filename: str
    extracted_elements: list[str] = Field(default_factory=list)


class SearchMetadata(BaseModel):
    """Search and retrieval metadata."""
    function_tags: list[str] = Field(default_factory=list)
    ingredient_source_tags: list[str] = Field(default_factory=list)
    industry_tags: list[str] = Field(default_factory=list)
    claims_compliance_tags: list[str] = Field(default_factory=list)
    format_tags: list[str] = Field(default_factory=list)
    region_language_tags: list[str] = Field(default_factory=list)


class ExtractionResult(BaseModel):
    """Complete extraction result from image processing."""
    # 1. Identity Resolution
    identity_resolution: IdentityResolution

    # 2. Website-ready structured output
    company: CompanyCreate
    products: list[ProductCreate] = Field(default_factory=list)
    category_taxonomy: CategoryTaxonomy = Field(default_factory=CategoryTaxonomy)
    search_metadata: SearchMetadata = Field(default_factory=SearchMetadata)

    # 3. Additional extractions
    claims: list[ClaimExtracted] = Field(default_factory=list)
    contacts: list[ContactExtracted] = Field(default_factory=list)

    # 4. Traceability
    traceability_map: list[TraceabilityEntry] = Field(default_factory=list)

    # 5. Quality report
    quality_report: DataQualityReport = Field(default_factory=DataQualityReport)

    # 6. Retrieval brief
    retrieval_brief: str = ""


class IngestionStatus(BaseModel):
    """Status response for an ingestion session."""
    session_id: str
    status: IngestionStatusEnum
    total_images: int
    processed_images: int
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None


class IngestionResponse(BaseModel):
    """Response from a completed ingestion."""
    session_id: str
    status: IngestionStatusEnum
    company_id: Optional[str] = None
    extraction_result: Optional[ExtractionResult] = None
    error_message: Optional[str] = None

    class Config:
        from_attributes = True
