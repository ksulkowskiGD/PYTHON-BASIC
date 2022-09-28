from bs4 import BeautifulSoup
from pytest import mark
from stock_info import all_stocks_are_listed_on_page


all_stocks_are_listed_on_page_params = [
    ('<div class="D(ib) Fz(m) Fw(b) Lh(23px) W(75%)--mobp"><span>Matching <\
span>Stocks</span></span><span class="Mstart(15px) Fw(500) Fz(s)"><\
span>1-28 of 28 results</span></span></div>', True),
    ('<div class="D(ib) Fz(m) Fw(b) Lh(23px) W(75%)--mobp"><span>Matching <\
span>Stocks</span></span><span class="Mstart(15px) Fw(500) Fz(s)"><\
span>1-100 of 282 results</span></span></div>', False)
]


@mark.parametrize('html, result', all_stocks_are_listed_on_page_params)
def test_all_stocks_are_listed_on_page(html, result):
    soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
    assert all_stocks_are_listed_on_page(soup) is result
