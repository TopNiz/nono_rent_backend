from fastapi import FastAPI
from nono_rent_backend.api.routers import (
    tenant_router,
    property_router,
    lease_router,
    quittance_router,
)
from nono_rent_backend.database import create_db_and_tables

app = FastAPI()

app.include_router(tenant_router)
app.include_router(property_router)
app.include_router(lease_router)
app.include_router(quittance_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
