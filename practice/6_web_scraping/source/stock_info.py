"""
There is a list of most active Stocks on Yahoo Finance https://finance.yahoo.com/most-active.
You need to compose several sheets based on data about companies from this list.
To fetch data from webpage you can use requests lib. To parse html you can use beautiful soup lib or lxml.
Sheets which are needed:
1. 5 stocks with most youngest CEOs and print sheet to output. You can find CEO info in Profile tab of concrete stock.
    Sheet's fields: Name, Code, Country, Employees, CEO Name, CEO Year Born.
TODO: 2. 10 stocks with best 52-Week Change. 52-Week Change placed on Statistics tab.
    Sheet's fields: Name, Code, 52-Week Change, Total Cash
TODO: 3. 10 largest holds of Blackrock Inc. You can find related info on the Holders tab.
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


from typing import Union
import requests
from bs4 import BeautifulSoup, element
from useful_data import COUNTRIES

URL = 'https://finance.yahoo.com'

MOST_ACTIVE_100_RESULTS = '/most-active?offset=0&count=100'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6)\
    AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15'
    }


def get_soup_from_page(
    url: str,
    headers: dict[str, str],
    html_parser: str = 'html.parser'
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


def parse_soup_for_stocks_list(
    soup: BeautifulSoup
        ) -> list[dict[str, Union[str, element.Tag]]]:
    if not all_stocks_are_listed_on_page(soup):
        print('Not all stocks are shown!!! :(')
    # TODO: FIX PARSING ALL STOCKS
    else:
        print('Done! :D')
    stocks_rows: element.ResultSet = soup.find_all(
        'tr',
        class_='simpTblRow'
    )
    result_stocks = []
    for stock in stocks_rows:
        code_tag: element.Tag = stock.find(
                'a',
                class_='Fw(600) C($linkColor)'
            )
        result_stocks.append({
            'code': code_tag.text,
            'name': stock.find(
                'td',
                class_='Va(m) Ta(start) Px(10px) Fz(s)'
            ).text,
            'stock_link': code_tag['href'],
            'stock_tag': stock
        })
    return result_stocks


def parse_for_stocks_profiles(
    stocks: list[dict[str, Union[str, element.Tag]]]
        ) -> None:
    for stock in stocks:
        try:
            stock['country'] = 'error'
            stock['employees'] = 'error'
            stock['ceo'] = 'error'
            stock['ceo_year_born'] = 'error'
            stock_link: str = stock['stock_link']
            qm_idx = stock_link.find('?')
            profile_link: str = stock_link[:qm_idx] + \
                '/profile' + stock_link[qm_idx:]
            stock_profile_soup: BeautifulSoup = get_soup_from_page(
                URL+profile_link,
                HEADERS
            )
            stock_details_left_col: element.Tag = stock_profile_soup.find(
                'p',
                class_='D(ib) W(47.727%) Pend(40px)'
            )
            stock_details_right_col: element.Tag = stock_profile_soup.find(
                'p',
                class_='D(ib) Va(t)'
            )
            stock_executives_table: element.Tag = stock_profile_soup.find(
                'table',
                class_='W(100%)'
            )
            left_column_brs = stock_details_left_col.find_all('br')
            left_column_lines = []
            for br in left_column_brs:
                left_column_lines.append(br.previous_sibling.text.strip())
            left_column_lines.append(
                left_column_brs[-1].next_sibling.text.strip()
            )
            for line in left_column_lines:
                if line in COUNTRIES:
                    stock['country'] = line
            stock['employees'] = ''.join(
                stock_details_right_col.find_all(
                    'span',
                    class_='Fw(600)'
                )[-1].text.strip()  # TODO: FIX + ERROR IF NOT GIVEN
            )
            for executive in stock_executives_table.find_all(
                'tr',
                class_='C($primaryColor) BdB Bdc($seperatorColor) H(36px)'
            ):  # TODO: IF NO CEO - PICK FIRST ONE
                if 'ceo' in executive.find(
                    'td',
                    class_='Ta(start) W(45%)'
                ).text.lower():
                    stock['ceo'] = executive.find(
                        'td',
                        'Ta(start)'
                    ).text.strip()
                    try:
                        stock['ceo_year_born'] = int(executive.find_all(
                            'td',
                            'Ta(end)'
                        )[-1].text.strip())
                    except ValueError:
                        stock['ceo_year_born'] = 'error'
                    # TODO: FIX PLACEHOLDER
                    break
        except AttributeError:
            continue
    for stock in stocks:  # TODO: MOVE IT TO SORTING
        if 'error' in stocks.values():
            stocks.remove(stock)


def find_youngest_ceos(
    stocks: list[dict[str, Union[str, element.Tag]]]
        ) -> list[dict[str, Union[str, element.Tag]]]:
    stocks.sort(key=lambda x: x['ceo_year_born'], reverse=True)
    return stocks[:5]


def save_youngest_ceos(stocks: list[dict[str, Union[str, element.Tag]]]):
    table_width: int = 19
    cols_width: dict[str, int] = {}
    for value, column_title in [
        ('code', 4),
        ('name', 4),
        ('country', 7),
        ('employees', 9),
        ('ceo', 8),
        ('ceo_year_born', 13)
    ]:
        cols_width[value] = max([
            len(str(stock[value])) for stock in stocks
        ] + [column_title])
        table_width += cols_width[value]
    table_title: str = ' 5 stocks with most youngest CEOs '
    with open('./results/youngest_ceos.txt', 'w') as fh:
        fh.write(f'{table_title:=^{table_width}}\n')
        fh.write(f'| {"Name":<{cols_width["name"]}} | \
{"Code":<{cols_width["code"]}} | {"Country":<{cols_width["country"]}} | \
{"Employees":<{cols_width["employees"]}} | {"CEO Name":<{cols_width["ceo"]}} \
| {"CEO Year Born":<{cols_width["ceo_year_born"]}} |\n')
        fh.write('-'*table_width + '\n')
        for stock in stocks:
            fh.write(f'| {stock["name"]:<{cols_width["name"]}} | \
{stock["code"]:<{cols_width["code"]}} | \
{stock["country"]:<{cols_width["country"]}} | \
{stock["employees"]:<{cols_width["employees"]}} | \
{stock["ceo"]:<{cols_width["ceo"]}} | \
{stock["ceo_year_born"]:<{cols_width["ceo_year_born"]}} |\n')


def main():
    soup: BeautifulSoup = get_soup_from_page(
        URL+MOST_ACTIVE_100_RESULTS,
        HEADERS
    )
    stocks: list[dict[str, Union[
        str,
        element.Tag
        ]]] = parse_soup_for_stocks_list(soup)
    parse_for_stocks_profiles(stocks)
    youngest_ceos_stocks = find_youngest_ceos(stocks)
    save_youngest_ceos(youngest_ceos_stocks)


if __name__ == '__main__':
    main()
