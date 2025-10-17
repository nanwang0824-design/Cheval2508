# test_parsers.py

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlmodel import select

from examples import html
from src.cheval.parsers.parsers import Parsers
from src.cheval.models.models import DataType, CodeRecorder, Match, Race, Horse, Jockey, Trainer, add_odds_tan_to_race
from src.cheval.storage.html_storage import HTMLStorage
from src.cheval.storage.database import ChevalDB

def test_month():
    test_html = html.html_month_1
    parser = Parsers()
    pr = parser.month.parse(html=test_html, entity_code="try202503")
    print(pr)

def test_match():
    test_html = html.html_match_1
    code = "pw01srl10012025020520250906/A8"
    name = "2回札幌5日"
    parser = Parsers()
    pr = parser.match.parse(html=test_html, entity_code=code)
    thematch: Match = pr.entity
    print(f"\nmatch: {thematch}")
    if len(thematch._races) > 0:
        print(f"\nthe first race (build in): {thematch._races.popitem()}")
    else:
        print(f"\nno race (build in): {thematch._races}")
    db = ChevalDB()
    record = db.check_code(code, DataType.MATCH)
    if record:
        print(f"\ncode exists: {record}")
    else:
        db.insert_match(thematch)
    obtained_match = db.get_match_by_code(code)
    print("\nmatch:\n", obtained_match)
    if len(obtained_match._races) > 0:
        print(f"\nthe first race (build in): {obtained_match._races.popitem()}")
    else:
        print(f"\nno race (build in): {obtained_match._races}")
    #print("\ncode list:\n", db.get_all_codes())
    db.close()

def test_race():
    test_html = html.html_race_2
    code = "pw01sde1005201703010420170603/1A"
    name = "障害3歳以上オープン（混合）"
    parser = Parsers()
    pr = parser.race.parse(html=test_html, entity_code=code, entity_name=name, father_entity_code="Unknown")
    therace: Race = pr.entity
    print(f"\nrace: {therace}")
    print(f"\nprize list: {therace._prize_list}")
    if len(therace._result_list) > 0:
        print(f"\nthe first result: {therace._result_list[0]}")
        print(f"\ncorner list in the first result: {therace._result_list[0]._corner_list}")
    else:
        print(f"\nno result: {therace._result_list}")
    db = ChevalDB()
    record = db.check_code(code, DataType.RACE)
    if record:
        print(f"\ncode exists: {record}")
    else:
        db.insert_race(therace)
        db.insert_race_result_list(therace._result_list)
    obtained_race = db.get_race_by_code(code)
    print(f"\nrace: {obtained_race}")
    print(f"\nprize list: {obtained_race._prize_list}")
    if len(obtained_race._result_list) > 0:
        print(f"\nthe first result (build in): {obtained_race._result_list[0]}")
        print(f"\ncorner list in the first result (build in): {obtained_race._result_list[0]._corner_list}")
    else:
        print(f"\nno result (build in): {obtained_race._result_list}")
    obtained_race_results = db.get_results_by_race_code(code)
    if len(obtained_race_results) > 0:
        print(f"\nthe first result (in database): {obtained_race_results[0]}")
        print(f"\ncorner list in the first result (in database): {obtained_race_results[0]._corner_list}")
    else:
        print(f"\nno result (in database): {obtained_race_results}")
    #print("\ncode list:\n", db.get_all_codes())
    db.close()

def test_horse():
    test_html = html.html_horse_2
    code = "pw01dud102014102254/C6"
    name = "スプリングボックス"
    parser = Parsers()
    pr = parser.horse.parse(html=test_html, entity_code=code, entity_name=name)
    thehorse: Horse = pr.entity
    print(f"\nhorse: {thehorse}")
    if len(thehorse._result_list) > 0:
        print(f"\nthe first result (build-in): {thehorse._result_list[0]}")
    else:
        print(f"\nno result (build-in): {thehorse._result_list}")
    db = ChevalDB()
    record = db.check_code(code, DataType.HORSE)
    if record:
        print(f"\ncode exists: {record}")
    else:
        db.insert_horse(thehorse)
        db.insert_horse_result_list(thehorse._result_list)
    obtained_horse = db.get_horse_by_code(code)
    print(f"\nhorse: {obtained_horse}")
    if len(obtained_horse._result_list) > 0:
        print(f"\nthe first result (build-in): {obtained_horse._result_list[0]}")
    else:
        print(f"\nno result (build-in): {obtained_horse._result_list}")
    obtained_horse_results = db.get_results_by_horse_code(code)
    if len(obtained_horse_results) > 0:
        print(f"\nthe first result (in database) of {len(obtained_horse_results)}: {obtained_horse_results[0]}")
    else:
        print(f"\nno result (in database): {obtained_horse_results}")
    #print("\ncode list:\n", db.get_all_codes())
    db.close()

def test_jockey():
    test_html = html.html_jockey_1
    code="pw04kmk001160/FA"
    name="荻野 極"
    parser = Parsers()
    pr = parser.jockey.parse(html=test_html, entity_code=code, entity_name=name)
    thejockey: Jockey = pr.entity
    test_html = html.html_jockey_summary_1
    summary_code = "pw04kps101160/00"
    pr = parser.joceky_summary.parse(html=test_html, entity_code=summary_code, father_entity_code=code)
    thejockey._summary_past = pr.history
    print(f"\njockey: {thejockey}")
    if len(thejockey._summary_this_year) > 0:
        print(f"\nthe first summary of this year: {thejockey._summary_this_year[0]}")
    else:
        print(f"\nno summary of this year: {thejockey._summary_this_year}")
    if len(thejockey._summary_total) > 0:
        print(f"\nthe first summary of total: {thejockey._summary_total[0]}")
    else:
        print(f"\nno summary of total: {thejockey._summary_total}")
    if len(thejockey._summary_past) > 0:
        print(f"\nthe first summary of past: {thejockey._summary_past[0]}")
    else:
        print(f"\nno summary of past: {thejockey._summary_past}")
    db = ChevalDB()
    record = db.check_code(code, DataType.JOCKEY)
    if record:
        print(f"\ncode exists: {record}")
    else:
        db.insert_jockey(thejockey)
        db.insert_jockey_trainer_summary_list(thejockey._summary_this_year)
        db.insert_jockey_trainer_summary_list(thejockey._summary_total)
        db.insert_jockey_trainer_summary_list(thejockey._summary_past)
    obtained_jockey = db.get_jockey_by_code(code)
    print(f"\njockey: {obtained_jockey}")
    if len(obtained_jockey._summary_this_year) > 0:
        print(f"\nthe first summary of this year (build in): {obtained_jockey._summary_this_year[0]}")
    else:
        print(f"\nno summary of this year (build in): {obtained_jockey._summary_this_year}")
    if len(obtained_jockey._summary_total) > 0:
        print(f"\nthe first summary of total (build in): {obtained_jockey._summary_total[0]}")
    else:
        print(f"\nno summary of total (build in): {obtained_jockey._summary_total}")
    if len(obtained_jockey._summary_past) > 0:
        print(f"\nthe first summary of past (build in): {obtained_jockey._summary_past[0]}")
    else:
        print(f"\nno summary of past (build in): {obtained_jockey._summary_past}")
    obtained_jockey_summries = db.get_summaries_by_jockey_trainer_code(code)
    if len(obtained_jockey_summries) > 0:
        print(f"\nthe first summary (in database): {obtained_jockey_summries[0]}")
    else:
        print(f"\nno summary (in database): {obtained_jockey_summries}")
    #print("\ncode list:\n", db.get_all_codes())
    db.close()

def test_trainer():
    test_html = html.html_trainer_1
    code="pw05cmk000427/1A"
    name="森 秀行"
    parser = Parsers()
    pr = parser.trainer.parse(html=test_html, entity_code=code, entity_name=name)
    thetrainer: Trainer = pr.entity
    test_html = html.html_trainer_summary_1
    summary_code = "pw05cps100427/20"
    pr = parser.trainer_summary.parse(html=test_html, entity_code=summary_code, father_entity_code=code)
    thetrainer._summary_past = pr.history
    print(f"\ntrainer: {thetrainer}")
    if len(thetrainer._summary_this_year) > 0:
        print(f"\nthe first summary of this year: {thetrainer._summary_this_year[0]}")
    else:
        print(f"\nno summary of this year: {thetrainer._summary_this_year}")
    if len(thetrainer._summary_total) > 0:
        print(f"\nthe first summary of total: {thetrainer._summary_total[0]}")
    else:
        print(f"\nno summary of total: {thetrainer._summary_total}")
    if len(thetrainer._summary_past) > 0:
        print(f"\nthe first summary of past: {thetrainer._summary_past[0]}")
    else:
        print(f"\nno summary of past: {thetrainer._summary_past}")
    db = ChevalDB()
    record = db.check_code(code, DataType.TRAINER)
    if record:
        print(f"\ncode exists: {record}")
    else:
        db.insert_trainer(thetrainer)
        db.insert_jockey_trainer_summary_list(thetrainer._summary_this_year)
        db.insert_jockey_trainer_summary_list(thetrainer._summary_total)
        db.insert_jockey_trainer_summary_list(thetrainer._summary_past)
    obtained_trainer = db.get_trainer_by_code(code)
    print(f"\ntrainer: {obtained_trainer}")
    if len(obtained_trainer._summary_this_year) > 0:
        print(f"\nthe first summary of this year (build in): {obtained_trainer._summary_this_year[0]}")
    else:
        print(f"\nno summary of this year (build in): {obtained_trainer._summary_this_year}")
    if len(obtained_trainer._summary_total) > 0:
        print(f"\nthe first summary of total (build in): {obtained_trainer._summary_total[0]}")
    else:
        print(f"\nno summary of total (build in): {obtained_trainer._summary_total}")
    if len(obtained_trainer._summary_past) > 0:
        print(f"\nthe first summary of past (build in): {obtained_trainer._summary_past[0]}")
    else:
        print(f"\nno summary of past (build in): {obtained_trainer._summary_past}")
    obtained_trainer_summries = db.get_summaries_by_jockey_trainer_code(code)
    if len(obtained_trainer_summries) > 0:
        print(f"\nthe first summary (in database): {obtained_trainer_summries[0]}")
    else:
        print(f"\nno summary (in database): {obtained_trainer_summries}")
    print("\ncode list:\n", db.get_all_codes())
    db.close()

def test_odds_tan():
    test_html = html.html_race_1
    parser = Parsers()
    pr = parser.race.parse(html=test_html, entity_code="pw01sde1005201703010420170603/1A", entity_name="障害3歳以上オープン（混合）")
    therace: Race = pr.entity
    test_html = html.html_odds_tan_1
    parser = Parsers()
    pr_odds = parser.odds_tan.parse(html=test_html, entity_code="pw151ou1005201703010420170603Z/5C", entity_name="障害3歳以上オープン（混合）")
    theodds = pr_odds.entity
    therace.add_odds_tan(theodds)
    print(f"\nodds: {theodds}")
    print(f"\nrace: {therace}")

if __name__ == "__main__":
    print("Hello")
    test_month()
    #test_match()
    #test_race()
    test_horse()
    #test_jockey()
    #test_trainer()
    #test_odds_tan()