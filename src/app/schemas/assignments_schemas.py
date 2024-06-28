from uuid import UUID

from pydantic import BaseModel


class AssignmentsResponse(BaseModel):
    id: UUID
    identification: str
    name: str
    magic_affinity: str
    grimoire: str

    def as_dict(self):
        return {
            "id": self.id,
            "identification": self.identification,
            "name": self.name,
            "magic_affinity": self.magic_affinity,
            "grimoire": self.grimoire,
        }
