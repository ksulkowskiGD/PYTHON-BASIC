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


import sys
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
    results_shown_n: str = soup.findChild(
        'span',
        string='Stocks'
    ).parent.next_sibling.findChild(
        'span'
    ).text
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


def get_link_to_stock_page(stock_link: str, page: str) -> str:
    qm_idx: int = stock_link.find('?')
    return stock_link[:qm_idx] + page + stock_link[qm_idx:]


def parse_for_stocks_statistics(
    stocks: list[dict[str, Union[str, element.Tag]]]
        ) -> None:
    for stock in stocks:
        try:
            stock['change'] = 'error'
            stock['total_cash'] = 'error'
            stats_link: str = get_link_to_stock_page(
                stock['stock_link'],
                '/key-statistics'
            )
            stock_stats_soup: BeautifulSoup = get_soup_from_page(
                URL+stats_link,
                HEADERS
            )
            try:
                stock['change'] = stock_stats_soup.findChild(
                    'span',
                    string='52-Week Change'
                ).parent.next_sibling.text.strip()
            except AttributeError:
                stock['change'] = 'error'

            try:
                stock['total_cash'] = stock_stats_soup.findChild(
                    'span',
                    string='Total Cash'
                ).parent.next_sibling.text.strip()
            except AttributeError:
                stock['total_cash'] = 'error'

        except (ValueError, AttributeError):
            continue


def parse_for_stocks_profiles(
    stocks: list[dict[str, Union[str, element.Tag]]]
        ) -> None:
    for stock in stocks:
        try:
            stock['country'] = 'error'
            stock['employees'] = 'error'
            stock['ceo'] = 'error'
            stock['ceo_year_born'] = 'error'
            profile_link: str = get_link_to_stock_page(
                stock['stock_link'],
                '/profile'
            )
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

            try:
                stock['employees'] = ''.join(
                    stock_details_right_col.find(
                        'span',
                        string='Full Time Employees'
                    ).next_sibling.next_sibling.text.strip()
                )
            except AttributeError:
                stock['employees'] = 'error'

            executives: element.ResultSet = stock_executives_table.find_all(
                'tr',
                class_='C($primaryColor) BdB Bdc($seperatorColor) H(36px)'
            )
            for executive in executives:
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
                    except (AttributeError, ValueError):
                        stock['ceo_year_born'] = 'error'
                    break

            if stock['ceo'] == 'error':
                stock['ceo'] = executives[0].find(
                        'td',
                        'Ta(start)'
                    ).text.strip()

        except (AttributeError, ValueError):
            continue


def find_youngest_ceos(
    stocks: list[dict[str, Union[str, element.Tag]]]
        ) -> list[dict[str, Union[str, element.Tag]]]:
    stocks_copy = stocks.copy()
    for stock in stocks:
        if 'error' in stock.values():
            stocks_copy.remove(stock)
    stocks_copy.sort(key=lambda x: x['ceo_year_born'], reverse=True)
    return stocks_copy[:5]


def find_best_52_week_change_stocks(
    stocks: list[dict[str, Union[str, element.Tag]]]
        ) -> list[dict[str, Union[str, element.Tag]]]:
    stocks_copy = stocks.copy()
    for stock in stocks:
        if 'error' in [stock['change'], stock['total_cash']] or\
                'N/A' in [stock['change'], stock['total_cash']]:
            stocks_copy.remove(stock)
    stocks_copy.sort(key=lambda x: float(x['change'][:-1]), reverse=True)
    return stocks_copy[:10]


def save_results_to_file(
    stocks: list[dict[str, Union[str, element.Tag]]],
    file_name: str,
    task_number: int
        ):
    table_title: str = ''
    table_width: int
    cols_width: dict[str, int] = {}
    columns: list[tuple[str, str, int]]
    match task_number:
        case 1:
            columns = [
                ('Name', 'name', 4),
                ('Code', 'code', 4),
                ('Country', 'country', 7),
                ('Employees', 'employees', 9),
                ('CEO Name', 'ceo', 8),
                ('CEO Year Born', 'ceo_year_born', 13)
            ]
            table_title = ' 5 stocks with most youngest CEOs '
            table_width = 19
            for _, key, column_title in columns:
                cols_width[key] = max([
                    len(str(stock[key])) for stock in stocks
                ] + [column_title])
                table_width += cols_width[key]
        case 2:
            columns = [
                ('Name', 'name', 4),
                ('Code', 'code', 4),
                ('52-Week Change', 'change', 14),
                ('Total Cash', 'total_cash', 10)
            ]
            table_title = ' 10 stocks with best 52-Week Change '
            table_width = 13
            for _, key, column_title in columns:
                cols_width[key] = max([
                    len(str(stock[key])) for stock in stocks
                ] + [column_title])
                table_width += cols_width[key]
        case 3:
            columns = [
                ('Name,' 'name', 4),
                ('Code', 'code', 4),
                ('Shares', 'shares', 6),
                ('Date Reported', 'date_reported', 13),
                ('% Out', 'p_out', 5),
                ('Value', 'value', 5)
            ]
            table_title = ' 10 largest holds of Blackrock Inc. '
            table_width = 19
            for _, key, column_title in columns:
                cols_width[key] = max([
                    len(str(stock[key])) for stock in stocks
                ] + [column_title])
                table_width += cols_width[key]
        case _:
            raise Exception('Wrong task_number')
    with open(file_name, 'w') as fh:
        fh.write(f'{table_title:=^{table_width}}\n')
        values: str = ' | '.join([
            f'{string:<{cols_width[key]}}' for string, key, _ in columns
        ])
        values = '| ' + values + ' |\n'
        fh.write(values)
        fh.write('-'*table_width + '\n')
        for stock in stocks:
            stock_row: str = ' | '.join([
                f'{stock[key]:<{cols_width[key]}}' for
                _,
                key,
                _
                in columns
            ])
            stock_row = '| ' + stock_row + ' |\n'
            fh.write(stock_row)


def main():
    # soup: BeautifulSoup = get_soup_from_page(
    #     URL+MOST_ACTIVE_100_RESULTS,
    #     HEADERS
    # )
    # stocks: list[dict[str, Union[
    #     str,
    #     element.Tag
    #     ]]] = parse_soup_for_stocks_list(soup)
    # parse_for_stocks_profiles(stocks)
    # youngest_ceos_stocks = find_youngest_ceos(stocks)
    # save_results_to_file(
    #     youngest_ceos_stocks,
    #     'results/result1.txt',
    #     1
    # )

    soup: BeautifulSoup = get_soup_from_page(
        URL+MOST_ACTIVE_100_RESULTS,
        HEADERS
    )
    stocks: list[dict[str, Union[
        str,
        element.Tag
        ]]] = parse_soup_for_stocks_list(soup)
    parse_for_stocks_statistics(stocks)
    save_results_to_file(
        find_best_52_week_change_stocks(stocks),
        'results/best_52_week_change.txt',
        2
    )


if __name__ == '__main__':
    main()
