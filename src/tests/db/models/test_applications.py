from src.app.db.models.applications import Application, ApplicationRepository
from src.app.db.models.students import Student, StudentRepository
from src.tests.conftest import StudentFactory


def test_create_application(db_session):
    application_repository = ApplicationRepository(db_session)
    student_repository = StudentRepository(db_session)
    student = StudentFactory()
    student_repository.create_student(
        identification=student.identification,
        name=student.name,
        last_name=student.last_name,
        age=student.age,
        magic_affinity=student.magic_affinity,
    )

    db_student = (
        db_session.query(Student)
        .filter_by(identification=student.identification)
        .one_or_none()
    )

    application = application_repository.create_application(
        status="Pendiente",
        student_id=db_student.id,
    )

    db_application = (
        db_session.query(Application)
        .filter_by(student_id=application.student.id)
        .one_or_none()
    )
    assert db_application is not None
    assert db_application.status == "Pendiente"
    assert db_application.student.identification == application.student.identification
    assert db_application.student.name == application.student.name
    assert db_application.student.last_name == application.student.last_name
    assert db_application.student.age == application.student.age
    assert db_application.student.magic_affinity == application.student.magic_affinity
    assert db_application.student.grimoire is None


def test_get_applications(db_session):
    application_repository = ApplicationRepository(db_session)
    student_repository = StudentRepository(db_session)

    applications = []
    for _ in range(3):
        student = StudentFactory()
        student_repository.create_student(**student.__dict__)
        db_student = (
            db_session.query(Student)
            .filter_by(identification=student.identification)
            .one_or_none()
        )
        application = application_repository.create_application(
            student_id=db_student.id
        )
        applications.append(application)

    db_applications = application_repository.get_applications()
    count_found = sum(
        1
        for db_application in db_applications
        if db_application.id in [application.id for application in applications]
    )
    assert count_found == len(applications)


def test_get_approved_applications(db_session):
    application_repository = ApplicationRepository(db_session)
    student_repository = StudentRepository(db_session)
    student = StudentFactory()
    student_repository.create_student(**student.__dict__)
    db_student = (
        db_session.query(Student)
        .filter_by(identification=student.identification)
        .one_or_none()
    )
    new_application = application_repository.create_application(
        student_id=db_student.id
    )
    new_application = application_repository.update_application(
        new_application, "Aprobada"
    )
    approved_applications = application_repository.get_approved_applications()
    approved_applications = [
        application
        for application in approved_applications
        if application.id == new_application.id
    ]
    assert len(approved_applications) == 1
    assert approved_applications[0].status == "Aprobada"


def test_get_application_by_id(db_session):
    application_repository = ApplicationRepository(db_session)
    student_repository = StudentRepository(db_session)
    student = StudentFactory()
    student_repository.create_student(**student.__dict__)
    db_student = (
        db_session.query(Student)
        .filter_by(identification=student.identification)
        .one_or_none()
    )
    application = application_repository.create_application(student_id=db_student.id)
    retrieved_application = application_repository.get_application_by_id(application.id)
    assert retrieved_application.id == application.id


def test_update_application(db_session):
    application_repository = ApplicationRepository(db_session)
    student_repository = StudentRepository(db_session)
    student = StudentFactory()
    student_repository.create_student(**student.__dict__)
    db_student = (
        db_session.query(Student)
        .filter_by(identification=student.identification)
        .one_or_none()
    )
    application = application_repository.create_application(student_id=db_student.id)
    updated_application = application_repository.update_application(
        application, "Aprobada"
    )
    assert updated_application.status == "Aprobada"


def test_delete_application(db_session):
    application_repository = ApplicationRepository(db_session)
    student_repository = StudentRepository(db_session)
    student = StudentFactory()
    student_repository.create_student(**student.__dict__)
    db_student = (
        db_session.query(Student)
        .filter_by(identification=student.identification)
        .one_or_none()
    )
    application = application_repository.create_application(student_id=db_student.id)
    deleted_application = application_repository.delete_application(application)
    assert (
        db_session.query(Application)
        .filter_by(id=deleted_application.id)
        .first()
        .deleted_at
        is not None
    )
