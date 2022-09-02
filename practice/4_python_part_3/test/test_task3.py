from pytest import mark
from task_3 import is_http_domain


inputs = [
    ('http://wikipedia.org', True),
    ('https://ru.wikipedia.org/', True),
    ('griddynamics.com', False),
    ('https://w51.sfgame.net', True),
    ('https://github.com/', True),
    ('', False),
    ('https://www.youtube.com', True),
    ('http://facebook', False),
    ('http://facebook.', False),
    ('http://www.facebook', False),
    ('htttp://.facebook.com', False),
    ('s.', False),
    ('http://www.s.s.s', False),
    ('https://ss.ss', True),
    ('http://s.ss', True)
]


@mark.task3
@mark.parametrize('domain, result', inputs)
def test_is_http_domain(domain, result):
    assert is_http_domain(domain) is result
