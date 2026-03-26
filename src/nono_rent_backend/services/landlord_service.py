from sqlmodel import Session, select
from typing import List, Optional
from nono_rent_backend.models.landlord import Landlord


class LandlordService:
    @staticmethod
    def create_landlord(session: Session, landlord_data: dict) -> Landlord:
        landlord = Landlord.model_validate(landlord_data)
        session.add(landlord)
        session.commit()
        session.refresh(landlord)
        return landlord

    @staticmethod
    def get_landlord_by_id(session: Session, landlord_id: int) -> Optional[Landlord]:
        return session.get(Landlord, landlord_id)

    @staticmethod
    def get_all_landlords(session: Session) -> List[Landlord]:
        return session.exec(select(Landlord)).all()

    @staticmethod
    def update_landlord(
        session: Session, landlord_id: int, landlord_update: dict
    ) -> Optional[Landlord]:
        landlord = session.get(Landlord, landlord_id)
        if not landlord:
            return None
        for key, value in landlord_update.items():
            if hasattr(landlord, key):
                setattr(landlord, key, value)
        session.commit()
        session.refresh(landlord)
        return landlord

    @staticmethod
    def delete_landlord(session: Session, landlord_id: int) -> bool:
        landlord = session.get(Landlord, landlord_id)
        if not landlord:
            return False
        session.delete(landlord)
        session.commit()
        return True
