from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlmodel import Session
from uuid import UUID
from pydantic import BaseModel
from datetime import date
from nono_rent_backend.models.quittance import Quittance, QuittanceStatus
from nono_rent_backend.database import get_session
from nono_rent_backend.services.quittance_service import QuittanceService


class QuittanceCreate(BaseModel):
    lease_id: int
    period_month: int
    period_year: int
    rent_amount: float
    charges_amount: float
    total_amount: float
    payment_date: date
    status: QuittanceStatus = QuittanceStatus.DRAFT


class QuittanceUpdate(BaseModel):
    lease_id: int | None = None
    period_month: int | None = None
    period_year: int | None = None
    rent_amount: float | None = None
    charges_amount: float | None = None
    total_amount: float | None = None
    payment_date: date | None = None
    status: QuittanceStatus | None = None


router = APIRouter(prefix="/quittances", tags=["quittances"])


@router.post("/", response_model=Quittance)
def create_quittance(
    quittance_data: QuittanceCreate, session: Session = Depends(get_session)
):
    return QuittanceService.create_quittance(session, quittance_data.model_dump())


@router.get("/", response_model=list[Quittance])
def read_quittances(session: Session = Depends(get_session)):
    return QuittanceService.get_all_quittances(session)


@router.get("/{quittance_id}", response_model=Quittance)
def read_quittance(quittance_id: UUID, session: Session = Depends(get_session)):
    quittance = QuittanceService.get_quittance_by_id(session, quittance_id)
    if not quittance:
        raise HTTPException(status_code=404, detail="Quittance not found")
    return quittance


@router.put("/{quittance_id}", response_model=Quittance)
def update_quittance(
    quittance_id: UUID,
    quittance_update: QuittanceUpdate,
    session: Session = Depends(get_session),
):
    quittance = QuittanceService.update_quittance(
        session, quittance_id, quittance_update.model_dump(exclude_unset=True)
    )
    if not quittance:
        raise HTTPException(status_code=404, detail="Quittance not found")
    return quittance


@router.delete("/{quittance_id}")
def delete_quittance(quittance_id: UUID, session: Session = Depends(get_session)):
    if not QuittanceService.delete_quittance(session, quittance_id):
        raise HTTPException(status_code=404, detail="Quittance not found")
    return {"ok": True}


@router.get("/{quittance_id}/pdf")
def export_quittance_pdf(quittance_id: UUID, session: Session = Depends(get_session)):
    try:
        pdf_buffer = QuittanceService.export_pdf(session, quittance_id)
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=quittance.pdf"},
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
