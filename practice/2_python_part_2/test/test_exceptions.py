import pytest
from task_exceptions import division

inputs = [
    (4, 2, 2),
    (5, 2, 2.5)
]


@pytest.mark.exceptions
@pytest.mark.parametrize('a, b, quotient', inputs)
def test_normal_division(a, b, quotient, capsys):
    assert division(a, b) == quotient
    out, _ = capsys.readouterr()
    assert out == 'Division finished\n'


@pytest.mark.exceptions
def test_division_by_1(capsys):
    division(5, 1)
    out, _ = capsys.readouterr()
    assert out == 'Deletion on 1 get the same result\nDivision finished\n'


@pytest.mark.exceptions
def test_division_by_0(capsys):
    division(5, 0)
    out, _ = capsys.readouterr()
    assert out == 'Division by 0\nDivision finished\n'
