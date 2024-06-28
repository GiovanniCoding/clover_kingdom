from typing import List
from uuid import UUID

from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from src.app.db.models.base import BaseModel

MagicAffinityEnum = Enum(
    "Oscuridad", "Luz", "Fuego", "Agua", "Viento", "Tierra", name="magic_affinity"
)
GrimoireRarityEnum = Enum(
    "Una Hoja",
    "Dos Hojas",
    "Tres Hojas",
    "Cuatro Hojas",
    "Cinco Hojas",
    name="grimoire_rarity",
)


class Student(BaseModel):
    __tablename__ = "students"

    identification = Column(String(10), unique=True, nullable=False)
    name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    age = Column(Integer, nullable=False)
    magic_affinity = Column(MagicAffinityEnum, nullable=False)
    grimoire = Column(GrimoireRarityEnum, nullable=True)

    applications = relationship("Application", back_populates="student")


class StudentRepository:
    def __init__(self, session):
        self.session = session

    def create_student(self, **kwargs):
        student = Student(
            identification=kwargs.get("identification"),
            name=kwargs.get("name"),
            last_name=kwargs.get("last_name"),
            age=kwargs.get("age"),
            magic_affinity=kwargs.get("magic_affinity"),
        )
        self.session.add(student)
        self.session.commit()
        self.session.refresh(student)
        return student

    def get_students(self) -> List[Student]:
        return self.session.query(Student).filter(Student.deleted_at.is_(None)).all()

    def get_student_by_identification(self, identification: str):
        return (
            self.session.query(Student)
            .filter(
                Student.identification == identification,
                Student.deleted_at.is_(None),
            )
            .first()
        )

    def get_student_by_id(self, id: UUID):
        return (
            self.session.query(Student)
            .filter(
                Student.id == id,
                Student.deleted_at.is_(None),
            )
            .first()
        )

    def update_student(self, student: Student, **kwargs):
        for key, value in kwargs.items():
            if value is not None:
                setattr(student, key, value)
        self.session.commit()
        self.session.refresh(student)
        return student
