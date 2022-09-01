from pytest import mark, raises
from task_2 import OperationNotFoundException, math_calculate


normal_inputs = [
    ('log', 10.0, [1024, 2]),
    ('ceil', 11, [10.7]),
    ('fabs', 3, [-3]),
    ('pow', 81, [3, 4]),
    ('sqrt', 14.0, [196]),
    ('cosh', 11.573574828312076, [3.14])
]


@mark.task2
@mark.parametrize('math_fun, result, args', normal_inputs)
def test_math_calculate(math_fun, result, args):
    assert math_calculate(math_fun, *args) == result


@mark.task2
def test_wrong_operation():
    with raises(OperationNotFoundException):
        math_calculate('power', 14, 2)


@mark.task2
def test_wrong_args():
    with raises(TypeError):
        math_calculate('pow', 4, 2, 2)
