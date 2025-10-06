# test_parsers.py

import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from examples import html
from src.cheval.parsers.parsers import Parsers
from src.cheval.models.models import DataType
from src.cheval.storage.html_storage import HTMLStorage

def test_match_list():
    test_html = html.html_match_list_1
    parser = Parsers()
    pr = parser.match_list.parse(html=test_html, entity_code="try202503")
    print(pr)

def test_match():
    test_html = html.html_match_1
    parser = Parsers()
    pr = parser.match.parse(html=test_html, entity_code="pw01srl10012025020520250906/A8")
    print(pr)

def test_race():
    test_html = html.html_race_1
    parser = Parsers()
    pr = parser.race.parse(html=test_html, entity_code="pw01sde1005201703010420170603/1A", entity_name="障害3歳以上オープン（混合）")
    print(pr)

def test_horse():
    test_html = html.html_horse_1
    parser = Parsers()
    pr = parser.horse.parse(html=test_html, entity_code="pw01dud102012104889/21")
    print(pr)

def test_jockey():
    test_html = html.html_jockey_1
    parser = Parsers()
    pr = parser.jockey.parse(html=test_html, entity_code="pw04kmk001160/FA")
    #print(pr)
    test_html = html.html_jockey_summary_1
    pr = parser.joceky_summary.parse(html=test_html)
    print(pr)

def test_trainer():
    test_html = html.html_trainer_1
    parser = Parsers()
    pr = parser.trainer.parse(html=test_html, entity_code="pw05cmk000427/1A")
    print(pr)
    test_html = html.html_trainer_summary_1
    pr = parser.trainer_summary.parse(html=test_html)
    print(pr)

if __name__ == "__main__":
    print("Hello")
    #test_match_list()
    #test_match()
    #test_race()
    #test_horse()
    #test_jockey()
    #test_trainer()