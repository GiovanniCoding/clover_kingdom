from fastapi import APIRouter, Depends, HTTPException, status

from app.db.database import get_db
from app.db.models.applications import ApplicationRepository
from app.db.models.profiles import ProfileRepository
from app.schemas.applications_schemas import (
    PostApplicationRequest,
    ApplicationResponse,
)
from typing import List

router = APIRouter()


@router.post(
    "/",
    tags=["solicitudes"],
    summary="Create a new application",
    description="Create a new application",
    response_description="Application created successfully",
    response_model=ApplicationResponse,
)
async def post_application(
    application: PostApplicationRequest, session=Depends(get_db)
) -> ApplicationResponse:
    """
    Endpoint to create a new application
    """
    try:
        # Verify if the student id is already in the database
        profile_repository = ProfileRepository(session)
        profile = profile_repository.get_profile_by_personal_id(
            personal_id=application.personal_id
        )
        if profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The student id is already in the database",
            )
        # Create profile in database
        profile_repository = ProfileRepository(session)
        profile = profile_repository.create_profile(
            personal_id=application.personal_id,
            name=application.name,
            last_name=application.last_name,
            age=application.age,
            magic_affinity=application.magic_affinity,
        )

        # Create application in database
        application_repository = ApplicationRepository(session)
        application = application_repository.create_application(
            profile_id=profile.id,
        )

        # Return application created
        return ApplicationResponse(
            id=application.id,
            personal_id=profile.personal_id,
            name=profile.name,
            last_name=profile.last_name,
            age=profile.age,
            magic_affinity=profile.magic_affinity,
        )
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Something went wrong while creating the application: {e}",
        )


@router.get(
    "/",
    tags=["solicitudes"],
    summary="Get all applications",
    description="Get all applications",
    response_description="Applications retrieved successfully",
    response_model=List[ApplicationResponse],
)
async def get_applications(session=Depends(get_db)) -> List[ApplicationResponse]:
    """
    Endpoint to get all applications
    """
    try:
        # Get all applications
        application_repository = ApplicationRepository(session)
        applications = application_repository.get_applications()

        # Return applications
        return [
            ApplicationResponse(
                id=application.id,
                personal_id=application.profile.personal_id,
                name=application.profile.name,
                last_name=application.profile.last_name,
                age=application.profile.age,
                magic_affinity=application.profile.magic_affinity,
            )
            for application in applications
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Something went wrong while getting the applications: {e}",
        )
