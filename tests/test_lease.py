import pytest
from datetime import date
from pydantic import ValidationError
from nono_rent_backend.models.lease import Lease


def test_lease_creation():
    """Test creating a Lease instance."""
    lease = Lease.model_validate(
        {
            "tenant_id": 1,
            "property_id": 1,
            "start_date": date(2024, 1, 1),
            "end_date": date(2025, 1, 1),
            "rent_amount": 1000.0,
            "charges": 100.0,
            "deposit": 2000.0,
            "lease_type": "meublé",
        }
    )
    assert lease.tenant_id == 1
    assert lease.property_id == 1
    assert lease.start_date == date(2024, 1, 1)
    assert lease.end_date == date(2025, 1, 1)
    assert lease.rent_amount == 1000.0
    assert lease.charges == 100.0
    assert lease.deposit == 2000.0
    assert lease.lease_type == "meublé"


def test_lease_invalid_dates():
    """Test that end_date before start_date raises ValidationError."""
    with pytest.raises(ValidationError):
        Lease.model_validate(
            {
                "tenant_id": 1,
                "property_id": 1,
                "start_date": date(2024, 1, 2),
                "end_date": date(2024, 1, 1),
                "rent_amount": 1000.0,
                "charges": 100.0,
                "deposit": 2000.0,
                "lease_type": "meublé",
            }
        )


def test_lease_negative_amounts():
    """Test that negative amounts raise ValidationError."""
    with pytest.raises(ValidationError):
        Lease.model_validate(
            {
                "tenant_id": 1,
                "property_id": 1,
                "start_date": date(2024, 1, 1),
                "end_date": date(2025, 1, 1),
                "rent_amount": -100.0,
                "charges": 100.0,
                "deposit": 2000.0,
                "lease_type": "meublé",
            }
        )
