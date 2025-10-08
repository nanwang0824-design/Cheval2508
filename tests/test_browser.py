# test_browser.py

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import random

from src.cheval.browser.browser import Browser
from src.cheval.browser.navigator import Navigator
from src.cheval.parsers.parsers import Parsers
from src.cheval.models.models import DataType, Match, Race, Horse, Jockey, Trainer, add_odds_tan_to_race
from src.cheval.config import BASE_URL


def test_browser():
    browser = Browser()
    navigator = Navigator(browser)
    parsers = Parsers()
    navigator.go_to_search_page()
    year = random.choice(range(2020, 2025))
    month = random.choice(range(1, 13))
    navigator.search_by_year_month(year, month)
    html_match_list = navigator.get_html()
    parse_result_match_list = parsers.match_list.parse(html=html_match_list, entity_code=str(year).zfill(4)+str(month).zfill(2))
    for cnla_match in parse_result_match_list.links[DataType.MATCH]:
        html_match = navigator.get_match_html(cnla_match.action)
        parse_result_match = parsers.match.parse(html=html_match, entity_code=cnla_match.code, entity_name=cnla_match.name)
        the_match: Match = parse_result_match.entity
        for i in range(len(parse_result_match.links[DataType.RACE])):
            cnla_race = parse_result_match.links[DataType.RACE][i]
            html_race = navigator.get_race_html(BASE_URL+cnla_race.link)
            parse_result_race = parsers.race.parse(html=html_race, entity_code=cnla_race.code, entity_name=cnla_race.name)
            the_race: Race = parse_result_race.entity
            for cnla_horse in parse_result_race.links[DataType.HORSE]:
                html_horse = navigator.get_horse_html(BASE_URL+cnla_horse.link)
                parse_result_horse = parsers.horse.parse(html=html_horse, entity_code=cnla_horse.code, entity_name=cnla_horse.name)
                the_horse: Horse = parse_result_horse.entity
                navigator.back()
            for cnla_jockey in parse_result_race.links[DataType.JOCKEY]:
                html_jockey = navigator.get_jockey_trainer_html(cnla_jockey.action)
                parse_result_jockey = parsers.jockey.parse(html=html_jockey, entity_code=cnla_jockey.code, entity_name=cnla_jockey.name)
                the_jockey: Jockey = parse_result_jockey.entity
                cnla_jockey_summary = parse_result_jockey.links[DataType.JOCKEY_SUMMARY][0]
                html_jockey_summary = navigator.get_jockey_trainer_html(cnla_jockey_summary.action)
                parse_result_jockey_summary = parsers.joceky_summary.parse(html=html_jockey_summary, entity_code=cnla_jockey_summary.code, entity_name=cnla_jockey_summary.name)
                the_jockey.summary_past = parse_result_jockey_summary.history
                navigator.back()
                navigator.back()
            for cnla_trainer in parse_result_race.links[DataType.TRAINER]:
                html_trainer = navigator.get_jockey_trainer_html(cnla_trainer.action)
                parse_result_trainer = parsers.trainer.parse(html=html_trainer, entity_code=cnla_trainer.code, entity_name=cnla_trainer.name)
                the_trainer: Trainer = parse_result_trainer.entity
                cnla_trainer_summary = parse_result_trainer.links[DataType.TRAINER_SUMMARY][0]
                html_trainer_summary = navigator.get_jockey_trainer_html(cnla_trainer_summary.action)
                parse_result_trainer_summary = parsers.trainer_summary.parse(html=html_trainer_summary, entity_code=cnla_trainer_summary.code, entity_name=cnla_trainer_summary.name)
                the_trainer.summary_past = parse_result_trainer_summary.history
                navigator.back()
                navigator.back()
            navigator.back()
            cnla_odds_tan = parse_result_match.links[DataType.ODDS_TAN][i]
            odds_tan_html = navigator.get_odds_tan_html(cnla_odds_tan.action)
            parse_result_odds_tan = parsers.odds_tan.parse(html=odds_tan_html, entity_code=cnla_odds_tan.code, entity_name=cnla_race.name)
            add_odds_tan_to_race(the_race, parse_result_odds_tan.entity)
            navigator.back()
        navigator.back()
    navigator.back()


if __name__ == "__main__":
    test_browser()
    input()