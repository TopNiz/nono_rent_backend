from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel
from nono_rent_backend.models.landlord import Landlord
from nono_rent_backend.database import get_session
from nono_rent_backend.services.landlord_service import LandlordService


class LandlordCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str


class LandlordUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None


router = APIRouter(prefix="/landlords", tags=["landlords"])


@router.post("/", response_model=Landlord)
def create_landlord(
    landlord_data: LandlordCreate, session: Session = Depends(get_session)
):
    return LandlordService.create_landlord(session, landlord_data.model_dump())


@router.get("/", response_model=list[Landlord])
def read_landlords(session: Session = Depends(get_session)):
    return LandlordService.get_all_landlords(session)


@router.get("/{landlord_id}", response_model=Landlord)
def read_landlord(landlord_id: int, session: Session = Depends(get_session)):
    landlord = LandlordService.get_landlord_by_id(session, landlord_id)
    if not landlord:
        raise HTTPException(status_code=404, detail="Landlord not found")
    return landlord


@router.put("/{landlord_id}", response_model=Landlord)
def update_landlord(
    landlord_id: int,
    landlord_update: LandlordUpdate,
    session: Session = Depends(get_session),
):
    landlord = LandlordService.update_landlord(
        session, landlord_id, landlord_update.model_dump(exclude_unset=True)
    )
    if not landlord:
        raise HTTPException(status_code=404, detail="Landlord not found")
    return landlord


@router.delete("/{landlord_id}")
def delete_landlord(landlord_id: int, session: Session = Depends(get_session)):
    if not LandlordService.delete_landlord(session, landlord_id):
        raise HTTPException(status_code=404, detail="Landlord not found")
    return {"ok": True}
