from bs4 import BeautifulSoup
from pytest import mark
from source.stock_info import all_stocks_are_listed_on_page


with open('test/htmls_for_testing.txt', 'r') as fh:
    not_all_results: str = fh.readline()
    all_results: str = fh.readline()


all_stocks_are_listed_on_page_params = [
    (all_results, True),
    (not_all_results, False)
]


@mark.parametrize('html, result', all_stocks_are_listed_on_page_params)
def test_all_stocks_are_listed_on_page(html, result):
    soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
    assert all_stocks_are_listed_on_page(soup) is result
