"""Ingestion session and image models for tracking document processing."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, JSON, ForeignKey, Integer, Enum
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class IngestionStatus(str, enum.Enum):
    """Status of an ingestion session."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class IngestionSession(Base):
    """Tracks a single ingestion event (multiple images as one bundle)."""

    __tablename__ = "ingestion_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    # Status
    status = Column(String(20), default=IngestionStatus.PENDING.value)
    error_message = Column(Text)

    # Processing metadata
    total_images = Column(Integer, default=0)
    processed_images = Column(Integer, default=0)

    # Raw AI response (for debugging/audit)
    raw_response = Column(Text)

    # Data quality report
    quality_report = Column(JSON, default=dict)  # Missing info, unclear specs, etc.

    # Image-to-data traceability map
    traceability_map = Column(JSON, default=dict)  # {image_id: [extracted_elements]}

    # Relationships
    company = relationship("Company", back_populates="ingestion_sessions")
    images = relationship("IngestionImage", back_populates="session", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<IngestionSession(id={self.id}, status={self.status})>"


class IngestionImage(Base):
    """Individual image uploaded as part of an ingestion session."""

    __tablename__ = "ingestion_images"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("ingestion_sessions.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Image metadata
    filename = Column(String(500))
    content_type = Column(String(100))
    file_size = Column(Integer)
    image_order = Column(Integer)  # Order in the bundle

    # Storage
    storage_path = Column(String(1000))  # Path to stored image
    base64_data = Column(Text)  # Or base64 for processing

    # Extracted data summary
    extracted_elements = Column(JSON, default=list)  # What was found in this image

    # Relationships
    session = relationship("IngestionSession", back_populates="images")

    def __repr__(self):
        return f"<IngestionImage(id={self.id}, filename={self.filename})>"
