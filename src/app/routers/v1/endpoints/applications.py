from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from app.db.database import get_db
from app.db.models.students import StudentRepository
from app.schemas.applications_schemas import (
    PostApplicationRequest,
    ApplicationResponse,
    PutApplicationRequest,
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
        student_repository = StudentRepository(session)
        student = student_repository.get_student_by_student_id(
            student_id=application.student_id
        )
        if student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The student id is already in the database",
            )

        # Create student in database
        student = student_repository.create_student(
            student_id=application.student_id,
            name=application.name,
            last_name=application.last_name,
            age=application.age,
            magic_affinity=application.magic_affinity,
        )

        # Return application created
        return ApplicationResponse(
            id=student.id,
            student_id=student.student_id,
            name=student.name,
            last_name=student.last_name,
            age=student.age,
            magic_affinity=student.magic_affinity,
            status=student.status,
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
        student_repository = StudentRepository(session)
        applications = student_repository.get_students()

        # Return applications
        return [
            ApplicationResponse(
                id=application.id,
                student_id=application.student_id,
                name=application.name,
                last_name=application.last_name,
                age=application.age,
                magic_affinity=application.magic_affinity,
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
async def put_application(id: UUID, new_values: PutApplicationRequest, session=Depends(get_db)) -> ApplicationResponse:
    """
    Endpoint to update an application
    """
    try:
        # Verify if the application exists in the database
        student_repository = StudentRepository(session)
        student = student_repository.get_student_by_id(id=id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The application was not found",
            )

        # Update student in database
        student = student_repository.update_student(student=student, **new_values.as_dict())

        # Return application updated
        return ApplicationResponse(
            id=student.id,
            student_id=student.student_id,
            name=student.name,
            last_name=student.last_name,
            age=student.age,
            magic_affinity=student.magic_affinity,
            status=student.status,
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
        student_repository = StudentRepository(session)
        student = student_repository.get_student_by_id(id=id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The application was not found",
            )

        # Update student in database
        student = student_repository.update_student(student=student, status='Aprobada')

        # Return application updated
        return ApplicationResponse(
            id=student.id,
            student_id=student.student_id,
            name=student.name,
            last_name=student.last_name,
            age=student.age,
            magic_affinity=student.magic_affinity,
            status=student.status,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Something went wrong while updating the application: {e}",
        )
