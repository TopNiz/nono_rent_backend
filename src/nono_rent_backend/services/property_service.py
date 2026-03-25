from sqlmodel import Session, select
from nono_rent_backend.models.property import Property
from typing import List, Optional


class PropertyService:
    @staticmethod
    def create_property(session: Session, property_data: dict) -> Property:
        property = Property.model_validate(property_data)
        session.add(property)
        session.commit()
        session.refresh(property)
        return property

    @staticmethod
    def get_property_by_id(session: Session, property_id: int) -> Optional[Property]:
        return session.get(Property, property_id)

    @staticmethod
    def get_all_properties(session: Session) -> List[Property]:
        return session.exec(select(Property)).all()

    @staticmethod
    def update_property(
        session: Session, property_id: int, property_update: dict
    ) -> Optional[Property]:
        property = session.get(Property, property_id)
        if not property:
            return None
        for key, value in property_update.items():
            if hasattr(property, key):
                setattr(property, key, value)
        session.commit()
        session.refresh(property)
        return property

    @staticmethod
    def delete_property(session: Session, property_id: int) -> bool:
        property = session.get(Property, property_id)
        if not property:
            return False
        session.delete(property)
        session.commit()
        return True
