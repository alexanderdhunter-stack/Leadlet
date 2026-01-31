"""Ingestion service for processing leaflet images with Claude Vision."""
import json
import logging
from datetime import datetime
from typing import Optional

import anthropic
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import Company, Product, Claim, Contact, IngestionSession, IngestionImage
from app.models.ingestion import IngestionStatus
from app.schemas.ingestion import (
    IngestionRequest,
    IngestionResponse,
    ExtractionResult,
    IngestionStatusEnum,
    ImageData,
)
from app.services.prompts import SYSTEM_PROMPT, EXTRACTION_PROMPT

logger = logging.getLogger(__name__)
settings = get_settings()


class IngestionService:
    """Service for ingesting and processing leaflet images."""

    def __init__(self, db: Session):
        """Initialize the ingestion service."""
        self.db = db
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    async def create_session(self, request: IngestionRequest) -> IngestionSession:
        """Create a new ingestion session."""
        session = IngestionSession(
            status=IngestionStatus.PENDING.value,
            total_images=len(request.images),
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        # Store image metadata
        for idx, img in enumerate(request.images):
            image = IngestionImage(
                session_id=session.id,
                filename=img.filename,
                content_type=img.content_type,
                image_order=img.image_order or idx,
                base64_data=img.base64_data,
            )
            self.db.add(image)

        self.db.commit()
        return session

    def _build_image_content(self, images: list[ImageData]) -> list[dict]:
        """Build the image content blocks for Claude API."""
        content = []

        for idx, img in enumerate(images):
            # Add image identifier text
            content.append({
                "type": "text",
                "text": f"--- Image {idx + 1} (image_{idx + 1}): {img.filename} ---"
            })

            # Determine media type
            media_type = img.content_type
            if media_type not in ["image/jpeg", "image/png", "image/gif", "image/webp"]:
                media_type = "image/jpeg"  # Default fallback

            # Add image block
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": img.base64_data,
                }
            })

        # Add extraction prompt at the end
        content.append({
            "type": "text",
            "text": EXTRACTION_PROMPT
        })

        return content

    def _parse_extraction_response(self, response_text: str) -> ExtractionResult:
        """Parse the Claude response into structured extraction result."""
        # Clean up response - remove any markdown code blocks if present
        cleaned = response_text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Response text: {response_text[:500]}...")
            raise ValueError(f"Failed to parse extraction response: {e}")

        # Build ExtractionResult from parsed data
        return ExtractionResult(
            identity_resolution=data.get("identity_resolution", {}),
            company=data.get("company", {}),
            products=data.get("products", []),
            category_taxonomy=data.get("category_taxonomy", {}),
            search_metadata=data.get("search_metadata", {}),
            claims=data.get("claims", []),
            contacts=data.get("contacts", []),
            traceability_map=data.get("traceability_map", []),
            quality_report=data.get("quality_report", {}),
            retrieval_brief=data.get("retrieval_brief", ""),
        )

    async def process_images(self, session_id: str) -> ExtractionResult:
        """Process images using Claude Vision API."""
        session = self.db.query(IngestionSession).filter(
            IngestionSession.id == session_id
        ).first()

        if not session:
            raise ValueError(f"Session {session_id} not found")

        # Update status to processing
        session.status = IngestionStatus.PROCESSING.value
        self.db.commit()

        try:
            # Get images for this session
            images = self.db.query(IngestionImage).filter(
                IngestionImage.session_id == session_id
            ).order_by(IngestionImage.image_order).all()

            # Convert to ImageData for processing
            image_data = [
                ImageData(
                    filename=img.filename,
                    content_type=img.content_type or "image/jpeg",
                    base64_data=img.base64_data,
                    image_order=img.image_order,
                )
                for img in images
            ]

            # Build content for Claude API
            content = self._build_image_content(image_data)

            # Call Claude API
            logger.info(f"Calling Claude API with {len(images)} images")
            response = self.client.messages.create(
                model=settings.anthropic_model,
                max_tokens=8192,
                system=SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": content}
                ]
            )

            # Extract text response
            response_text = ""
            for block in response.content:
                if block.type == "text":
                    response_text += block.text

            # Store raw response
            session.raw_response = response_text

            # Parse response
            extraction_result = self._parse_extraction_response(response_text)

            # Update image extracted elements from traceability map
            for trace in extraction_result.traceability_map:
                for img in images:
                    if f"image_{img.image_order + 1}" == trace.image_id or img.filename == trace.filename:
                        img.extracted_elements = trace.extracted_elements

            # Store quality report and traceability
            session.quality_report = extraction_result.quality_report.model_dump()
            session.traceability_map = {
                t.image_id: t.extracted_elements for t in extraction_result.traceability_map
            }

            session.processed_images = len(images)
            session.status = IngestionStatus.COMPLETED.value
            session.completed_at = datetime.utcnow()
            self.db.commit()

            return extraction_result

        except Exception as e:
            logger.exception(f"Error processing images: {e}")
            session.status = IngestionStatus.FAILED.value
            session.error_message = str(e)
            self.db.commit()
            raise

    def save_extraction_result(
        self,
        session_id: str,
        result: ExtractionResult,
        existing_company_id: Optional[str] = None
    ) -> Company:
        """Save extraction result to database."""
        session = self.db.query(IngestionSession).filter(
            IngestionSession.id == session_id
        ).first()

        if not session:
            raise ValueError(f"Session {session_id} not found")

        # Check if we should update existing company or create new
        company = None
        if existing_company_id:
            company = self.db.query(Company).filter(
                Company.id == existing_company_id
            ).first()

        if not company:
            # Create new company
            company_data = result.company.model_dump() if hasattr(result.company, 'model_dump') else result.company
            if isinstance(company_data, dict):
                company = Company(**company_data)
            else:
                company = Company(**company_data)
            self.db.add(company)
            self.db.commit()
            self.db.refresh(company)

        # Link session to company
        session.company_id = company.id
        self.db.commit()

        # Save products
        for prod_data in result.products:
            prod_dict = prod_data.model_dump() if hasattr(prod_data, 'model_dump') else prod_data
            if isinstance(prod_dict, dict):
                prod_dict['company_id'] = company.id
                # Remove company_id if it's already there as None
                product = Product(**prod_dict)
            else:
                product = Product(company_id=company.id, **prod_dict)
            self.db.add(product)

        # Save claims
        for claim_data in result.claims:
            claim_dict = claim_data.model_dump() if hasattr(claim_data, 'model_dump') else claim_data
            if isinstance(claim_dict, dict):
                claim_dict['company_id'] = company.id
                claim = Claim(**claim_dict)
            else:
                claim = Claim(company_id=company.id, **claim_dict)
            self.db.add(claim)

        # Save contacts
        for contact_data in result.contacts:
            contact_dict = contact_data.model_dump() if hasattr(contact_data, 'model_dump') else contact_data
            if isinstance(contact_dict, dict):
                contact_dict['company_id'] = company.id
                contact = Contact(**contact_dict)
            else:
                contact = Contact(company_id=company.id, **contact_dict)
            self.db.add(contact)

        self.db.commit()
        self.db.refresh(company)

        return company

    async def ingest(self, request: IngestionRequest) -> IngestionResponse:
        """Main entry point for ingestion workflow."""
        # Create session
        session = await self.create_session(request)

        try:
            # Process images
            extraction_result = await self.process_images(session.id)

            # Save results
            company = self.save_extraction_result(
                session.id,
                extraction_result,
                request.existing_company_id
            )

            return IngestionResponse(
                session_id=session.id,
                status=IngestionStatusEnum.COMPLETED,
                company_id=company.id,
                extraction_result=extraction_result,
            )

        except Exception as e:
            logger.exception(f"Ingestion failed: {e}")
            return IngestionResponse(
                session_id=session.id,
                status=IngestionStatusEnum.FAILED,
                error_message=str(e),
            )

    def get_session_status(self, session_id: str) -> Optional[IngestionSession]:
        """Get the status of an ingestion session."""
        return self.db.query(IngestionSession).filter(
            IngestionSession.id == session_id
        ).first()
