# odds_tan_parser.py

import re
from datetime import datetime
from typing import Dict, List

from bs4 import BeautifulSoup
from bs4.element import Tag

from ..utils.misc import minsec_to_sec, extract_class_race, extract_class_jockey, extract_dd_horse, extract_dd_trainer
from ..models.models import Horse, ResultOfHorse, DataType, CodeNameLinkAction, OddsTan
from .base import BaseParser, ParseResult

class OddsTanParser(BaseParser):
    data_type = DataType.ODDS_TAN
    parser_name = data_type.value

    """
    def __init__(self):
        pass
    """

    def _parse_impl(self, html: str, entity_code: str = None, entity_name: str = None):
        """read the html string of a horse page"""

        soup = BeautifulSoup(html, "html.parser")
        parse_result = ParseResult[OddsTan]()

        odds_tan = OddsTan(code=entity_code)

        # read the odds of horses
        temp = soup.select_one("table.basic.narrow-xy.tanpuku tbody")
        #print(temp.prettify())
        temps: List[Tag] = list(temp.select("tr"))
        for temp in temps:
            num = int(temp.select_one("td.num").get_text(strip=True))
            odds = float(temp.select_one("td.odds_tan").get_text(strip=True))
            odds_tan.odds[num] = odds

        parse_result.entity = odds_tan
        return parse_result

