from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from uuid import UUID
from nono_rent_backend.models.quittance import Quittance
from nono_rent_backend.models.lease import Lease
from nono_rent_backend.models.property import Property
from typing import List, Optional
from datetime import date
from nono_rent_backend.models.quittance import QuittanceStatus
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from io import BytesIO


class QuittanceService:
    @staticmethod
    def create_quittance(session: Session, quittance_data: dict) -> Quittance:
        quittance = Quittance.model_validate(quittance_data)
        session.add(quittance)
        session.commit()
        session.refresh(quittance)
        return quittance

    @staticmethod
    def get_quittance_by_id(
        session: Session, quittance_id: UUID
    ) -> Optional[Quittance]:
        return session.get(Quittance, quittance_id)

    @staticmethod
    def get_all_quittances(session: Session) -> List[Quittance]:
        return session.exec(select(Quittance)).all()

    @staticmethod
    def update_quittance(
        session: Session, quittance_id: UUID, quittance_update: dict
    ) -> Optional[Quittance]:
        quittance = session.get(Quittance, quittance_id)
        if not quittance:
            return None
        for key, value in quittance_update.items():
            if hasattr(quittance, key):
                setattr(quittance, key, value)
        session.commit()
        session.refresh(quittance)
        return quittance

    @staticmethod
    def delete_quittance(session: Session, quittance_id: UUID) -> bool:
        quittance = session.get(Quittance, quittance_id)
        if not quittance:
            return False
        session.delete(quittance)
        session.commit()
        return True

    @staticmethod
    def export_pdf(session: Session, quittance_id: UUID) -> BytesIO:
        from nono_rent_backend.models.tenant import Tenant
        from nono_rent_backend.models.landlord import Landlord

        quittance = session.get(Quittance, quittance_id)
        if not quittance:
            raise ValueError("Quittance not found")

        lease = session.get(Lease, quittance.lease_id)
        if not lease:
            raise ValueError("Lease not found")

        tenant = session.get(Tenant, lease.tenant_id)
        if not tenant:
            raise ValueError("Tenant not found")

        property = session.get(Property, lease.property_id)
        if not property:
            raise ValueError("Property not found")

        landlord = session.get(Landlord, property.landlord_id)
        if not landlord:
            raise ValueError("Landlord not found")

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Title
        title = Paragraph("Quittance de Loyer", styles["Title"])
        story.append(title)
        story.append(Spacer(1, 12))

        # Landlord
        landlord_text = f"Propriétaire: {landlord.first_name} {landlord.last_name}<br/>{landlord.address}"
        story.append(Paragraph(landlord_text, styles["Normal"]))
        story.append(Spacer(1, 12))

        # Tenant
        tenant_text = (
            f"Locataire: {tenant.first_name} {tenant.last_name}<br/>{tenant.address}"
        )
        story.append(Paragraph(tenant_text, styles["Normal"]))
        story.append(Spacer(1, 12))

        # Property
        property_text = f"Adresse du bien: {property.address}"
        story.append(Paragraph(property_text, styles["Normal"]))
        story.append(Spacer(1, 12))

        # Period
        month_names = [
            "janvier",
            "février",
            "mars",
            "avril",
            "mai",
            "juin",
            "juillet",
            "août",
            "septembre",
            "octobre",
            "novembre",
            "décembre",
        ]
        period_text = f"Période: {month_names[quittance.period_month - 1]} {quittance.period_year}"
        story.append(Paragraph(period_text, styles["Normal"]))
        story.append(Spacer(1, 12))

        # Amounts
        details = f"""
        Montant du loyer: {quittance.rent_amount:.2f} €<br/>
        Charges: {quittance.charges_amount:.2f} €<br/>
        Total: {quittance.total_amount:.2f} €<br/>
        Date de paiement: {quittance.payment_date.strftime("%d/%m/%Y")}<br/>
        """
        para = Paragraph(details, styles["Normal"])
        story.append(para)
        story.append(Spacer(1, 24))

        # Signature
        signature_text = "Signature du propriétaire:"
        story.append(Paragraph(signature_text, styles["Normal"]))
        story.append(Spacer(1, 48))

        doc.build(story)
        buffer.seek(0)
        return buffer
