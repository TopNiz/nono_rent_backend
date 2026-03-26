from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel
from nono_rent_backend.models.property import Property, PropertyType
from nono_rent_backend.database import get_session
from nono_rent_backend.services.property_service import PropertyService


class PropertyCreate(BaseModel):
    address: str
    type: PropertyType
    landlord_id: int


class PropertyUpdate(BaseModel):
    address: str | None = None
    type: PropertyType | None = None
    landlord_id: int | None = None


router = APIRouter(prefix="/properties", tags=["properties"])


@router.post("/", response_model=Property)
def create_property(
    property_data: PropertyCreate, session: Session = Depends(get_session)
):
    return PropertyService.create_property(session, property_data.model_dump())


@router.get("/", response_model=list[Property])
def read_properties(session: Session = Depends(get_session)):
    return PropertyService.get_all_properties(session)


@router.get("/{property_id}", response_model=Property)
def read_property(property_id: int, session: Session = Depends(get_session)):
    property = PropertyService.get_property_by_id(session, property_id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property


@router.put("/{property_id}", response_model=Property)
def update_property(
    property_id: int,
    property_update: PropertyUpdate,
    session: Session = Depends(get_session),
):
    property = PropertyService.update_property(
        session, property_id, property_update.model_dump(exclude_unset=True)
    )
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property


@router.delete("/{property_id}")
def delete_property(property_id: int, session: Session = Depends(get_session)):
    if not PropertyService.delete_property(session, property_id):
        raise HTTPException(status_code=404, detail="Property not found")
    return {"ok": True}
