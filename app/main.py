from fastapi import FastAPI
from app.core.settings import settings
from app.api.v1.router import router as api_v1_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para gestionar usuarios e ítems",
    version="1.0.0",
)

app.include_router(api_v1_router, prefix="/api")
