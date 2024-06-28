from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    status: str


@router.get(
    "/",
    tags=["health"],
    summary="Health Check",
    description="Check the health status of the API",
    response_description="Health status of the API",
    response_model=HealthResponse,
)
async def get_health_status():
    """
    Endpoint to check the health status of the API
    """
    return HealthResponse(status="ok")
