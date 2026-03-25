from sqlmodel import Session, select
from uuid import UUID
from nono_rent_backend.models.lease import Lease
from typing import List, Optional
from datetime import date
from nono_rent_backend.models.lease import LeaseType


class LeaseService:
    @staticmethod
    def create_lease(session: Session, lease_data: dict) -> Lease:
        lease = Lease.model_validate(lease_data)
        session.add(lease)
        session.commit()
        session.refresh(lease)
        return lease

    @staticmethod
    def get_lease_by_id(session: Session, lease_id: UUID) -> Optional[Lease]:
        return session.get(Lease, lease_id)

    @staticmethod
    def get_all_leases(session: Session) -> List[Lease]:
        return session.exec(select(Lease)).all()

    @staticmethod
    def update_lease(
        session: Session, lease_id: UUID, lease_update: dict
    ) -> Optional[Lease]:
        lease = session.get(Lease, lease_id)
        if not lease:
            return None
        for key, value in lease_update.items():
            if hasattr(lease, key):
                setattr(lease, key, value)
        session.commit()
        session.refresh(lease)
        return lease

    @staticmethod
    def delete_lease(session: Session, lease_id: UUID) -> bool:
        lease = session.get(Lease, lease_id)
        if not lease:
            return False
        session.delete(lease)
        session.commit()
        return True
