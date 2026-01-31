"""Product model for storing extracted product information."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Product(Base):
    """Product entity extracted from leaflets."""

    __tablename__ = "products"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Identity
    name = Column(String(500), nullable=False, index=True)
    product_code = Column(String(200))

    # Categorization
    category = Column(String(200), index=True)
    subcategory = Column(String(200))

    # Description
    description = Column(Text)
    key_specs = Column(JSON, default=dict)  # Key specifications as key-value pairs

    # Variants & formats
    formats_variants = Column(JSON, default=list)
    ingredients = Column(JSON, default=list)

    # Claims & applications
    claims = Column(JSON, default=list)
    applications = Column(JSON, default=list)
    target_customers = Column(JSON, default=list)

    # Compliance
    certifications = Column(JSON, default=list)

    # Packaging & logistics
    packaging = Column(Text)
    storage_shelf_life = Column(String(200))
    origin = Column(String(200))
    regulatory_notes = Column(Text)

    # Ordering
    ordering_info = Column(Text)

    # Metadata
    search_tags = Column(JSON, default=dict)  # {function: [], ingredient: [], format: [], etc.}
    source_images = Column(JSON, default=list)
    confidence = Column(String(20), default="Medium")  # High/Medium/Low

    # Relationships
    company = relationship("Company", back_populates="products")

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name})>"
