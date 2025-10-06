# match_list_parser.py

import re
from datetime import datetime
from typing import Dict, List

from bs4 import BeautifulSoup
from bs4.element import Tag

from ..utils.misc import extract_doaction_code
from ..models.models import CodeNameLinkAction, DataType
from .base import BaseParser, ParseResult

class MatchListParser(BaseParser):
    data_type = DataType.MATCH_LIST
    parser_name = data_type.value

    """
    def __init__(self):
        pass
    """

    def _parse_impl(self, html: str, entity_code: str = None, entity_name: str = None) -> ParseResult[None]:
        """read the html string of a match list, and save the informations;
        return the links of matches if return_links=True"""

        links_of_matches: List[CodeNameLinkAction] = []
        parse_result = ParseResult[None]()

        soup = BeautifulSoup(html, "html.parser")

        # read the table of matches
        matches: List[Tag] = list(soup.select("div.past_result_line_unit div.link_list.multi.div3.mid.center.narrow a"))
        for thematch in matches:
            name = thematch.get_text(strip=True)
            action = str(thematch["onclick"])
            code = extract_doaction_code(action)
            links_of_matches.append(CodeNameLinkAction(thetype=DataType.MATCH, code=code, name=name, action=action))

        parse_result.links[DataType.MATCH] = links_of_matches

        return parse_result