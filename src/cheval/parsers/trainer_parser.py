# trainer_parser.py

import re
from datetime import datetime
from typing import Dict, List, Optional

from bs4 import BeautifulSoup
from bs4.element import Tag

from ..models.models import Trainer, SummaryOfJockeyTrainer, DataType, CodeNameLinkAction
from ..utils.misc import extract_doaction_code
from .base import BaseParser, ParseResult
from .jockey_parser import JockeyParser

class TrainerParser(BaseParser):
    data_type = DataType.TRAINER
    parser_name = data_type.value

    """
    def __init__(self):
        pass
    """

    def _parse_impl(self, html: str, entity_code: str = None, entity_name: str = None, father_entity_code: str = None):
        """read the html string of a trainer page"""

        soup = BeautifulSoup(html, "html.parser")
        parse_result = ParseResult[Trainer]()

        # read the name of trainer
        temp = soup.select_one("div.header_line.no-mb span.txt")
        name_kana = temp.select_one("span.kana").get_text(strip=True)
        name = temp.get_text(strip=True).replace("調教師情報", "").replace(name_kana, "")
        name_kana = name_kana.replace("（", "").replace("）", "")
        retired = True if temp.select_one("span.retired") else False
        if retired:
            name = name.replace("引退", "", 1)

        # read the table of baisc informations
        temp = soup.select("div.main.mt15 div.profile div.data dl")
        for term in temp:
            key = term.select_one("dt").get_text(strip=True)
            value = term.select_one("dd")
            match key:
                case "生年月日":
                    birth_date = datetime.strptime(value.get_text(strip=True), "%Y年%m月%d日")
                case "出身地":
                    birth_place = value.get_text(strip=True)
                case "免許取得年":
                    license_acquisition_year = int(value.get_text(strip=True).replace("年", ""))
                case "所属":
                    affiliation = value.get_text(strip=True)
                case "初出走":
                    first_race = value.get_text(strip=True)
                case "初勝利":
                    first_victory = value.get_text(strip=True)

        # read the table of year_record 本年成績
        temp = soup.select_one("#year_record")
        if temp is not None:
            summary_this_year = self._read_summary_table(tag=temp, jockey_trainer_code=entity_code) if temp else []
        else:
            summary_this_year = []

        # read the table of year_record 累計成績
        temp = soup.select_one("#total_record")
        if temp is not None:
            summary_total = self._read_summary_table(temp, jockey_trainer_code=entity_code) if temp else []
        else:
            summary_total = []

        # link to 過去成績
        temp = soup.select_one("div.jockey_menu.mt30 li:has(a:-soup-contains('過去成績')) a")
        summary_action = temp["onclick"]
        summary_code = extract_doaction_code(summary_action)
        parse_result.links[DataType.TRAINER_SUMMARY] = [CodeNameLinkAction(thetype=DataType.TRAINER_SUMMARY, name=entity_name, code=summary_code, action=summary_action)]

        # defin the trainer
        trainer = Trainer(code=entity_code, name=name, name_kana=name_kana, retired=retired, birth_date=birth_date, birth_place=birth_place, license_acquisition_year=license_acquisition_year, affiliation=affiliation, first_race=first_race, first_victory=first_victory, _summary_this_year=summary_this_year, _summary_total=summary_total, summary_past_code=summary_code)

        parse_result.entity = trainer
        return parse_result

    @staticmethod
    def _read_summary_table(tag: Tag, append_list: List[SummaryOfJockeyTrainer] = None, append: bool = False, summary_code: str = None, jockey_trainer_code: str = None):
        return JockeyParser._read_summary_table(tag=tag, append_list=append_list, append=append, summary_code=summary_code, jockey_trainer_code=jockey_trainer_code)
    

class TrainerSummaryParser(BaseParser):
    data_type = DataType.TRAINER_SUMMARY
    parser_name = data_type.value

    """
    def __init__(self):
        pass
    """

    def _parse_impl(self, html: str, entity_code: str = None, entity_name: str = None, father_entity_code: str = None):
        """read the html string of a trainer summary page"""
        soup = BeautifulSoup(html, "html.parser")

        results: List[SummaryOfJockeyTrainer] = []
        parse_result = ParseResult[SummaryOfJockeyTrainer]()

        tables = soup.select("table.basic.narrow.mt15, table.basic.narrow.mt40")
        for table in tables:
            TrainerParser._read_summary_table(tag=table, append_list=results, append=True, summary_code=entity_code, jockey_trainer_code=father_entity_code)

        parse_result.history = results
        return parse_result