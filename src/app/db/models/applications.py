import enum

from sqlalchemy import Column, Enum
from sqlalchemy.orm import relationship

from src.app.db.models.base import BaseModel


class ApplicationsStatusEnum(enum.Enum):
    pending = "Pendiente"
    approved = "Aprobada"
    rejected = "Rechazada"


class Applications(BaseModel):
    __tablename__ = "applications"

    status = Column(Enum(ApplicationsStatusEnum), nullable=False)

    profile = relationship("Profile", uselist=False, back_populates="application")
