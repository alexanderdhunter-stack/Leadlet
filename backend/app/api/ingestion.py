"""Ingestion API endpoints."""
import base64
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.ingestion import (
    IngestionRequest,
    IngestionResponse,
    IngestionStatus,
    IngestionStatusEnum,
    ImageData,
)
from app.services.ingestion import IngestionService

router = APIRouter()


@router.post("/", response_model=IngestionResponse)
async def ingest_images(
    request: IngestionRequest,
    db: Session = Depends(get_db),
):
    """
    Ingest multiple images as a single document bundle.

    Processes all images together using Claude Vision to extract
    company and product information.
    """
    service = IngestionService(db)
    return await service.ingest(request)


@router.post("/upload", response_model=IngestionResponse)
async def upload_and_ingest(
    files: list[UploadFile] = File(..., description="Images to process"),
    existing_company_id: Optional[str] = Form(None),
    treat_as_single_bundle: bool = Form(True),
    db: Session = Depends(get_db),
):
    """
    Upload and ingest multiple images via form data.

    This endpoint accepts multipart form uploads for easier integration
    with frontend file upload components.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    # Convert uploaded files to ImageData
    images = []
    for idx, file in enumerate(files):
        content = await file.read()
        base64_data = base64.b64encode(content).decode("utf-8")

        images.append(ImageData(
            filename=file.filename or f"image_{idx + 1}",
            content_type=file.content_type or "image/jpeg",
            base64_data=base64_data,
            image_order=idx,
        ))

    # Create request
    request = IngestionRequest(
        images=images,
        treat_as_single_bundle=treat_as_single_bundle,
        existing_company_id=existing_company_id,
    )

    service = IngestionService(db)
    return await service.ingest(request)


@router.get("/status/{session_id}", response_model=IngestionStatus)
async def get_ingestion_status(
    session_id: str,
    db: Session = Depends(get_db),
):
    """Get the status of an ingestion session."""
    service = IngestionService(db)
    session = service.get_session_status(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return IngestionStatus(
        session_id=session.id,
        status=IngestionStatusEnum(session.status),
        total_images=session.total_images,
        processed_images=session.processed_images,
        error_message=session.error_message,
        created_at=session.created_at,
        completed_at=session.completed_at,
    )
