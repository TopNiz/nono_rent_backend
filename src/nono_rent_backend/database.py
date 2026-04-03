import os
from collections.abc import Generator

from sqlalchemy.pool import StaticPool
from sqlmodel import Session, create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")

engine_kwargs: dict[str, object] = {"connect_args": {"check_same_thread": False}}
if DATABASE_URL.endswith(":memory:"):
    engine_kwargs["poolclass"] = StaticPool

engine = create_engine(DATABASE_URL, **engine_kwargs)


def get_session() -> Generator[Session, None, None]:
    """Yield a SQLModel database session."""
    with Session(engine) as session:
        yield session


def create_db_and_tables() -> None:
    """Create all SQLModel tables if missing."""
    from sqlmodel import SQLModel

    import nono_rent_backend.models  # noqa: F401

    SQLModel.metadata.create_all(engine)
