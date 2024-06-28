from typing import List

from sqlalchemy import UUID as PGUUID
from sqlalchemy import Column, Enum, ForeignKey
from sqlalchemy.orm import relationship

from src.app.db.models.base import BaseModel

ApplicationsStatusEnum = Enum(
    "Pendiente", "Aprobada", "Rechazada", name="applications_status"
)


class Application(BaseModel):
    __tablename__ = "applications"

    status = Column(ApplicationsStatusEnum, nullable=False)
    student_id = Column(PGUUID, ForeignKey("students.id"), nullable=False)

    student = relationship("Student", back_populates="applications")


class ApplicationRepository:
    def __init__(self, session):
        self.session = session

    def create_application(self, **kwargs):
        application = Application(
            status="Pendiente",
            student_id=kwargs.get("student_id"),
        )
        self.session.add(application)
        self.session.commit()
        self.session.refresh(application)
        return application

    def get_applications(self) -> List[Application]:
        return (
            self.session.query(Application)
            .filter(Application.deleted_at.is_(None))
            .all()
        )

    def get_application_by_id(self, application_id: str) -> Application:
        return (
            self.session.query(Application)
            .filter(Application.id == application_id, Application.deleted_at.is_(None))
            .first()
        )

    def update_application(self, application: Application, status: str) -> Application:
        setattr(application, "status", status)
        self.session.commit()
        self.session.refresh(application)
        return application
