import pytest
from fastapi.testclient import TestClient
from nono_rent_backend.api import app
from nono_rent_backend.database import create_db_and_tables


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    create_db_and_tables()


lease_id = None
landlord_id = None
tenant_id = None
property_id = None

client = TestClient(app)


def test_create_tenant():
    global tenant_id
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
    tenant_id = data["id"]


def test_read_tenants():
    response = client.get("/tenants/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_create_landlord():
    global landlord_id
    response = client.post(
        "/landlords/",
        json={
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "phone": "0987654321",
            "address": "456 Avenue des Champs, Paris",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Jane"
    assert "id" in data
    landlord_id = data["id"]


def test_create_property():
    global property_id
    response = client.post(
        "/properties/",
        json={
            "address": "456 Rue du Test, Paris",
            "type": "meublé",
            "landlord_id": landlord_id,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["address"] == "456 Rue du Test, Paris"
    assert data["type"] == "meublé"
    property_id = data["id"]


def test_create_lease():
    global lease_id
    response = client.post(
        "/leases/",
        json={
            "tenant_id": tenant_id,
            "property_id": property_id,
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
    lease_id = data["id"]


def test_create_quittance():
    response = client.post(
        "/receipts/",
        json={
            "lease_id": lease_id,
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


def test_generate_receipt_pdf():
    response = client.post(
        "/receipts/generate",
        json={
            "lease_id": lease_id,
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
    assert response.headers["content-type"] == "application/pdf"
    assert (
        "attachment; filename=quittance.pdf" in response.headers["content-disposition"]
    )
    # Check that PDF content is present
    pdf_content = response.content
    assert len(pdf_content) > 0
