from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel
from nono_rent_backend.models.tenant import Tenant
from nono_rent_backend.database import get_session
from nono_rent_backend.services.tenant_service import TenantService


class TenantCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str | None = None
    address: str


class TenantUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None


router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.post("/", response_model=Tenant)
def create_tenant(tenant_data: TenantCreate, session: Session = Depends(get_session)):
    return TenantService.create_tenant(session, tenant_data.model_dump())


@router.get("/", response_model=list[Tenant])
def read_tenants(session: Session = Depends(get_session)):
    return TenantService.get_all_tenants(session)


@router.get("/{tenant_id}", response_model=Tenant)
def read_tenant(tenant_id: int, session: Session = Depends(get_session)):
    tenant = TenantService.get_tenant_by_id(session, tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant


@router.put("/{tenant_id}", response_model=Tenant)
def update_tenant(
    tenant_id: int, tenant_update: TenantUpdate, session: Session = Depends(get_session)
):
    tenant = TenantService.update_tenant(
        session, tenant_id, tenant_update.model_dump(exclude_unset=True)
    )
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant


@router.delete("/{tenant_id}")
def delete_tenant(tenant_id: int, session: Session = Depends(get_session)):
    if not TenantService.delete_tenant(session, tenant_id):
        raise HTTPException(status_code=404, detail="Tenant not found")
    return {"ok": True}
