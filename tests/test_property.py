import pytest
from pydantic import ValidationError
from nono_rent_backend.models.property import Property, PropertyType


def test_property_creation():
    """Test creating a Property instance."""
    prop = Property.model_validate(
        {
            "address": "123 Rue de la Paix, Paris",
            "type": "meublé",
        }
    )
    assert prop.address == "123 Rue de la Paix, Paris"
    assert prop.type == PropertyType.MEUBLE


def test_property_invalid_address():
    """Test that empty address raises ValidationError."""
    with pytest.raises(ValidationError):
        Property.model_validate(
            {
                "address": "",
                "type": "meublé",
            }
        )


def test_property_invalid_type():
    """Test that invalid type raises ValidationError."""
    with pytest.raises(ValidationError):
        Property.model_validate(
            {
                "address": "123 Rue de la Paix, Paris",
                "type": "invalid",
            }
        )
