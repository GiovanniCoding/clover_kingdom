from fastapi import APIRouter

from .endpoints import applications, assignments, health

router = APIRouter(
    prefix="/v1",
)
router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(applications.router, prefix="/solicitudes", tags=["solicitudes"])
router.include_router(assignments.router, prefix="/asignaciones", tags=["asignaciones"])
