from fastapi import APIRouter

from .endpoints import health
from .endpoints import applications

router = APIRouter(
    prefix="/v1",
)
router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(applications.router, prefix="/applications", tags=["applications"])
