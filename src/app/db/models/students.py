from uuid import UUID
from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import relationship, Mapped
from typing import List

from src.app.db.models.base import BaseModel

MagicAffinityEnum = Enum(
    "Oscuridad", "Luz", "Fuego", "Agua", "Viento", "Tierra", name="magic_affinity"
)
ApplicationsStatusEnum = Enum(
    "Pendiente", "Aprobada", "Rechazada", name="applications_status"
)


class Student(BaseModel):
    __tablename__ = "students"

    student_id = Column(String(10), unique=True, nullable=False)
    name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    age = Column(Integer, nullable=False)
    magic_affinity = Column(MagicAffinityEnum, nullable=False)
    status = Column(ApplicationsStatusEnum, nullable=False)


class StudentRepository:
    def __init__(self, session):
        self.session = session

    def create_student(self, **kwargs):
        profile = Student(
            student_id=kwargs.get("student_id"),
            name=kwargs.get("name"),
            last_name=kwargs.get("last_name"),
            age=kwargs.get("age"),
            magic_affinity=kwargs.get("magic_affinity"),
            status='Pendiente',
        )
        self.session.add(profile)
        self.session.commit()
        self.session.refresh(profile)
        return profile
    
    def get_students(self) -> List[Student]:
        return self.session.query(Student).filter(
            Student.deleted_at.is_(None)
        ).all()

    def get_student_by_student_id(self, student_id: str):
        return (
            self.session.query(Student)
            .filter(
                Student.student_id == student_id,
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
