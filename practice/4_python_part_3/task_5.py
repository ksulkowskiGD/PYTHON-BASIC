"""
Write a function that makes a request
to some url using urllib. Return
status code and decoded response data in utf-8
Examples:
     >>> make_request('https://www.google.com')
     200, 'response data'
"""
from typing import Tuple
from urllib.request import urlopen


def make_request(url: str) -> Tuple[int, str]:
    try:
        with urlopen(url) as response:
            # response.decode('utf-8')
            return response.status, response.read().decode('utf-8')
    except (Exception) as e:
        print(str(e))


def main():
    print(make_request('http://example.com'))


if __name__ == '__main__':
    main()


"""
Write test for make_request function
Use Mock for mocking request with urlopen
https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 200
    >>> m.method2.return_value = b'some text'
    >>> m.method()
    200
    >>> m.method2()
    b'some text'
"""
