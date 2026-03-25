from sqlmodel import Session, select
from nono_rent_backend.models.tenant import Tenant
from typing import List, Optional


class TenantService:
    @staticmethod
    def create_tenant(session: Session, tenant_data: dict) -> Tenant:
        tenant = Tenant.model_validate(tenant_data)
        session.add(tenant)
        session.commit()
        session.refresh(tenant)
        return tenant

    @staticmethod
    def get_tenant_by_id(session: Session, tenant_id: int) -> Optional[Tenant]:
        return session.get(Tenant, tenant_id)

    @staticmethod
    def get_all_tenants(session: Session) -> List[Tenant]:
        return session.exec(select(Tenant)).all()

    @staticmethod
    def update_tenant(
        session: Session, tenant_id: int, tenant_update: dict
    ) -> Optional[Tenant]:
        tenant = session.get(Tenant, tenant_id)
        if not tenant:
            return None
        for key, value in tenant_update.items():
            if hasattr(tenant, key):
                setattr(tenant, key, value)
        session.commit()
        session.refresh(tenant)
        return tenant

    @staticmethod
    def delete_tenant(session: Session, tenant_id: int) -> bool:
        tenant = session.get(Tenant, tenant_id)
        if not tenant:
            return False
        session.delete(tenant)
        session.commit()
        return True
