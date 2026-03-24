from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from uuid import UUID
from pydantic import BaseModel
from datetime import date
from nono_rent_backend.models.quittance import Quittance, QuittanceStatus
from nono_rent_backend.database import get_session


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
    quittance = Quittance(**quittance_data.model_dump())
    session.add(quittance)
    session.commit()
    session.refresh(quittance)
    return quittance


@router.get("/", response_model=list[Quittance])
def read_quittances(session: Session = Depends(get_session)):
    return session.exec(select(Quittance)).all()


@router.get("/{quittance_id}", response_model=Quittance)
def read_quittance(quittance_id: UUID, session: Session = Depends(get_session)):
    quittance = session.get(Quittance, quittance_id)
    if not quittance:
        raise HTTPException(status_code=404, detail="Quittance not found")
    return quittance


@router.put("/{quittance_id}", response_model=Quittance)
def update_quittance(
    quittance_id: UUID,
    quittance_update: QuittanceUpdate,
    session: Session = Depends(get_session),
):
    quittance = session.get(Quittance, quittance_id)
    if not quittance:
        raise HTTPException(status_code=404, detail="Quittance not found")
    for key, value in quittance_update.model_dump(exclude_unset=True).items():
        setattr(quittance, key, value)
    session.commit()
    session.refresh(quittance)
    return quittance


@router.delete("/{quittance_id}")
def delete_quittance(quittance_id: UUID, session: Session = Depends(get_session)):
    quittance = session.get(Quittance, quittance_id)
    if not quittance:
        raise HTTPException(status_code=404, detail="Quittance not found")
    session.delete(quittance)
    session.commit()
    return {"ok": True}
