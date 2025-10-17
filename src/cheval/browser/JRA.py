# JRA.py

import random

from .browser import Browser
from .navigator import Navigator
from ..parsers.parsers import Parsers
from ..models.models import DataType, Month, Match, Race, Horse, Jockey, Trainer, OddsTan
from ..config import BASE_URL
from ..storage.database import ChevalDB
from ..utils.logging import get_logger


def parse_JRA(year: int, month: int):
    month_code = str(year).zfill(4)+str(month).zfill(2)
    db = ChevalDB()
    if db.check_code(code=month_code, datetype=DataType.MONTH) is not None:
        db.close()
        return
    browser = Browser()
    navigator = Navigator(browser)
    parsers = Parsers()
    logger = get_logger(f"cheval.test.browser")
    navigator.go_to_search_page()
    navigator.search_by_year_month(year, month)
    html_month = navigator.get_html()
    parse_month_list = parsers.month.parse(html=html_month, entity_code=month_code)
    the_month: Month = parse_month_list.entity
    for cnla_match in parse_month_list.links[DataType.MATCH]:
        if db.check_code(code=cnla_match.code, datetype=DataType.MATCH) is not None:
            logger.info(f"Skip: {cnla_match}")
            continue
        html_match = navigator.get_match_html(cnla_match.action)
        parse_result_match = parsers.match.parse(html=html_match, entity_code=cnla_match.code, entity_name=cnla_match.name)
        the_match: Match = parse_result_match.entity
        for i in range(len(parse_result_match.links[DataType.RACE])):
            cnla_race = parse_result_match.links[DataType.RACE][i]
            if db.check_code(code=cnla_race.code, datetype=DataType.RACE) is not None:
                logger.info(f"Skip: {cnla_race}")
                continue
            html_race = navigator.get_race_html(BASE_URL+cnla_race.link)
            parse_result_race = parsers.race.parse(html=html_race, entity_code=cnla_race.code, entity_name=cnla_race.name, father_entity_code=cnla_match.code)
            the_race: Race = parse_result_race.entity
            for cnla_horse in parse_result_race.links[DataType.HORSE]:
                if db.check_code(code=cnla_horse.code, datetype=DataType.HORSE) is not None:
                    logger.info(f"Skip: {cnla_horse}")
                    continue
                html_horse = navigator.get_horse_html(BASE_URL+cnla_horse.link)
                parse_result_horse = parsers.horse.parse(html=html_horse, entity_code=cnla_horse.code, entity_name=cnla_horse.name)
                the_horse: Horse = parse_result_horse.entity
                db.insert_horse(the_horse)
                db.insert_horse_result_list(the_horse._result_list)
                navigator.back()
            for cnla_jockey in parse_result_race.links[DataType.JOCKEY]:
                if db.check_code(code=cnla_jockey.code, datetype=DataType.JOCKEY) is not None:
                    logger.info(f"Skip: {cnla_jockey}")
                    continue
                html_jockey = navigator.get_jockey_trainer_html(cnla_jockey.action)
                parse_result_jockey = parsers.jockey.parse(html=html_jockey, entity_code=cnla_jockey.code, entity_name=cnla_jockey.name)
                the_jockey: Jockey = parse_result_jockey.entity
                cnla_jockey_summary = parse_result_jockey.links[DataType.JOCKEY_SUMMARY][0]
                html_jockey_summary = navigator.get_jockey_trainer_html(cnla_jockey_summary.action)
                parse_result_jockey_summary = parsers.joceky_summary.parse(html=html_jockey_summary, entity_code=cnla_jockey_summary.code, entity_name=cnla_jockey_summary.name, father_entity_code=cnla_jockey.code)
                the_jockey._summary_past = parse_result_jockey_summary.history
                db.insert_jockey(the_jockey)
                db.insert_jockey_trainer_summary_list(the_jockey._summary_this_year)
                db.insert_jockey_trainer_summary_list(the_jockey._summary_total)
                db.insert_jockey_trainer_summary_list(the_jockey._summary_past)
                navigator.back()
                navigator.back()
            for cnla_trainer in parse_result_race.links[DataType.TRAINER]:
                if db.check_code(code=cnla_trainer.code, datetype=DataType.TRAINER) is not None:
                    logger.info(f"Skip: {cnla_trainer}")
                    continue
                html_trainer = navigator.get_jockey_trainer_html(cnla_trainer.action)
                parse_result_trainer = parsers.trainer.parse(html=html_trainer, entity_code=cnla_trainer.code, entity_name=cnla_trainer.name)
                the_trainer: Trainer = parse_result_trainer.entity
                cnla_trainer_summary = parse_result_trainer.links[DataType.TRAINER_SUMMARY][0]
                html_trainer_summary = navigator.get_jockey_trainer_html(cnla_trainer_summary.action)
                parse_result_trainer_summary = parsers.trainer_summary.parse(html=html_trainer_summary, entity_code=cnla_trainer_summary.code, entity_name=cnla_trainer_summary.name, father_entity_code=cnla_trainer.code)
                the_trainer._summary_past = parse_result_trainer_summary.history
                db.insert_trainer(the_trainer)
                db.insert_jockey_trainer_summary_list(the_trainer._summary_this_year)
                db.insert_jockey_trainer_summary_list(the_trainer._summary_total)
                db.insert_jockey_trainer_summary_list(the_trainer._summary_past)
                navigator.back()
                navigator.back()
            navigator.back()
            cnla_odds_tan = parse_result_match.links[DataType.ODDS_TAN][i]
            odds_tan_html = navigator.get_odds_tan_html(cnla_odds_tan.action)
            parse_result_odds_tan = parsers.odds_tan.parse(html=odds_tan_html, entity_code=cnla_odds_tan.code, entity_name=cnla_race.name)
            the_odds_tan: OddsTan = parse_result_odds_tan.entity
            the_race.add_odds_tan(the_odds_tan)
            db.insert_race(the_race)
            db.insert_race_result_list(the_race._result_list)
            db.insert_odds_tan(the_odds_tan)
            navigator.back()
        db.insert_match(the_match)
        navigator.back()
    db.insert_month(the_month)
    navigator.back()
    navigator.close()
    db.close()
    logger.info(f"Finish: {the_month.code}")