# match_parser.py

import re
from datetime import datetime
from typing import Dict, List

from bs4 import BeautifulSoup
from bs4.element import Tag

from utils import extract_doaction_code

from src.cheval.models.models import Match, CodeNameLinkAction

class MatchParser:

    def __init__(self):
        pass

    def parse(self, html: str, match_code: str = None, return_links: bool = True):
        """read the html string of a match, and save the informations;
        return the links of races and odds if return_links=True"""

        links_of_races: List[CodeNameLinkAction] = []
        links_of_odds: List[CodeNameLinkAction] = []

        soup = BeautifulSoup(html, "html.parser")

        # read the name and date
        temp = soup.select_one("table.basic.mt20 div.main")
        name = temp.get_text(strip=True).split("）")[-1].strip()
        date = datetime.strptime(temp.get_text(strip=True).split("（")[0].strip(), "%Y年%m月%d日")
        
        thematch = Match(code=match_code, date=date, name=name)

        # read the table of races
        races: List[Tag] = list(soup.select("tbody tr"))
        thematch.number_races_in_match = len(races)
        for race in races:
            print(race.prettify())
            race_name = race.select_one("td.race_name").get_text(strip=True)
            race_link = str(race.select_one("th.race_num a")["href"])
            race_code = race_link.replace("/JRADB/accessS.html?CNAME=", "")
            if return_links:
                links_of_races.append(CodeNameLinkAction(code=race_code, name=race_name, link=race_link))
            thematch.races.append(race_code)
            odds_action = race.select_one("td.odds a")["onclick"]
            odds_code = extract_doaction_code(odds_action)
            if return_links:
                links_of_odds.append(CodeNameLinkAction(code=odds_code, name=race_name, action=odds_action))
                #links_of_odds[odds_code] = odds_action
            

        return thematch, links_of_races, links_of_odds


        
        