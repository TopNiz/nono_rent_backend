from sqlmodel import Field, SQLModel
from pydantic import field_validator
from enum import Enum
from datetime import date
from uuid import UUID, uuid4
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch


class QuittanceStatus(str, Enum):
    DRAFT = "draft"
    GENERATED = "generated"


class Quittance(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    lease_id: int = Field(foreign_key="lease.id")
    period_month: int
    period_year: int
    rent_amount: float
    charges_amount: float
    total_amount: float
    payment_date: date
    status: QuittanceStatus = QuittanceStatus.DRAFT

    @field_validator("period_month")
    @classmethod
    def validate_month(cls, v):
        if not (1 <= v <= 12):
            raise ValueError("Month must be between 1 and 12")
        return v

    @field_validator("period_year")
    @classmethod
    def validate_year(cls, v):
        if v < 1900 or v > 2100:
            raise ValueError("Invalid year")
        return v

    @field_validator("rent_amount", "charges_amount", "total_amount")
    @classmethod
    def validate_positive_amounts(cls, v):
        if v < 0:
            raise ValueError("Amount must be positive")
        return v

    def generate_pdf(self, filepath: str):
        """Generate PDF quittance in French."""
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Title
        title = Paragraph("QUITTANCE DE LOYER", styles["Title"])
        story.append(title)
        story.append(Spacer(1, 0.5 * inch))

        # Period
        month_names = [
            "Janvier",
            "Février",
            "Mars",
            "Avril",
            "Mai",
            "Juin",
            "Juillet",
            "Août",
            "Septembre",
            "Octobre",
            "Novembre",
            "Décembre",
        ]
        period_text = (
            f"Période: {month_names[self.period_month - 1]} {self.period_year}"
        )
        story.append(Paragraph(period_text, styles["Normal"]))
        story.append(Spacer(1, 0.25 * inch))

        # Amounts
        rent_text = f"Loyer: {self.rent_amount:.2f} €"
        charges_text = f"Charges: {self.charges_amount:.2f} €"
        total_text = f"Total: {self.total_amount:.2f} €"
        story.append(Paragraph(rent_text, styles["Normal"]))
        story.append(Paragraph(charges_text, styles["Normal"]))
        story.append(Paragraph(total_text, styles["Normal"]))
        story.append(Spacer(1, 0.25 * inch))

        # Payment date
        payment_text = f"Date de paiement: {self.payment_date.strftime('%d/%m/%Y')}"
        story.append(Paragraph(payment_text, styles["Normal"]))
        story.append(Spacer(1, 0.5 * inch))

        # Signature space
        signature_text = "Signature du propriétaire:"
        story.append(Paragraph(signature_text, styles["Normal"]))
        story.append(Spacer(1, 1 * inch))

        doc.build(story)
        self.status = QuittanceStatus.GENERATED
