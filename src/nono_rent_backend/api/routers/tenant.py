from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from nono_rent_backend.models.tenant import Tenant
from nono_rent_backend.database import get_session

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.post("/", response_model=Tenant)
def create_tenant(tenant: Tenant, session: Session = Depends(get_session)):
    session.add(tenant)
    session.commit()
    session.refresh(tenant)
    return tenant


@router.get("/", response_model=list[Tenant])
def read_tenants(session: Session = Depends(get_session)):
    return session.exec(select(Tenant)).all()


@router.get("/{tenant_id}", response_model=Tenant)
def read_tenant(tenant_id: int, session: Session = Depends(get_session)):
    tenant = session.get(Tenant, tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant


@router.put("/{tenant_id}", response_model=Tenant)
def update_tenant(
    tenant_id: int, tenant_update: Tenant, session: Session = Depends(get_session)
):
    tenant = session.get(Tenant, tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    for key, value in tenant_update.model_dump().items():
        setattr(tenant, key, value)
    session.commit()
    session.refresh(tenant)
    return tenant


@router.delete("/{tenant_id}")
def delete_tenant(tenant_id: int, session: Session = Depends(get_session)):
    tenant = session.get(Tenant, tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    session.delete(tenant)
    session.commit()
    return {"ok": True}
