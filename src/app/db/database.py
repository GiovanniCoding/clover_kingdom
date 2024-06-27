from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from alembic import command
from alembic.config import Config
from app.core.settings import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal: Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
