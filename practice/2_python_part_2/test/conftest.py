from pytest import fixture
from task_classes import Teacher, Student, Homework


@fixture
def create_teacher():
    return Teacher('Orlyakov', 'Dmitry')


@fixture
def create_student():
    return Student('Popov', 'Vladislav')


@fixture
def create_homework():
    return Homework('Learn functions', 5)


@fixture
def create_teacher_with_homework():
    teacher = Teacher('Orlyakov', 'Dmitry')
    return teacher, teacher.create_homework('Study Python', 2)


@fixture
def create_teacher_with_expired_homework():
    teacher = Teacher('Orlyakov', 'Dmitry')
    return teacher, teacher.create_homework('Study Python', 0)
