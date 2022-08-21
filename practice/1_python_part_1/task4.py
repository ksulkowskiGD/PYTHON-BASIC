"""
Write function which receives list of integers.
Calculate power of each integer and
subtract difference between original previous value and its power.
For first value subtract nothing.
Restriction:
Examples:
    >>> calculate_power_with_difference([1, 2, 3])
    [1, 4, 7]  # because [1^2, 2^2 - (1^2 - 1), 3^2 - (2^2 - 2)]
"""
from typing import List


def calculate_power_with_difference(ints: List[int]) -> List[int]:
    if ints:
        return [ints[0]**2] + [
            number**2 - (ints[idx]**2 - ints[idx])
            for idx, number in enumerate(ints[1:])
            ]
    return []
