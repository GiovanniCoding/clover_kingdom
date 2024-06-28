from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.db.database import get_db
from app.db.models.applications import ApplicationRepository

from app.schemas.assignments_schemas import AssignmentsResponse


router = APIRouter()


@router.get(
    "/",
    tags=["asignaciones"],
    summary="Get all assignments",
    description="Get all assignments",
    response_description="Assigments retrieved successfully",
    response_model=List[AssignmentsResponse],
)
async def get_assignments(session=Depends(get_db)) -> List[AssignmentsResponse]:
    """
    Endpoint to get all assignments
    """
    try:
        # Get all assignments
        application_repository = ApplicationRepository(session)
        assignments = application_repository.get_approved_applications()

        # Return assignments
        return [
            AssignmentsResponse(
                id=assignment.id,
                identification=assignment.student.identification,
                name=assignment.student.name,
                magic_affinity=assignment.student.magic_affinity,
                grimoire=assignment.student.grimoire,
            )
            for assignment in assignments
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Something went wrong while getting the assigments: {e}",
        )
