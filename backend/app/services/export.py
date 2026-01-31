"""Export service for generating CSV outputs."""
import csv
import io
import json
from typing import Optional

from sqlalchemy.orm import Session

from app.models import Company, Product, Claim, Contact
from app.schemas.export import CSVExportResponse


class ExportService:
    """Service for exporting data to CSV format."""

    def __init__(self, db: Session):
        """Initialize export service."""
        self.db = db

    def _list_to_pipe_string(self, items: list) -> str:
        """Convert list to pipe-separated string."""
        if not items:
            return ""
        return " | ".join(str(item) for item in items)

    def _dict_to_json_string(self, data: dict) -> str:
        """Convert dict to JSON string."""
        if not data:
            return ""
        return json.dumps(data, ensure_ascii=False)

    def export_company_profile(self, company_id: Optional[str] = None) -> CSVExportResponse:
        """Export company profile(s) to CSV."""
        query = self.db.query(Company)
        if company_id:
            query = query.filter(Company.id == company_id)

        companies = query.all()

        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        headers = [
            "company_name_printed", "company_name_english", "legal_entity",
            "brand_names", "tagline", "description", "business_type",
            "capabilities", "industries_served", "markets_served",
            "certifications", "key_differentiators", "addresses",
            "phones", "emails", "websites", "social_links", "moq",
            "lead_time", "packaging_options", "notable_numbers", "notes",
            "source_images", "confidence"
        ]
        writer.writerow(headers)

        # Write data rows
        for company in companies:
            row = [
                company.name_printed or "",
                company.name_english or "",
                company.legal_entity or "",
                self._list_to_pipe_string(company.brand_names or []),
                company.tagline or "",
                company.description or "",
                company.business_type or "",
                self._list_to_pipe_string(company.capabilities or []),
                self._list_to_pipe_string(company.industries_served or []),
                self._list_to_pipe_string(company.markets_served or []),
                self._list_to_pipe_string(company.certifications or []),
                self._list_to_pipe_string(company.key_differentiators or []),
                self._list_to_pipe_string(company.addresses or []),
                self._list_to_pipe_string(company.phones or []),
                self._list_to_pipe_string(company.emails or []),
                self._list_to_pipe_string(company.websites or []),
                self._dict_to_json_string(company.social_links or {}),
                company.moq or "",
                company.lead_time or "",
                self._list_to_pipe_string(company.packaging_options or []),
                self._dict_to_json_string(company.notable_numbers or {}),
                company.notes or "",
                self._list_to_pipe_string(company.source_images or []),
                company.confidence or "Medium",
            ]
            writer.writerow(row)

        return CSVExportResponse(
            filename="Company_Profile.csv",
            data=output.getvalue(),
        )

    def export_products(self, company_id: Optional[str] = None) -> CSVExportResponse:
        """Export products to CSV."""
        query = self.db.query(Product).join(Company)
        if company_id:
            query = query.filter(Product.company_id == company_id)

        products = query.all()

        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        headers = [
            "company_name", "product_name", "product_code", "category",
            "subcategory", "description", "key_specs", "formats_variants",
            "ingredients", "claims", "applications", "target_customers",
            "certifications", "packaging", "storage_shelf_life", "origin",
            "regulatory_notes", "ordering_info", "search_tags",
            "source_images", "confidence"
        ]
        writer.writerow(headers)

        # Write data rows
        for product in products:
            row = [
                product.company.name_printed if product.company else "",
                product.name or "",
                product.product_code or "",
                product.category or "",
                product.subcategory or "",
                product.description or "",
                self._dict_to_json_string(product.key_specs or {}),
                self._list_to_pipe_string(product.formats_variants or []),
                self._list_to_pipe_string(product.ingredients or []),
                self._list_to_pipe_string(product.claims or []),
                self._list_to_pipe_string(product.applications or []),
                self._list_to_pipe_string(product.target_customers or []),
                self._list_to_pipe_string(product.certifications or []),
                product.packaging or "",
                product.storage_shelf_life or "",
                product.origin or "",
                product.regulatory_notes or "",
                product.ordering_info or "",
                self._dict_to_json_string(product.search_tags or {}),
                self._list_to_pipe_string(product.source_images or []),
                product.confidence or "Medium",
            ]
            writer.writerow(row)

        return CSVExportResponse(
            filename="Products.csv",
            data=output.getvalue(),
        )

    def export_claims(self, company_id: Optional[str] = None) -> CSVExportResponse:
        """Export claims and certifications to CSV."""
        query = self.db.query(Claim)
        if company_id:
            query = query.filter(Claim.company_id == company_id)

        claims = query.all()

        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        headers = [
            "scope", "item_name", "claim_or_cert_type", "claim_text",
            "standard_or_authority", "source_images", "confidence"
        ]
        writer.writerow(headers)

        # Write data rows
        for claim in claims:
            row = [
                claim.scope or "",
                claim.item_name or "",
                claim.claim_or_cert_type or "",
                claim.claim_text or "",
                claim.standard_or_authority or "",
                self._list_to_pipe_string(claim.source_images or []),
                claim.confidence or "Medium",
            ]
            writer.writerow(row)

        return CSVExportResponse(
            filename="Claims_and_Certifications.csv",
            data=output.getvalue(),
        )

    def export_contacts(self, company_id: Optional[str] = None) -> CSVExportResponse:
        """Export contacts to CSV."""
        query = self.db.query(Contact).join(Company)
        if company_id:
            query = query.filter(Contact.company_id == company_id)

        contacts = query.all()

        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        headers = [
            "company_name", "contact_type", "value", "context",
            "source_images", "confidence"
        ]
        writer.writerow(headers)

        # Write data rows
        for contact in contacts:
            row = [
                contact.company.name_printed if contact.company else "",
                contact.contact_type or "",
                contact.value or "",
                contact.context or "",
                self._list_to_pipe_string(contact.source_images or []),
                contact.confidence or "Medium",
            ]
            writer.writerow(row)

        return CSVExportResponse(
            filename="Contacts.csv",
            data=output.getvalue(),
        )

    def export_all(self, company_id: Optional[str] = None) -> dict[str, CSVExportResponse]:
        """Export all data types to CSV."""
        return {
            "company_profile": self.export_company_profile(company_id),
            "products": self.export_products(company_id),
            "claims": self.export_claims(company_id),
            "contacts": self.export_contacts(company_id),
        }
