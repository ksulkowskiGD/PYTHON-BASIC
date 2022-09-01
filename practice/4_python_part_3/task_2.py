"""
Write function which executes custom operation from math module
for given arguments.
Restrition: math function could take 1 or 2 arguments
If given operation does not exists, raise OperationNotFoundException
Examples:
     >>> math_calculate('log', 1024, 2)
     10.0
     >>> math_calculate('ceil', 10.7)
     11
"""
import math


class OperationNotFoundException(Exception):
    def __init__(self):
        self.msg: str = 'Operation not found in math module'
        super().__init__(self.msg)


def math_calculate(function: str, *args):
    try:
        math_func = getattr(math, function)
    except (AttributeError):
        raise OperationNotFoundException
    return math_func(*args)


"""
Write tests for math_calculate function
"""
