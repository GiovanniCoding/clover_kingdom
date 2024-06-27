from uuid import uuid4

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    deleted_at = Column(DateTime, nullable=True)

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }


class BaseModelWithUUID(BaseModel):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    def as_dict(self) -> dict:
        return super().as_dict() | {
            "id": self.id,
        }


class BaseModelWithAutoIncrementID(BaseModel):
    __abstract__ = True

    id = Column(Integer, primary_key=True , autoincrement=True)

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }
