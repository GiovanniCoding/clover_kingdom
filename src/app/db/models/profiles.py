import enum

from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from src.app.db.models.base import BaseModel


class MagicAffinityEnum(enum.Enum):
    darkness = "Oscuridad"
    light = "Luz"
    fire = "Fuego"
    water = "Agua"
    wind = "Viento"
    land = "Tierra"


class Profile(BaseModel):
    __tablename__ = "profiles"

    personal_id = Column(String(10), unique=True, nullable=False)
    name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    age = Column(Integer, nullable=False)
    magic_affinity = Column(Enum(MagicAffinityEnum), nullable=False)

    applications = relationship("Applications", back_populates="profile")
