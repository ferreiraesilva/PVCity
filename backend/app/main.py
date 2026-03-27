from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import scenarios, bootstrap, products, scenario_store, parity

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    scenarios.router,
    prefix=f"{settings.API_V1_STR}/scenarios/calculate",
    tags=["scenarios"],
)

app.include_router(
    scenario_store.router,
    prefix=f"{settings.API_V1_STR}/scenarios",
    tags=["scenario-store"],
)

app.include_router(
    bootstrap.router,
    prefix=f"{settings.API_V1_STR}/bootstrap",
    tags=["bootstrap"],
)

app.include_router(
    products.router,
    prefix=f"{settings.API_V1_STR}/products",
    tags=["products"],
)

app.include_router(
    parity.router,
    prefix=f"{settings.API_V1_STR}/parity",
    tags=["parity"],
)


@app.get("/")
def root():
    return {"message": "PVCity API is running."}
