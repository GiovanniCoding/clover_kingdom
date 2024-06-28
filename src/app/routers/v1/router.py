from fastapi import APIRouter

from .endpoints import applications, health

router = APIRouter(
    prefix="/v1",
)
router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(applications.router, prefix="/solicitudes", tags=["solicitudes"])
