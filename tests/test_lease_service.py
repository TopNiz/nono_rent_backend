import pytest
from datetime import date
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.pool import StaticPool
from nono_rent_backend.models.lease import Lease, LeaseType
from nono_rent_backend.services.lease_service import LeaseService
from nono_rent_backend.models import Tenant, Property, Lease as LeaseModel, Quittance


@pytest.fixture(scope="module")
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        yield s


def test_create_lease(session: Session):
    lease_data = {
        "tenant_id": 1,
        "property_id": 1,
        "start_date": date(2024, 1, 1),
        "end_date": date(2025, 1, 1),
        "rent_amount": 1000.0,
        "charges": 100.0,
        "deposit": 2000.0,
        "lease_type": LeaseType.MEUBLE,
    }
    lease = LeaseService.create_lease(session, lease_data)
    assert lease.tenant_id == 1
    assert lease.rent_amount == 1000.0


def test_get_lease_by_id(session: Session):
    lease_data = {
        "tenant_id": 1,
        "property_id": 1,
        "start_date": date(2024, 1, 1),
        "end_date": date(2025, 1, 1),
        "rent_amount": 1000.0,
        "charges": 100.0,
        "deposit": 2000.0,
        "lease_type": LeaseType.MEUBLE,
    }
    lease = LeaseService.create_lease(session, lease_data)
    retrieved = LeaseService.get_lease_by_id(session, lease.id)
    assert retrieved == lease


def test_get_all_leases(session: Session):
    leases = LeaseService.get_all_leases(session)
    assert len(leases) >= 1


def test_update_lease(session: Session):
    lease_data = {
        "tenant_id": 1,
        "property_id": 1,
        "start_date": date(2024, 1, 1),
        "end_date": date(2025, 1, 1),
        "rent_amount": 1000.0,
        "charges": 100.0,
        "deposit": 2000.0,
        "lease_type": LeaseType.MEUBLE,
    }
    lease = LeaseService.create_lease(session, lease_data)
    update_data = {"rent_amount": 1200.0}
    updated = LeaseService.update_lease(session, lease.id, update_data)
    assert updated.rent_amount == 1200.0


def test_delete_lease(session: Session):
    lease_data = {
        "tenant_id": 1,
        "property_id": 1,
        "start_date": date(2024, 1, 1),
        "end_date": date(2025, 1, 1),
        "rent_amount": 1000.0,
        "charges": 100.0,
        "deposit": 2000.0,
        "lease_type": LeaseType.MEUBLE,
    }
    lease = LeaseService.create_lease(session, lease_data)
    assert LeaseService.delete_lease(session, lease.id)
    assert LeaseService.get_lease_by_id(session, lease.id) is None
