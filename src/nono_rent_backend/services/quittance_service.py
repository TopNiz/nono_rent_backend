from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from uuid import UUID
from nono_rent_backend.models.quittance import Quittance
from nono_rent_backend.models.lease import Lease
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
        statement = (
            select(Quittance)
            .where(Quittance.id == quittance_id)
            .options(
                joinedload(Quittance.lease).joinedload(Lease.tenant),
                joinedload(Quittance.lease).joinedload(Lease.property),
            )
        )
        quittance = session.exec(statement).first()
        if not quittance:
            raise ValueError("Quittance not found")

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Title
        title = Paragraph("Quittance de Loyer", styles["Title"])
        story.append(title)
        story.append(Spacer(1, 12))

        # Quittance details in French
        details = f"""
        Locataire: {quittance.lease.tenant.first_name} {quittance.lease.tenant.last_name}<br/>
        Propriété: {quittance.lease.property.address}<br/>
        Période: {quittance.period_month}/{quittance.period_year}<br/>
        Montant du loyer: {quittance.rent_amount} €<br/>
        Charges: {quittance.charges_amount} €<br/>
        Total: {quittance.total_amount} €<br/>
        Date de paiement: {quittance.payment_date}<br/>
        Statut: {quittance.status.value}
        """
        para = Paragraph(details, styles["Normal"])
        story.append(para)

        doc.build(story)
        buffer.seek(0)
        return buffer
