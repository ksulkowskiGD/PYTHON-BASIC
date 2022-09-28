"""
There is a list of most active Stocks on Yahoo Finance https://finance.yahoo.com/most-active.
You need to compose several sheets based on data about companies from this list.
To fetch data from webpage you can use requests lib. To parse html you can use beautiful soup lib or lxml.
Sheets which are needed:
1. 5 stocks with most youngest CEOs and print sheet to output. You can find CEO info in Profile tab of concrete stock.
    Sheet's fields: Name, Code, Country, Employees, CEO Name, CEO Year Born.
2. 10 stocks with best 52-Week Change. 52-Week Change placed on Statistics tab.
    Sheet's fields: Name, Code, 52-Week Change, Total Cash
3. 10 largest holds of Blackrock Inc. You can find related info on the Holders tab.
    Blackrock Inc is an investment management corporation.
    Sheet's fields: Name, Code, Shares, Date Reported, % Out, Value.
    All fields except first two should be taken from Holders tab.


Example for the first sheet (you need to use same sheet format):
==================================== 5 stocks with most youngest CEOs ===================================
| Name        | Code | Country       | Employees | CEO Name                             | CEO Year Born |
---------------------------------------------------------------------------------------------------------
| Pfizer Inc. | PFE  | United States | 78500     | Dr. Albert Bourla D.V.M., DVM, Ph.D. | 1962          |
...

About sheet format:
- sheet title should be aligned to center
- all columns should be aligned to the left
- empty line after sheet

Write at least 2 tests on your choose.
Links:
    - requests docs: https://docs.python-requests.org/en/latest/
    - beautiful soup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    - lxml docs: https://lxml.de/
"""


import requests
from bs4 import BeautifulSoup, element
import mechanicalsoup

URL = 'https://finance.yahoo.com/most-active?offset=0&count=100'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6)\
    AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15'
    }


def get_soup_from_main_page(
    url: str,
    headers: dict[str, str],
    html_parser: str
        ) -> BeautifulSoup:
    html = requests.get(url, headers=headers)
    return BeautifulSoup(html.content, html_parser)


def all_stocks_are_listed_on_page(soup: BeautifulSoup) -> bool:
    stocks_header: element.Tag = soup.find(
        'div',
        class_='D(ib) Fz(m) Fw(b) Lh(23px) W(75%)--mobp'
    )
    spans: element.ResultSet = stocks_header.find_all('span', recursive=False)
    results_shown_n: str = spans[1].span.text
    start_idx: int = results_shown_n.find('of ') + 3
    number_of_all_stocks: str = ''
    number_of_shown_stocks: str = ''
    for x in results_shown_n[2:]:
        if x == ' ':
            break
        number_of_shown_stocks += x
    for y in results_shown_n[start_idx:]:
        if y == ' ':
            break
        number_of_all_stocks += y
    return int(number_of_all_stocks) == int(number_of_shown_stocks)


def parse_soup_for_stocks_list(soup: BeautifulSoup):
    if not all_stocks_are_listed_on_page(soup):
        print('Not all stocks are shown!!! :(')
    else:
        print('Done! :D')
    stocks_rows: element.ResultSet = soup.find_all(
        'tr',
        class_='simpTblRow'
    )
    result_stocks = []
    for stock in stocks_rows:
        result_stocks.append((
            stock.find(
                'a',
                class_='Fw(600) C($linkColor)'
            ).text,
            stock.find(
                'td',
                class_='Va(m) Ta(start) Px(10px) Fz(s)'
            ).text,
            stock
        ))
    return result_stocks


def parse_for_youngest_ceos(stocks: element.ResultSet):
    pass


def main():
    soup: BeautifulSoup = get_soup_from_main_page(
        URL,
        HEADERS,
        'html.parser'
    )
    stocks: element.ResultSet = parse_soup_for_stocks_list(soup)
    for stock in stocks:
        print(stock[0], stock[1])


if __name__ == '__main__':
    main()
