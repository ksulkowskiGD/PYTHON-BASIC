from task_read_write import read_files, write_to_file
from pytest import mark


@mark.read_write
def test_read_files(create_test_read_write_files):
    temp_dir, _ = create_test_read_write_files
    assert ['23', '78', '3'] == read_files(temp_dir, 3)


@mark.read_write
def test_write_to_file(create_test_read_write_files):
    _, file = create_test_read_write_files
    write_to_file(file, ['23', '78', '3'])
    assert file.read() == '23, 78, 3'


@mark.read_write
def test_read_and_write(create_test_read_write_files):
    dir, write_file = create_test_read_write_files
    write_to_file(write_file, read_files(dir, 3))
    assert '23, 78, 3' == write_file.read()
