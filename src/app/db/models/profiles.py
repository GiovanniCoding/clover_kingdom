from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import relationship, Mapped

from src.app.db.models.base import BaseModel

MagicAffinityEnum = Enum(
    "Oscuridad", "Luz", "Fuego", "Agua", "Viento", "Tierra", name="magic_affinity"
)


class Profile(BaseModel):
    __tablename__ = "profiles"

    personal_id = Column(String(10), unique=True, nullable=False)
    name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    age = Column(Integer, nullable=False)
    magic_affinity = Column(MagicAffinityEnum, nullable=False)

    application: Mapped["Application"] = relationship(back_populates="profile") # type: ignore


class ProfileRepository:
    def __init__(self, session):
        self.session = session

    def create_profile(self, **kwargs):
        profile = Profile(
            personal_id=kwargs.get("personal_id"),
            name=kwargs.get("name"),
            last_name=kwargs.get("last_name"),
            age=kwargs.get("age"),
            magic_affinity=kwargs.get("magic_affinity"),
        )
        self.session.add(profile)
        self.session.commit()
        self.session.refresh(profile)
        return profile

    def get_profile_by_personal_id(self, personal_id: str):
        return (
            self.session.query(Profile)
            .filter(
                Profile.personal_id == personal_id,
                Profile.deleted_at.is_(None),
            )
            .first()
        )
