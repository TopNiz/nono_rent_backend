from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from nono_rent_backend.models.property import Property
from nono_rent_backend.database import get_session

router = APIRouter(prefix="/properties", tags=["properties"])


@router.post("/", response_model=Property)
def create_property(property: Property, session: Session = Depends(get_session)):
    session.add(property)
    session.commit()
    session.refresh(property)
    return property


@router.get("/", response_model=list[Property])
def read_properties(session: Session = Depends(get_session)):
    return session.exec(select(Property)).all()


@router.get("/{property_id}", response_model=Property)
def read_property(property_id: int, session: Session = Depends(get_session)):
    property = session.get(Property, property_id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property


@router.put("/{property_id}", response_model=Property)
def update_property(
    property_id: int, property_update: Property, session: Session = Depends(get_session)
):
    property = session.get(Property, property_id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    for key, value in property_update.model_dump().items():
        setattr(property, key, value)
    session.commit()
    session.refresh(property)
    return property


@router.delete("/{property_id}")
def delete_property(property_id: int, session: Session = Depends(get_session)):
    property = session.get(Property, property_id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    session.delete(property)
    session.commit()
    return {"ok": True}
