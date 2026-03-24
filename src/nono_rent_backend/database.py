from sqlmodel import create_engine, Session
from sqlalchemy.pool import StaticPool

# For testing, use in-memory SQLite
DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    from nono_rent_backend.models import Tenant, Property, Lease, Quittance
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)
