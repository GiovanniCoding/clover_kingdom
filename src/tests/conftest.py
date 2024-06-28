from uuid import uuid4
import pytest
from factory import SubFactory, LazyAttribute, Sequence
from pytest_factoryboy import register
from factory.alchemy import SQLAlchemyModelFactory
from src.app.db.models.students import Student
from src.app.db.models.applications import Application
from src.app.db.database import get_db
from factory.faker import faker
from sqlalchemy.orm import scoped_session, sessionmaker
from src.app.db.database import engine, Base, SessionLocal

fake = faker.Faker()

Session = scoped_session(sessionmaker(bind=get_db()))

@register
class StudentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Student
        sqlalchemy_session = Session

    id = Sequence(lambda x: uuid4())
    created_at = Sequence(lambda x: fake.date_time())
    updated_at = Sequence(lambda x: fake.date_time())
    deleted_at = None
    identification = Sequence(lambda n: f"ID-{n}")
    name = LazyAttribute(lambda x: fake.first_name())
    last_name = LazyAttribute(lambda x: fake.last_name())
    age = LazyAttribute(lambda x: fake.random_int(min=10, max=99))
    magic_affinity = LazyAttribute(lambda x: fake.random_element(elements=("Oscuridad", "Luz", "Fuego", "Agua", "Viento", "Tierra")))


@register
class ApplicationFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Application
        sqlalchemy_session = Session

    id = Sequence(lambda n: uuid4())
    created_at = Sequence(lambda n: fake.date_time())
    updated_at = Sequence(lambda n: fake.date_time())
    deleted_at = None
    status = "Pendiente"
    student = Sequence(lambda x: SubFactory(StudentFactory))

@pytest.fixture(scope='session')
def connection():
    """Establece una conexión a la base de datos que se usa durante toda la sesión de pruebas."""
    connection = engine.connect()
    yield connection
    connection.close()

@pytest.fixture(scope='session')
def setup_database(connection):
    """Inicializa la base de datos para la sesión de pruebas."""
    Base.metadata.create_all(bind=connection)
    yield
    Base.metadata.drop_all(bind=connection)

@pytest.fixture(scope='function')
def db_session(connection, setup_database):
    """Proporciona una sesión de base de datos que hace rollback después de cada prueba."""

    session = SessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        Session.remove()
