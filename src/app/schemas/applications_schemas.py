from typing import Annotated, Optional
from uuid import UUID

import annotated_types
from pydantic import BaseModel, field_validator


class PostApplicationRequest(BaseModel):
    identification: Annotated[str, annotated_types.MaxLen(10)]
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
    identification: Optional[Annotated[str, annotated_types.MaxLen(10)]] = None
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
            "identification": self.identification,
            "name": self.name,
            "last_name": self.last_name,
            "age": self.age,
            "magic_affinity": self.magic_affinity,
        }


class ApplicationResponse(BaseModel):
    id: UUID
    identification: str
    name: str
    last_name: str
    age: int
    magic_affinity: str
    status: str
    grimoire: Optional[str]

    def as_dict(self):
        return {
            "id": self.id,
            "identification": self.identification,
            "name": self.name,
            "last_name": self.last_name,
            "age": self.age,
            "magic_affinity": self.magic_affinity,
            "status": self.status,
            "grimoire": self.grimoire,
        }
