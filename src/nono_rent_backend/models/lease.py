from sqlmodel import Field, Relationship, SQLModel
from pydantic import field_validator
from enum import Enum
from datetime import date
from uuid import UUID, uuid4


class LeaseType(str, Enum):
    MEUBLE = "meublé"
    VIDE = "vide"


class Lease(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tenant_id: int = Field(foreign_key="tenant.id")
    tenant: "Tenant" = Relationship()
    property_id: int = Field(foreign_key="property.id")
    property: "Property" = Relationship()
    start_date: date
    end_date: date
    rent_amount: float
    charges: float
    deposit: float
    lease_type: LeaseType

    @field_validator("end_date")
    @classmethod
    def validate_dates(cls, v, info):
        start_date = info.data.get("start_date")
        if start_date and v <= start_date:
            raise ValueError("End date must be after start date")
        return v

    @field_validator("rent_amount", "charges", "deposit")
    @classmethod
    def validate_positive_amounts(cls, v):
        if v < 0:
            raise ValueError("Amount must be positive")
        return v
