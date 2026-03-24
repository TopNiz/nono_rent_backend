import pytest
from datetime import date
from pydantic import ValidationError
from nono_rent_backend.models.quittance import Quittance, QuittanceStatus
import os
import tempfile


def test_quittance_creation():
    """Test creating a Quittance instance."""
    quittance = Quittance.model_validate(
        {
            "lease_id": 1,
            "period_month": 1,
            "period_year": 2024,
            "rent_amount": 1000.0,
            "charges_amount": 100.0,
            "total_amount": 1100.0,
            "payment_date": date(2024, 1, 15),
            "status": QuittanceStatus.GENERATED,
        }
    )
    assert quittance.lease_id == 1
    assert quittance.period_month == 1
    assert quittance.period_year == 2024
    assert quittance.rent_amount == 1000.0
    assert quittance.charges_amount == 100.0
    assert quittance.total_amount == 1100.0
    assert quittance.payment_date == date(2024, 1, 15)
    assert quittance.status == QuittanceStatus.GENERATED


def test_quittance_invalid_month():
    """Test that invalid month raises ValidationError."""
    with pytest.raises(ValidationError):
        Quittance.model_validate(
            {
                "lease_id": 1,
                "period_month": 13,
                "period_year": 2024,
                "rent_amount": 1000.0,
                "charges_amount": 100.0,
                "total_amount": 1100.0,
                "payment_date": date(2024, 1, 15),
                "status": QuittanceStatus.DRAFT,
            }
        )


def test_quittance_negative_amounts():
    """Test that negative amounts raise ValidationError."""
    with pytest.raises(ValidationError):
        Quittance.model_validate(
            {
                "lease_id": 1,
                "period_month": 1,
                "period_year": 2024,
                "rent_amount": -100.0,
                "charges_amount": 100.0,
                "total_amount": 1100.0,
                "payment_date": date(2024, 1, 15),
                "status": QuittanceStatus.DRAFT,
            }
        )


def test_generate_pdf():
    """Test PDF generation."""
    quittance = Quittance(
        lease_id=1,
        period_month=1,
        period_year=2024,
        rent_amount=1000.0,
        charges_amount=100.0,
        total_amount=1100.0,
        payment_date=date(2024, 1, 15),
        status=QuittanceStatus.DRAFT,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = os.path.join(tmpdir, "quittance.pdf")
        quittance.generate_pdf(pdf_path)

        assert os.path.exists(pdf_path)
        assert os.path.getsize(pdf_path) > 0  # PDF has content

    # Check that status changes to GENERATED
    assert quittance.status == QuittanceStatus.GENERATED
