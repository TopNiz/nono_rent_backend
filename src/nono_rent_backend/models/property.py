from sqlmodel import Field, SQLModel
from pydantic import field_validator
from enum import Enum


class PropertyType(str, Enum):
    MEUBLE = "meublé"
    VIDE = "vide"


class Property(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    address: str
    type: PropertyType

    @field_validator("address")
    @classmethod
    def validate_address(cls, v):
        if not v.strip():
            raise ValueError("Address cannot be empty")
        return v
