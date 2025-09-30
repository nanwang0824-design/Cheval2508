# main3.py

import random

from browser import Browser
from navigator import Navigator
from parsers import Parsers

def main():
    browser = Browser()
    navigator = Navigator(browser)
    parsers = Parsers()
    navigator.go_to_search_page()
    year = 2024 #random.choice(range(2020, 2025))
    month = 7 # random.choice(range(1, 13))
    navigator.search_by_year_month(year, month)
    html = navigator.get_html()
    l = parsers.match_list.parse(html=html)
    print(l)


    


if __name__ == "__main__":
    main()
    input()