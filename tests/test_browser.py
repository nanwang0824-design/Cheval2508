# main3.py

import random

from src.cheval.browser.browser import Browser
from src.cheval.browser.navigator import Navigator
from src.cheval.parsers import MatchListParser, MatchParser, RaceParser, HorseParser, JockeyParser, TrainerParser

def main():
    browser = Browser()
    navigator = Navigator(browser)
    parsers = Parsers()
    navigator.go_to_search_page()
    year = 2024 #random.choice(range(2020, 2025))
    month = 7 # random.choice(range(1, 13))
    navigator.search_by_year_month(year, month)
    html = navigator.get_html()
    code_name_link_action_list = parsers.match_list.parse(html=html)
    for cnla in code_name_link_action_list:
        navigator.open_match(cnla.code, cnla.action)


    


if __name__ == "__main__":
    main()
    input()