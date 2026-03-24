import pytest
from fastapi.testclient import TestClient
from nono_rent_backend.api import app
from nono_rent_backend.database import create_db_and_tables


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    create_db_and_tables()


client = TestClient(app)


def test_create_tenant():
    response = client.post(
        "/tenants/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "0123456789",
            "address": "123 Rue de la Paix, Paris",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "John"
    assert "id" in data


def test_read_tenants():
    response = client.get("/tenants/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_create_property():
    response = client.post(
        "/properties/", json={"address": "456 Rue du Test, Paris", "type": "meublé"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["address"] == "456 Rue du Test, Paris"
    assert data["type"] == "meublé"


def test_create_lease():
    response = client.post(
        "/leases/",
        json={
            "tenant_id": 1,
            "property_id": 1,
            "start_date": "2024-01-01",
            "end_date": "2025-01-01",
            "rent_amount": 1000.0,
            "charges": 100.0,
            "deposit": 2000.0,
            "lease_type": "meublé",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["rent_amount"] == 1000.0
    assert "id" in data


def test_create_quittance():
    response = client.post(
        "/quittances/",
        json={
            "lease_id": 1,
            "period_month": 1,
            "period_year": 2024,
            "rent_amount": 1000.0,
            "charges_amount": 100.0,
            "total_amount": 1100.0,
            "payment_date": "2024-01-15",
            "status": "draft",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_amount"] == 1100.0
