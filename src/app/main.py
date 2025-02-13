from fastapi import FastAPI

from src.app.core.settings import settings
from src.app.routers.v1.router import router as api_v1_router

from .db.database import run_migrations

run_migrations()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para gestionar aspirantes a magos",
    version="1.6.0",
)

app.include_router(api_v1_router, prefix="/api")
