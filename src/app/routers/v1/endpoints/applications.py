from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.db.database import get_db
from app.db.models.applications import ApplicationRepository
from app.db.models.students import StudentRepository
from app.helpers.grimoire import select_grimoire
from app.schemas.applications_schemas import (
    ApplicationResponse,
    PostApplicationRequest,
    PutApplicationRequest,
)

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
        student_repository = StudentRepository(session)
        application_repository = ApplicationRepository(session)
        student = student_repository.get_student_by_identification(
            identification=application.identification
        )
        if student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The student application is already in the database",
            )

        # Create student in database
        student = student_repository.create_student(
            identification=application.identification,
            name=application.name,
            last_name=application.last_name,
            age=application.age,
            magic_affinity=application.magic_affinity,
        )

        # Create application in database
        application = application_repository.create_application(student_id=student.id)

        # Return application created
        return ApplicationResponse(
            id=application.id,
            identification=application.student.identification,
            name=application.student.name,
            last_name=application.student.last_name,
            age=application.student.age,
            magic_affinity=application.student.magic_affinity,
            status=application.status,
            grimoire=application.student.grimoire,
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
                identification=application.student.identification,
                name=application.student.name,
                last_name=application.student.last_name,
                age=application.student.age,
                magic_affinity=application.student.magic_affinity,
                status=application.status,
            )
            for application in applications
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Something went wrong while getting the applications: {e}",
        )


@router.put(
    "/{id}",
    tags=["solicitudes"],
    summary="Update an application",
    description="Update an application",
    response_description="Application updated successfully",
    response_model=ApplicationResponse,
)
async def put_application(
    id: UUID, new_values: PutApplicationRequest, session=Depends(get_db)
) -> ApplicationResponse:
    """
    Endpoint to update an application
    """
    try:
        # Verify if the application exists in the database
        application_repository = ApplicationRepository(session)
        application = application_repository.get_application_by_id(application_id=id)
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The application was not found",
            )

        # Update student in database
        student_repository = StudentRepository(session)
        student = student_repository.get_student_by_id(id=application.student_id)
        student = student_repository.update_student(
            student=student, **new_values.as_dict()
        )

        # Return application updated
        return ApplicationResponse(
            id=application.id,
            identification=student.identification,
            name=student.name,
            last_name=student.last_name,
            age=student.age,
            magic_affinity=student.magic_affinity,
            status=application.status,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Something went wrong while updating the application: {e}",
        )


@router.patch(
    "/{id}",
    tags=["solicitudes"],
    summary="Approve an application",
    description="Approve an application",
    response_description="Application approved successfully",
    response_model=ApplicationResponse,
)
async def patch_application(id: UUID, session=Depends(get_db)) -> ApplicationResponse:
    """
    Endpoint to approve an application
    """
    try:
        # Verify if the application exists in the database
        application_repository = ApplicationRepository(session)
        application = application_repository.get_application_by_id(application_id=id)
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The application was not found",
            )

        # Update the application status in database
        application = application_repository.update_application(
            application=application, status="Aprobada"
        )
        student_repository = StudentRepository(session)
        student = student_repository.get_student_by_id(id=application.student_id)
        student = student_repository.update_student(
            student=student, grimoire=select_grimoire()
        )

        # Return application updated
        return ApplicationResponse(
            id=application.id,
            identification=application.student.identification,
            name=application.student.name,
            last_name=application.student.last_name,
            age=application.student.age,
            magic_affinity=application.student.magic_affinity,
            status=application.status,
            grimoire=application.student.grimoire,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Something went wrong while updating the application: {e}",
        )


@router.delete(
    "/{id}",
    tags=["solicitudes"],
    summary="Delete an application",
    description="Delete an application",
    response_description="Application deleted successfully",
)
async def delete_application(id: UUID, session=Depends(get_db)):
    """
    Endpoint to delete an application
    """
    try:
        # Verify if the application exists in the database
        application_repository = ApplicationRepository(session)
        application = application_repository.get_application_by_id(application_id=id)
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The application was not found",
            )

        # Delete the application from the database
        application_repository.delete_application(application=application)

        student_repository = StudentRepository(session)
        student = student_repository.get_student_by_id(id=application.student_id)
        student_repository.delete_student(student=student)

        # Return success message
        return {"message": "Application deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Something went wrong while deleting the application: {e}",
        )
