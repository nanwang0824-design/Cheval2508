# jockey_parser.py

import re
from datetime import datetime
from typing import Dict, List, Optional

from bs4 import BeautifulSoup
from bs4.element import Tag

from ..models.models import Jockey, SummaryOfJockeyTrainer, DataType
from .base import BaseParser, ParseResult

class JockeyParser(BaseParser):
    data_type = DataType.JOCKEY
    parser_name = data_type.value

    """
    def __init__(self):
        pass
    """

    def _parse_impl(self, html: str, entity_code: str = None, entity_name: str = None):
        """read the html string of a jockey page"""

        soup = BeautifulSoup(html, "html.parser")
        parse_result = ParseResult[Jockey]()

        # read the name of jockey
        temp = soup.select_one("div.header_line.no-mb span.txt")
        name_kana = temp.select_one("span.kana").get_text(strip=True)
        name = temp.get_text(strip=True).replace("騎手情報", "").replace(name_kana, "")
        name_kana = name_kana.replace("（", "").replace("）", "")

        # read the table of baisc informations
        temp = soup.select("div.main.mt15 div.profile div.data dl")
        for term in temp:
            key = term.select_one("dt").get_text(strip=True)
            value = term.select_one("dd")
            match key:
                case "生年月日":
                    birth_date = datetime.strptime(value.get_text(strip=True), "%Y年%m月%d日")
                case "身長":
                    height_unit = value.select_one("span.unit").get_text(strip=True)
                    height = float(value.get_text(strip=True).replace(height_unit, ""))
                case "体重":
                    weight_unit = value.select_one("span.unit").get_text(strip=True)
                    weight = float(value.get_text(strip=True).replace(weight_unit, ""))
                case "血液型":
                    blood_type = value.get_text(strip=True)
                case "初免許年":
                    first_license_year = int(value.get_text(strip=True).replace("年", ""))
                case "免許種類":
                    license_type = value.get_text(strip=True)
                case "出身地":
                    birth_place = value.get_text(strip=True)
                case "所属":
                    affiliation = value.get_text(strip=True)
                case "所属厩舎":
                    affiliated_stable = value.get_text(strip=True)
                case "初騎乗":
                    first_ride = value.get_text(strip=True)
                case "初勝利":
                    first_victory = value.get_text(strip=True)

        # define the jockey
        jockey = Jockey(code=entity_code, name=name, name_kana=name_kana, birth_date=birth_date, height=height, height_unit=height_unit, weight=weight, weight_unit=weight_unit, blood_type=blood_type, first_license_year=first_license_year, license_type=license_type, birth_place=birth_place, affiliation=affiliation, affiliated_stable=affiliated_stable, first_ride=first_ride, first_victory=first_victory)

        # read the table of year_record 本年成績
        temp = soup.select_one("#year_record")
        jockey.summary_this_year = self._read_summary_table(tag=temp)

        # read the table of year_record 本年成績
        temp = soup.select_one("#total_record")
        jockey.summary_total = self._read_summary_table(temp)

        parse_result.entity = jockey
        return parse_result

    def parse_for_past(self, html: str):
        """read the html string of a jockey past results page"""

        soup = BeautifulSoup(html, "html.parser")

        results: List[SummaryOfJockeyTrainer] = []

        tables = soup.select("table.basic.narrow.mt15, table.basic.narrow.mt40")
        for table in tables:
            self._read_summary_table(tag=table, append_list=results, append=True)

        return results

    @staticmethod
    def _read_summary_table(tag: Tag, append_list: List[SummaryOfJockeyTrainer] = None, append: bool = False):
        results: List[SummaryOfJockeyTrainer] = []
        title = tag.select_one("div.main").get_text(strip=True)
        for row in tag.select("tr"):
            type = row.select_one("th[scope='row']")
            if not type:
                continue
            type = type.get_text(strip=True)
            columns = [int(column.get_text(strip=True)) if i < 7 else (float(column.get_text(strip=True)) if column.get_text(strip=True) else None) for i, column in enumerate(row.select("td"))]
            summary = SummaryOfJockeyTrainer(title=title, type=type, num_no1=columns[0], num_no2=columns[1], num_no3=columns[2], num_no4=columns[3], num_no5=columns[4], num_out5=columns[5], num_rides=columns[6], winning_rate=columns[7], quinella_rate=columns[8], top3_rate=columns[9])
            results.append(summary)
            if append and (append_list is not None):
                append_list.append(summary)
        return results

class JockeySummaryParser(BaseParser):
    data_type = DataType.JOCKEY_SUMMARY
    parser_name = data_type.value

    """
    def __init__(self):
        pass
    """

    def _parse_impl(self, html: str, entity_code: str = None, entity_name: str = None):
        """read the html string of a jockey summary page"""

        soup = BeautifulSoup(html, "html.parser")
        parse_result = ParseResult[SummaryOfJockeyTrainer]()

        results: List[SummaryOfJockeyTrainer] = []

        tables = soup.select("table.basic.narrow.mt15, table.basic.narrow.mt40")
        for table in tables:
            JockeyParser._read_summary_table(tag=table, append_list=results, append=True)

        parse_result.history = results
        return parse_result