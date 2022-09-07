import pytest
from unittest import mock
from task_5 import make_request


example_html: str = ''
with open('test/example-html.txt') as fh:
    example_html = fh.readline()


def return_generated_response():
    response_mock = mock.Mock()
    response_mock.status.return_value = 200
    response_mock.read().decode('utf-8').return_value = example_html
    return response_mock


@pytest.mark.task5
@mock.patch('task_5.urlopen')
def test_make_request(mocker):
    mocker.return_value = return_generated_response()
    assert make_request('http://example.com') == (200, example_html)
