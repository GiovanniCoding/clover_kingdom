from fastapi import FastAPI

from src.app.core.settings import settings
from src.app.routers.v1.router import router as api_v1_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para gestionar usuarios e ítems",
    version="1.0.0",
)

app.include_router(api_v1_router, prefix="/api")
