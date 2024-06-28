from sqlalchemy import Column, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped
from src.app.db.models.base import BaseModel

ApplicationsStatusEnum = Enum(
    "Pendiente", "Aprobada", "Rechazada", name="applications_status"
)


class Application(BaseModel):
    __tablename__ = "applications"

    status = Column(ApplicationsStatusEnum, nullable=False)
    
    profile_id = Column(UUID, ForeignKey("profiles.id"), nullable=False)
    profile: Mapped["Profile"] = relationship(back_populates="application") # type: ignore


class ApplicationRepository:
    def __init__(self, session):
        self.session = session

    def create_application(self, **kwargs):
        application = Application(
            status="Pendiente",
            profile_id=kwargs.get("profile_id"),
        )
        self.session.add(application)
        self.session.commit()
        self.session.refresh(application)
        return application
    
    def get_applications(self):
        return self.session.query(Application).filter(
            Application.deleted_at.is_(None)
        ).all()
