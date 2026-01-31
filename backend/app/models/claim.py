"""Claim and certification model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Claim(Base):
    """Claims and certifications extracted from leaflets."""

    __tablename__ = "claims"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Scope
    scope = Column(String(50), nullable=False)  # "company" or "product"
    item_name = Column(String(500))  # Company name or product name

    # Claim details
    claim_or_cert_type = Column(String(200), nullable=False)  # e.g., "certification", "claim", "award"
    claim_text = Column(Text, nullable=False)
    standard_or_authority = Column(String(500))  # e.g., "ISO", "USDA", "FDA"

    # Metadata
    source_images = Column(JSON, default=list)
    confidence = Column(String(20), default="Medium")

    # Relationships
    company = relationship("Company", back_populates="claims")

    def __repr__(self):
        return f"<Claim(id={self.id}, type={self.claim_or_cert_type})>"
