from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from uuid import UUID
from pydantic import BaseModel
from datetime import date
from nono_rent_backend.models.lease import Lease, LeaseType
from nono_rent_backend.database import get_session
from nono_rent_backend.services.lease_service import LeaseService


class LeaseCreate(BaseModel):
    tenant_id: int
    property_id: int
    start_date: date
    end_date: date
    rent_amount: float
    charges: float
    deposit: float
    lease_type: LeaseType


class LeaseUpdate(BaseModel):
    tenant_id: int | None = None
    property_id: int | None = None
    start_date: date | None = None
    end_date: date | None = None
    rent_amount: float | None = None
    charges: float | None = None
    deposit: float | None = None
    lease_type: LeaseType | None = None


router = APIRouter(prefix="/leases", tags=["leases"])


@router.post("/", response_model=Lease)
def create_lease(lease_data: LeaseCreate, session: Session = Depends(get_session)):
    return LeaseService.create_lease(session, lease_data.model_dump())


@router.get("/", response_model=list[Lease])
def read_leases(session: Session = Depends(get_session)):
    return LeaseService.get_all_leases(session)


@router.get("/{lease_id}", response_model=Lease)
def read_lease(lease_id: UUID, session: Session = Depends(get_session)):
    lease = LeaseService.get_lease_by_id(session, lease_id)
    if not lease:
        raise HTTPException(status_code=404, detail="Lease not found")
    return lease


@router.put("/{lease_id}", response_model=Lease)
def update_lease(
    lease_id: UUID, lease_update: LeaseUpdate, session: Session = Depends(get_session)
):
    lease = LeaseService.update_lease(
        session, lease_id, lease_update.model_dump(exclude_unset=True)
    )
    if not lease:
        raise HTTPException(status_code=404, detail="Lease not found")
    return lease


@router.delete("/{lease_id}")
def delete_lease(lease_id: UUID, session: Session = Depends(get_session)):
    if not LeaseService.delete_lease(session, lease_id):
        raise HTTPException(status_code=404, detail="Lease not found")
    return {"ok": True}
