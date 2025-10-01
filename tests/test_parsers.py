# test_parsers.py

import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
#sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from examples import html
from cheval.parsers.match_list_parser import MatchListParser

def test_match_list():
    test_html = html.html_macth_list_1
    print("test_match_list")
    parser = MatchListParser()

if __name__ == "__main__":
    test_match_list()