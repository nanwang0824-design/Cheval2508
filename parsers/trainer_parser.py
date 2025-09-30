# trainer_parser.py

import re
from datetime import datetime
from typing import Dict, List, Optional

from bs4 import BeautifulSoup
from bs4.element import Tag

from models import Trainer, SummaryOfJockeyTrainer
from parsers.jockey_parser import JockeyParser

class TrainerParser:
    def __init__(self):
        pass

    def parse(self, html: str, trainer_code: str = None):
        """read the html string of a trainer page,
        return the Trainer instance that records the information read"""

        soup = BeautifulSoup(html, "html.parser")

        # read the name of trainer
        temp = soup.select_one("div.header_line.no-mb span.txt")
        name_kana = temp.select_one("span.kana").get_text(strip=True)
        name = temp.get_text(strip=True).replace("調教師情報", "").replace(name_kana, "")
        name_kana = name_kana.replace("（", "").replace("）", "")

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

        trainer = Trainer(code=trainer_code, name=name, name_kana=name_kana, birth_date=birth_date, birth_place=birth_place, license_acquisition_year=license_acquisition_year, affiliation=affiliation, first_race=first_race, first_victory=first_victory)

        # read the table of year_record 本年成績
        temp = soup.select_one("#year_record")
        trainer.summary_this_year = self._read_summary_table(tag=temp)

        # read the table of year_record 本年成績
        temp = soup.select_one("#total_record")
        trainer.summary_total = self._read_summary_table(temp)

        return trainer

    def parse_for_past(self, html: str):
        """read the html string of a trainer past results page,
        return the list of SummaryOfJockeyTrainer instances that records the information read"""

        soup = BeautifulSoup(html, "html.parser")

        results: List[SummaryOfJockeyTrainer] = []

        tables = soup.select("table.basic.narrow.mt15, table.basic.narrow.mt40")
        for table in tables:
            self._read_summary_table(tag=table, append_list=results, append=True)

        return results

    def _read_summary_table(self, tag: Tag, append_list: List[SummaryOfJockeyTrainer] = None, append: bool = False):
        temp = JockeyParser()
        return temp._read_summary_table(tag=tag, append_list=append_list, append=append)