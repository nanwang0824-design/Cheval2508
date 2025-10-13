# match_parser.py

import re
from datetime import datetime
from typing import Dict, List

from bs4 import BeautifulSoup
from bs4.element import Tag

from ..utils.misc import extract_doaction_code
from ..models.models import Match, CodeNameLinkAction, DataType
from .base import BaseParser, ParseResult

class MatchParser(BaseParser):
    data_type = DataType.MATCH
    parser_name = data_type.value

    """
    def __init__(self):
        pass
    """

    def _parse_impl(self, html: str, entity_code: str = None, entity_name: str = None, father_entity_code: str = None):
        """read the html string of a match, and save the informations"""

        links_of_races: List[CodeNameLinkAction] = []
        links_of_odds: List[CodeNameLinkAction] = []
        parse_result = ParseResult[Match]()

        soup = BeautifulSoup(html, "html.parser")

        # read the name and date
        temp = soup.select_one("table.basic.mt20 div.main")
        name = temp.get_text(strip=True).split("）")[-1].strip()
        date = datetime.strptime(temp.get_text(strip=True).split("（")[0].strip(), "%Y年%m月%d日")
        
        thematch: Match = Match(code=entity_code, date=date, name=name)

        # read the table of races
        races: List[Tag] = list(soup.select("tbody tr"))
        thematch.number_races_in_match = len(races)
        for race in races:
            race_name = race.select_one("td.race_name").get_text(strip=True)
            race_link = str(race.select_one("th.race_num a")["href"])
            race_code = race_link.replace("/JRADB/accessS.html?CNAME=", "")
            links_of_races.append(CodeNameLinkAction(thetype=DataType.RACE, code=race_code, name=race_name, link=race_link))
            thematch._races[race_code] = race_name
            odds_action = race.select_one("td.odds a")["onclick"]
            odds_code = extract_doaction_code(odds_action)
            links_of_odds.append(CodeNameLinkAction(thetype=DataType.ODDS_TAN, code=odds_code, name=race_name, action=odds_action))
            #links_of_odds[odds_code] = odds_action
            

        parse_result.entity = thematch
        parse_result.links[DataType.RACE] = links_of_races
        parse_result.links[DataType.ODDS_TAN] = links_of_odds
        return parse_result

        
        