"""Contact model for storing contact information."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Contact(Base):
    """Contact information extracted from leaflets."""

    __tablename__ = "contacts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Contact details
    contact_type = Column(String(100), nullable=False)  # email, phone, address, website, social
    value = Column(Text, nullable=False)
    context = Column(String(500))  # e.g., "Sales", "Support", "Headquarters"

    # Metadata
    source_images = Column(JSON, default=list)
    confidence = Column(String(20), default="Medium")

    # Relationships
    company = relationship("Company", back_populates="contacts")

    def __repr__(self):
        return f"<Contact(id={self.id}, type={self.contact_type})>"
