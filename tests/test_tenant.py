import pytest
from pydantic import ValidationError
from nono_rent_backend.models.tenant import Tenant


def test_tenant_creation():
    """Test creating a Tenant instance."""
    tenant = Tenant.model_validate(
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "0123456789",
            "address": "123 Rue de la Paix, Paris",
        }
    )
    assert tenant.first_name == "John"
    assert tenant.last_name == "Doe"
    assert tenant.email == "john.doe@example.com"
    assert tenant.phone == "0123456789"
    assert tenant.address == "123 Rue de la Paix, Paris"


def test_tenant_invalid_email():
    """Test that invalid email raises ValidationError."""
    with pytest.raises(ValidationError):
        Tenant.model_validate(
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "notanemail",
                "phone": "0123456789",
                "address": "123 Rue de la Paix, Paris",
            }
        )
