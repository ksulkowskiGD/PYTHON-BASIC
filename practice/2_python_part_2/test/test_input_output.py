from task_input_output import read_numbers
from io import StringIO
from pytest import mark


normal_inputs = [
    ('2\n3\n4\n7\n10\n10', '6.00'),
    ('2\n3\n4\n7\n10\n12', '6.33')
]


@mark.parametrize('input, mean', normal_inputs)
@mark.io
def test_read_numbers_normal(monkeypatch, input, mean):
    io_input: StringIO = StringIO(input)
    monkeypatch.setattr('sys.stdin', io_input)
    result: str = read_numbers(6)
    assert result == 'Avg: ' + mean


@mark.io
def test_read_numbers_ignore_some(monkeypatch):
    io_input: StringIO = StringIO('a\n2\nb\n5\nc\n10')
    monkeypatch.setattr('sys.stdin', io_input)
    result: str = read_numbers(6)
    assert result == 'Avg: 5.67'


@mark.io
def test_read_numbers_ignore_all(monkeypatch):
    io_input: StringIO = StringIO('a\nb\nc\nd\ne\nf')
    monkeypatch.setattr('sys.stdin', io_input)
    result: str = read_numbers(6)
    assert result == 'No numbers entered'
