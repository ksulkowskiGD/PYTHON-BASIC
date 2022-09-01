from task_read_write_2 import write_words
from pytest import mark


@mark.read_write_2
def test_write_words(create_test_write_2_files):
    dir, file1, file2 = create_test_write_2_files
    write_words(dir, ['abc', 'def', 'xyz'])
    assert file1.read() == 'abc\ndef\nxyz'
    assert file2.read() == 'xyz,def,abc'
