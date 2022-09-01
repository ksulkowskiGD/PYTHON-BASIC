"""
using datetime module find number of days from custom date to now
Custom date is a string with format "2021-12-24"
If entered string pattern does not match, raise a custom Exception
If entered date is from future, return negative value for number of days
    >>> calculate_days('2021-10-07')  # for this example today is 6 october 2021
    -1
    >>> calculate_days('2021-10-05')
    1
    >>> calculate_days('10-07-2021')
    WrongFormatException
"""
import datetime
import re


class WrongFormatException(Exception):
    def __init__(self):
        self.msg = 'Wrong date input format'
        super().__init__(self.msg)


class InvalidDateException(Exception):
    def __init__(self):
        self.msg = 'Date does not exist'
        super().__init__(self.msg)


def calculate_days(from_date: str) -> int:
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', from_date):
        raise WrongFormatException
    try:
        input_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
    except(ValueError):
        raise InvalidDateException
    days_diff: datetime.timedelta = datetime.datetime.now().date() - input_date
    return days_diff.days

"""
Write tests for calculate_days function
Note that all tests should pass regardless of the day test was run
Tip: for mocking datetime.now() use https://pypi.org/project/pytest-freezegun/
"""
