import pytest
from datetime import date
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.pool import StaticPool
from nono_rent_backend.models.quittance import Quittance, QuittanceStatus
from nono_rent_backend.services.quittance_service import QuittanceService
from nono_rent_backend.models import (
    Tenant,
    Property,
    Lease,
    Quittance as QuittanceModel,
)


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


def test_create_quittance(session: Session):
    quittance_data = {
        "lease_id": 1,
        "period_month": 1,
        "period_year": 2024,
        "rent_amount": 1000.0,
        "charges_amount": 100.0,
        "total_amount": 1100.0,
        "payment_date": date(2024, 1, 15),
        "status": QuittanceStatus.DRAFT,
    }
    quittance = QuittanceService.create_quittance(session, quittance_data)
    assert quittance.rent_amount == 1000.0


def test_get_quittance_by_id(session: Session):
    quittance_data = {
        "lease_id": 1,
        "period_month": 1,
        "period_year": 2024,
        "rent_amount": 1000.0,
        "charges_amount": 100.0,
        "total_amount": 1100.0,
        "payment_date": date(2024, 1, 15),
        "status": QuittanceStatus.DRAFT,
    }
    quittance = QuittanceService.create_quittance(session, quittance_data)
    retrieved = QuittanceService.get_quittance_by_id(session, quittance.id)
    assert retrieved == quittance


def test_get_all_quittances(session: Session):
    quittances = QuittanceService.get_all_quittances(session)
    assert len(quittances) >= 1


def test_update_quittance(session: Session):
    quittance_data = {
        "lease_id": 1,
        "period_month": 1,
        "period_year": 2024,
        "rent_amount": 1000.0,
        "charges_amount": 100.0,
        "total_amount": 1100.0,
        "payment_date": date(2024, 1, 15),
        "status": QuittanceStatus.DRAFT,
    }
    quittance = QuittanceService.create_quittance(session, quittance_data)
    update_data = {"total_amount": 1200.0}
    updated = QuittanceService.update_quittance(session, quittance.id, update_data)
    assert updated.total_amount == 1200.0


def test_delete_quittance(session: Session):
    quittance_data = {
        "lease_id": 1,
        "period_month": 1,
        "period_year": 2024,
        "rent_amount": 1000.0,
        "charges_amount": 100.0,
        "total_amount": 1100.0,
        "payment_date": date(2024, 1, 15),
        "status": QuittanceStatus.DRAFT,
    }
    quittance = QuittanceService.create_quittance(session, quittance_data)
    assert QuittanceService.delete_quittance(session, quittance.id)
    assert QuittanceService.get_quittance_by_id(session, quittance.id) is None
