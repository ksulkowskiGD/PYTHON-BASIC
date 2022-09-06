import pytest
from task_4 import print_name_address, InvalidNumberOfDictsError
from faker import Faker


@pytest.mark.task4
def test_print_name_address(generate_default_args, capsys):
    Faker.seed(123)
    args = generate_default_args
    # pytest.set_trace()
    print_name_address(args)
    captured = capsys.readouterr()
    assert captured.out == "{'fake-address': '4106 Peterson Center\\nEast"\
        " Matthew, UT 32635', 'some_name': 'Patricia Cooper'}\n"\
        "{'fake-address': '96105 Garcia Cape Apt. 220\\nRhondashire, KS "\
        "62012', 'some_name': 'Christine Lynch'}\n"


@pytest.mark.task4
def test_print_name_address_wrong_int(generate_wrong_int_args):
    args = generate_wrong_int_args
    # pytest.set_trace()
    with pytest.raises(InvalidNumberOfDictsError):
        print_name_address(args)


@pytest.mark.task4
def test_print_name_address_invalid_dict_fields(
    generate_invalid_dict_field,
    capsys
):
    args = generate_invalid_dict_field
    print_name_address(args)
    captured = capsys.readouterr()
    assert captured.out == 'Error\nDictionaries fields usage: FIELD=PROVIDER\n'


@pytest.mark.task4
def test_print_name_address_invalid_faker_provider(
    generate_invalid_faker_provider,
    capsys
):
    args = generate_invalid_faker_provider
    print_name_address(args)
    captured = capsys.readouterr()
    assert captured.out == 'Error\nInvalid faker provider\n'
