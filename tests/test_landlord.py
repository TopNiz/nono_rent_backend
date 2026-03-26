import pytest
from pydantic import ValidationError
from nono_rent_backend.models.landlord import Landlord


def test_landlord_creation():
    """Test creating a Landlord instance."""
    landlord = Landlord.model_validate(
        {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "phone": "0987654321",
            "address": "456 Avenue des Champs, Paris",
        }
    )
    assert landlord.first_name == "Jane"
    assert landlord.last_name == "Smith"
    assert landlord.email == "jane.smith@example.com"
    assert landlord.phone == "0987654321"
    assert landlord.address == "456 Avenue des Champs, Paris"


def test_landlord_invalid_email():
    """Test that invalid email raises ValidationError."""
    with pytest.raises(ValidationError):
        Landlord.model_validate(
            {
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "notanemail",
                "phone": "0987654321",
                "address": "456 Avenue des Champs, Paris",
            }
        )
