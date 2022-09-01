"""
Write a parametrized test for two functions.
The functions are used to find a number by ordinal
in the Fibonacci sequence.
One of them has a bug.

Fibonacci sequence: https://en.wikipedia.org/wiki/Fibonacci_number

Task:
 1. Write a test with @pytest.mark.parametrize decorator.
 2. Find the buggy function and fix it.
"""

from task_parametrize import fibonacci_1, fibonacci_2
from pytest import mark


inputs = [
    (1, 1),
    (2, 1),
    (3, 2),
    (4, 3),
    (5, 5),
    (6, 8),
    (7, 13),
    (8, 21),
    (9, 34),
    (10, 55),
    (25, 75_025)
]


@mark.fibo
@mark.parametrize('n, result', inputs)
def test_fibonacci_1(n, result):
    assert result == fibonacci_1(n)


@mark.fibo
@mark.parametrize('n, result', inputs)
def test_fibonacci_2(n, result):
    assert result == fibonacci_2(n)
