# test_parsers.py

import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from examples import html
from src.cheval.parsers.parsers import Parsers

def test_match_list():
    test_html = html.html_match_list_1
    parser = Parsers()
    ls1 = parser.match_list.parse(test_html)
    print(ls1)
    test_html = html.html_match_list_2
    parser = Parsers()
    ls1 = parser.match_list.parse(test_html)
    print(ls1)

def test_match():
    test_html = html.html_match_1
    parser = Parsers()
    r, ls1, ls2 = parser.match.parse(test_html)
    print(r)
    print(ls1)
    print(ls2)

def test_race():
    test_html = html.html_race_1
    parser = Parsers()
    r, ls1, ls2, ls3 = parser.race.parse(test_html)
    print(r)
    print(ls1)
    print(ls2)
    print(ls3)

def test_horse():
    test_html = html.html_horse_1
    parser = Parsers()
    r = parser.horse.parse(test_html)
    print(r)

def test_jockey():
    test_html = html.html_jockey_1
    parser = Parsers()
    r = parser.jockey.parse(test_html)
    print(r)
    test_html = html.html_jockey_summary_1
    r = parser.jockey.parse_for_past(test_html)
    print(r)

def test_trainer():
    test_html = html.html_trainer_1
    parser = Parsers()
    r = parser.trainer.parse(test_html)
    print(r)
    test_html = html.html_trainer_summary_1
    r = parser.trainer.parse_for_past(test_html)
    print(r)

if __name__ == "__main__":
    #test_match_list()
    #test_match()
    #test_race()
    #test_horse()
    #test_jockey()
    test_trainer()