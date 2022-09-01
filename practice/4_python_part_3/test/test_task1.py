from task_1 import calculate_days
from task_1 import InvalidDateException, WrongFormatException
from pytest import mark, raises

### today's date for testing purposes: 2022-09-01

normal_dates_inputs = [
    ('2022-08-31', 1),
    ('2022-08-25', 7),
    ('2022-09-01', 0),
    ('2022-12-24', -114)
]


invalid_date_inputs = [
    '2022-02-29',
    '1990-02-30',
    '1976-01-98',
    '1929-05-32',
    '1023-04-31'
]

wrong_format_inputs = [
    'kjsdjs',
    '2022-02-111',
    ' 2022-01-10 ',
    '',
    '2022-02--25',
    '20-02-2022'
]


@mark.task1
@mark.freeze_time('2022-09-01')
@mark.parametrize('input_date, days', normal_dates_inputs)
def test_calculate_days(input_date, days):
    assert calculate_days(input_date) == days



@mark.task1
@mark.freeze_time('2022-09-01')
@mark.parametrize('input_date', invalid_date_inputs)
def test_calculate_days_invalid_date(input_date):
    with raises(InvalidDateException):
        calculate_days(input_date)


@mark.task1
@mark.freeze_time('2022-09-01')
@mark.parametrize('input_date', wrong_format_inputs)
def test_calculate_days_wrong_format(input_date):
    with raises(WrongFormatException):
        calculate_days(input_date)
