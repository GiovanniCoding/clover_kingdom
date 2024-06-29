from fastapi import APIRouter

from .endpoints import applications, assignments, health

router = APIRouter(
    prefix="/v1",
)
router.include_router(health.router, prefix="/health")
router.include_router(applications.router, prefix="/solicitudes")
router.include_router(assignments.router, prefix="/asignaciones")
