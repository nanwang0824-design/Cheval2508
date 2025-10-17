# month_parser.py

from typing import List

from bs4 import BeautifulSoup
from bs4.element import Tag

from ..utils.misc import extract_doaction_code
from ..models.models import CodeNameLinkAction, DataType, Month
from .base import BaseParser, ParseResult

class MonthParser(BaseParser):
    data_type = DataType.MONTH
    parser_name = data_type.value

    def _parse_impl(self, html: str, entity_code: str = None, entity_name: str = None, father_entity_code: str = None) -> ParseResult[None]:
        """read the html string of a match list, and save the informations"""

        links_of_matches: List[CodeNameLinkAction] = []
        parse_result = ParseResult[Month]()

        soup = BeautifulSoup(html, "html.parser")

        # read the table of matches
        temps: List[Tag] = list(soup.select("div.past_result_line_unit div.link_list.multi.div3.mid.center.narrow a"))
        for thematch in temps:
            name = thematch.get_text(strip=True)
            action = str(thematch["onclick"])
            code = extract_doaction_code(action)
            links_of_matches.append(CodeNameLinkAction(thetype=DataType.MATCH, code=code, name=name, action=action))

        month = Month(code=entity_code, number_races=len(links_of_matches))

        parse_result.entity = month
        parse_result.links[DataType.MATCH] = links_of_matches

        return parse_result