from typing import Annotated
from uuid import UUID

import annotated_types
from pydantic import BaseModel, field_validator


class PostApplicationRequest(BaseModel):
    personal_id: Annotated[str, annotated_types.MaxLen(10)]
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


class PostApplicationResponse(BaseModel):
    id: UUID
    personal_id: str
    name: str
    last_name: str
    age: int
    magic_affinity: str

    def as_dict(self):
        return {
            "id": self.id,
            "personal_id": self.personal_id,
            "name": self.name,
            "last_name": self.last_name,
            "age": self.age,
            "magic_affinity": self.magic_affinity,
        }
