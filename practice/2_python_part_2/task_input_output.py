"""
Write function which reads a number from input nth times.
If an entered value isn't a number, ignore it.
After all inputs are entered, calculate an average entered number.
Return string with following format:
If average exists, return: "Avg: X", where X is avg value which
rounded to 2 places after the decimal
If it doesn't exists, return: "No numbers entered"
Examples:
    user enters: 1, 2, hello, 2, world
    >>> read_numbers(5)
    Avg: 1.67
    ------------
    user enters: hello, world, foo, bar, baz
    >>> read_numbers(5)
    No numbers entered

"""
from statistics import mean


def read_numbers(n: int) -> str:
    numbers: list[int] = []
    for _ in range(n):
        try:
            numbers.append(int(input()))
        except ValueError:
            continue
    return f'Avg: {mean(numbers):.2f}' if numbers else 'No numbers entered'
