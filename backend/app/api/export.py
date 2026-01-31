"""Export API endpoints."""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.export import CSVExportResponse
from app.services.export import ExportService

router = APIRouter()


@router.get("/company-profile", response_model=CSVExportResponse)
async def export_company_profile(
    company_id: Optional[str] = Query(None, description="Export specific company"),
    db: Session = Depends(get_db),
):
    """Export company profile(s) as CSV."""
    service = ExportService(db)
    return service.export_company_profile(company_id)


@router.get("/company-profile/download")
async def download_company_profile(
    company_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Download company profile CSV as file."""
    service = ExportService(db)
    result = service.export_company_profile(company_id)

    return Response(
        content=result.data,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={result.filename}"
        }
    )


@router.get("/products", response_model=CSVExportResponse)
async def export_products(
    company_id: Optional[str] = Query(None, description="Export specific company"),
    db: Session = Depends(get_db),
):
    """Export products as CSV."""
    service = ExportService(db)
    return service.export_products(company_id)


@router.get("/products/download")
async def download_products(
    company_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Download products CSV as file."""
    service = ExportService(db)
    result = service.export_products(company_id)

    return Response(
        content=result.data,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={result.filename}"
        }
    )


@router.get("/claims", response_model=CSVExportResponse)
async def export_claims(
    company_id: Optional[str] = Query(None, description="Export specific company"),
    db: Session = Depends(get_db),
):
    """Export claims and certifications as CSV."""
    service = ExportService(db)
    return service.export_claims(company_id)


@router.get("/claims/download")
async def download_claims(
    company_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Download claims CSV as file."""
    service = ExportService(db)
    result = service.export_claims(company_id)

    return Response(
        content=result.data,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={result.filename}"
        }
    )


@router.get("/contacts", response_model=CSVExportResponse)
async def export_contacts(
    company_id: Optional[str] = Query(None, description="Export specific company"),
    db: Session = Depends(get_db),
):
    """Export contacts as CSV."""
    service = ExportService(db)
    return service.export_contacts(company_id)


@router.get("/contacts/download")
async def download_contacts(
    company_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Download contacts CSV as file."""
    service = ExportService(db)
    result = service.export_contacts(company_id)

    return Response(
        content=result.data,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={result.filename}"
        }
    )


@router.get("/all")
async def export_all(
    company_id: Optional[str] = Query(None, description="Export specific company"),
    db: Session = Depends(get_db),
):
    """Export all data types as a dictionary of CSVs."""
    service = ExportService(db)
    return service.export_all(company_id)
