from pytest import fixture
from unittest.mock import Mock


@fixture
def generate_default_args():
    args_mock = Mock()
    n_dicts = [2]
    dict_fields = ['fake-address=address', 'some_name=name']
    args_mock.number_of_dicts = n_dicts
    args_mock.dictionaries_fields = dict_fields
    return args_mock


@fixture
def generate_wrong_int_args():
    args_mock = Mock()
    n_dicts = [-2]
    dict_fields = ['fake-address=address', 'some_name=name']
    args_mock.number_of_dicts = n_dicts
    args_mock.dictionaries_fields = dict_fields
    return args_mock


@fixture
def generate_invalid_dict_field():
    args_mock = Mock()
    n_dicts = [2]
    dict_fields = ['test', 'some_name=name']
    args_mock.number_of_dicts = n_dicts
    args_mock.dictionaries_fields = dict_fields
    return args_mock


@fixture
def generate_invalid_faker_provider():
    arg_mock = Mock()
    n_dicts = [2]
    dict_fields = ['fake-address=lol', 'some_name=name']
    arg_mock.number_of_dicts = n_dicts
    arg_mock.dictionaries_fields = dict_fields
    return arg_mock
