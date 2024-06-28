from src.app.db.models.students import Student
from src.app.db.models.students import StudentRepository
from src.tests.conftest import StudentFactory


def test_create_student(db_session):
    student = StudentFactory()
    student_repository = StudentRepository(db_session)
    student_repository.create_student(
        identification=student.identification,
        name=student.name,
        last_name=student.last_name,
        age=student.age,
        magic_affinity=student.magic_affinity,
    )

    db_student = db_session.query(Student).filter_by(identification=student.identification).one_or_none()
    assert db_student is not None
    assert db_student.identification == student.identification
    assert db_student.name == student.name
    assert db_student.last_name == student.last_name
    assert db_student.age == student.age
    assert db_student.magic_affinity == student.magic_affinity
    assert db_student.grimoire is None


def test_get_students(db_session):
    students = [StudentFactory() for _ in range(3)]

    student_repository = StudentRepository(db_session)
    for student in students:
        student_repository.create_student(
            identification=student.identification,
            name=student.name,
            last_name=student.last_name,
            age=student.age,
            magic_affinity=student.magic_affinity,
        )
    db_students = student_repository.get_students()

    count_found = sum(1 for db_student in db_students if db_student.identification in [student.identification for student in students])
    assert count_found == len(students)


def test_get_student_by_identification(db_session):
    student = StudentFactory()

    student_repository = StudentRepository(db_session)
    student_repository.create_student(
        identification=student.identification,
        name=student.name,
        last_name=student.last_name,
        age=student.age,
        magic_affinity=student.magic_affinity,
    )
    db_student = student_repository.get_student_by_identification(student.identification)

    assert db_student is not None
    assert db_student.identification == student.identification


def test_get_student_by_id(db_session):
    student = StudentFactory()
    student_repository = StudentRepository(db_session)
    created_student = student_repository.create_student(
        identification=student.identification,
        name=student.name,
        last_name=student.last_name,
        age=student.age,
        magic_affinity=student.magic_affinity,
    )
    db_student = student_repository.get_student_by_id(created_student.id)
    assert db_student is not None
    assert db_student.id == created_student.id


def test_update_student(db_session):
    student = StudentFactory()
    student_repository = StudentRepository(db_session)
    created_student = student_repository.create_student(
        identification=student.identification,
        name=student.name,
        last_name=student.last_name,
        age=student.age,
        magic_affinity=student.magic_affinity,
    )

    updated_name = "Updated Name"
    student_repository.update_student(created_student, name=updated_name)

    db_student = db_session.query(Student).filter_by(id=created_student.id).one()
    assert db_student.name == updated_name


def test_delete_student(db_session):
    student = StudentFactory()
    student_repository = StudentRepository(db_session)
    created_student = student_repository.create_student(
        identification=student.identification,
        name=student.name,
        last_name=student.last_name,
        age=student.age,
        magic_affinity=student.magic_affinity,
    )

    student_repository.delete_student(created_student)

    db_student = db_session.query(Student).filter_by(id=created_student.id).one()
    assert db_student.deleted_at is not None
