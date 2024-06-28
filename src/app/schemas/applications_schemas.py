from typing import Annotated, Optional
from uuid import UUID

import annotated_types
from pydantic import BaseModel, field_validator


class PostApplicationRequest(BaseModel):
    student_id: Annotated[str, annotated_types.MaxLen(10)]
    name: Annotated[str, annotated_types.MaxLen(20)]
    last_name: Annotated[str, annotated_types.MaxLen(20)]
    age: Annotated[int, annotated_types.Ge(10), annotated_types.Le(99)]
    magic_affinity: Annotated[str, str]

    @field_validator("magic_affinity")
    def magic_affinity_option(cls, value: str) -> str:
        valid_options = ["Oscuridad", "Luz", "Fuego", "Agua", "Viento", "Tierra"]
        if value not in valid_options:
            raise ValueError(f"Magic affinity must be one of {valid_options}")
        return value


class PutApplicationRequest(BaseModel):
    student_id: Optional[Annotated[str, annotated_types.MaxLen(10)]] = None
    name: Optional[Annotated[str, annotated_types.MaxLen(20)]] = None
    last_name: Optional[Annotated[str, annotated_types.MaxLen(20)]] = None
    age: Optional[Annotated[int, annotated_types.Ge(10), annotated_types.Le(99)]] = None
    magic_affinity: Optional[Annotated[str, str]] = None

    @field_validator("magic_affinity")
    def magic_affinity_option(cls, value: str) -> str:
        valid_options = ["Oscuridad", "Luz", "Fuego", "Agua", "Viento", "Tierra"]
        if value not in valid_options:
            raise ValueError(f"Magic affinity must be one of {valid_options}")
        return value

    def as_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "last_name": self.last_name,
            "age": self.age,
            "magic_affinity": self.magic_affinity,
        }


class ApplicationResponse(BaseModel):
    id: UUID
    student_id: str
    name: str
    last_name: str
    age: int
    magic_affinity: str
    status: str

    def as_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "name": self.name,
            "last_name": self.last_name,
            "age": self.age,
            "magic_affinity": self.magic_affinity,
            "status": self.status,
        }
