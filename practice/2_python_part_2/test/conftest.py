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


@fixture
def create_test_read_write_files(tmpdir):
    dir = tmpdir.mkdir('dir')
    for i, number in enumerate(['23', '78', '3']):
        f = dir.join(f'file_{i+1}.txt')
        f.write(number)
    file = dir.join('result.txt')
    return dir, file


@fixture
def create_test_write_2_files(tmpdir):
    dir = tmpdir.mkdir('dir')
    f1 = dir.join('file1.txt')
    f2 = dir.join('file2.txt')
    return dir, f1, f2
