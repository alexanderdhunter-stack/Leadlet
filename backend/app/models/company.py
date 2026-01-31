"""Company model for storing extracted company information."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Company(Base):
    """Company entity extracted from leaflets."""

    __tablename__ = "companies"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Identity
    name_printed = Column(String(500), nullable=False, index=True)
    name_english = Column(String(500))
    legal_entity = Column(String(500))
    brand_names = Column(JSON, default=list)  # List of brand names

    # Overview
    tagline = Column(Text)
    description = Column(Text)
    business_type = Column(String(200))
    capabilities = Column(JSON, default=list)  # List of capabilities
    industries_served = Column(JSON, default=list)
    markets_served = Column(JSON, default=list)

    # Certifications & Differentiators
    certifications = Column(JSON, default=list)
    key_differentiators = Column(JSON, default=list)

    # Contact info (summary)
    addresses = Column(JSON, default=list)
    phones = Column(JSON, default=list)
    emails = Column(JSON, default=list)
    websites = Column(JSON, default=list)
    social_links = Column(JSON, default=dict)

    # Business info
    moq = Column(String(200))  # Minimum order quantity
    lead_time = Column(String(200))
    packaging_options = Column(JSON, default=list)
    notable_numbers = Column(JSON, default=dict)

    # Metadata
    notes = Column(Text)
    source_images = Column(JSON, default=list)
    confidence = Column(String(20), default="Medium")  # High/Medium/Low

    # Search & retrieval metadata
    search_tags = Column(JSON, default=dict)  # {function: [], ingredient: [], industry: [], etc.}

    # Retrieval brief
    retrieval_brief = Column(Text)

    # Relationships
    products = relationship("Product", back_populates="company", cascade="all, delete-orphan")
    claims = relationship("Claim", back_populates="company", cascade="all, delete-orphan")
    contacts = relationship("Contact", back_populates="company", cascade="all, delete-orphan")
    ingestion_sessions = relationship("IngestionSession", back_populates="company")

    def __repr__(self):
        return f"<Company(id={self.id}, name={self.name_printed})>"
