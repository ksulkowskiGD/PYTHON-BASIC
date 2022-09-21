from pytest import mark
import datetime
from task_classes import Teacher, Homework, Student


@mark.classes
@mark.student
def test_student_fullname(create_student):
    student: Student = create_student
    assert student.last_name == 'Popov'
    assert student.first_name == 'Vladislav'


@mark.classes
@mark.teacher
def test_teacher_fullname(create_teacher):
    teacher: Teacher = create_teacher
    assert teacher.last_name == 'Orlyakov'
    assert teacher.first_name == 'Dmitry'


@mark.classes
@mark.homework
def test_create_homework(create_homework):
    homework: Homework = create_homework
    assert homework.text == 'Learn functions'
    assert homework.created.date() == datetime.datetime.now().date()
    assert homework.deadline == datetime.timedelta(days=5)
    assert homework.is_active()


@mark.classes
@mark.homework
@mark.teacher
def test_teacher_creates_homework(create_teacher_with_homework):
    _, my_homework = create_teacher_with_homework
    assert my_homework.created.date() == datetime.datetime.now().date()
    assert my_homework.text == 'Study Python'
    assert my_homework.deadline == datetime.timedelta(days=2)
    assert my_homework.is_active


@mark.classes
@mark.student
@mark.homework
def test_student_does_homework_from_teacher(
    create_student,
    create_teacher_with_homework
):
    student: Student = create_student
    _, homework = create_teacher_with_homework

    assert student.do_homework(homework) == homework


@mark.classes
@mark.student
@mark.homework
def test_student_does_expired_homework(
    create_student,
    create_teacher_with_expired_homework,
    capsys
):
    student: Student = create_student
    _, homework = create_teacher_with_expired_homework

    assert student.do_homework(homework) is None
    out, _ = capsys.readouterr()
    assert out == 'You are late\n'
