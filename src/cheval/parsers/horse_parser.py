# horse_parser.py

import re
from datetime import datetime
from typing import Dict

from bs4 import BeautifulSoup
from bs4.element import Tag

from utils import minsec_to_sec, extract_class_race, extract_class_jockey, extract_dd_horse, extract_dd_trainer
from src.cheval.models.models import Horse, ResultOfHorse

class HorseParser:
    def __init__(self):
        pass

    def parse(self, html: str, horse_code: str = None):
        """read the html string of a horse page,
        return the Horse instance that records the information read"""

        soup = BeautifulSoup(html, "html.parser")

        # read the name of horse
        temp = soup.select_one("div.header_line.no-mb span.txt")
        name_en = temp.select_one("span.name_en").get_text(strip=True)
        name = temp.get_text(strip=True).replace("競走馬情報", "").replace(name_en, "")
        name = name
        name_en = name_en
        if temp.select_one("span.rest"):
            rest = temp.select_one("span.rest").get_text(strip=True)
            name = name.replace(rest, "")

        # read the table of baisc informations
        temp = soup.select("div.profile.mt20 li")
        for item in temp:
            value = item.select_one("dd").get_text(strip=True)
            key = item.get_text(strip=True).replace(value, "")
            match key:
                case "父":
                    father_code, father_name = extract_dd_horse(str(item.select_one("dd")))
                case "母":
                    mother_code, mother_name = extract_dd_horse(str(item.select_one("dd")))
                case "母の父":
                    father_of_mother_code, father_of_mother_name = extract_dd_horse(str(item.select_one("dd")))
                case "母の母":
                    mother_of_mother_code, mother_of_mother_name = extract_dd_horse(str(item.select_one("dd")))
                case "性別":
                    sex = value
                case "生年月日":
                    birth_date = datetime.strptime(value, "%Y年%m月%d日")
                case "毛色":
                    color = value
                case "馬主名":
                    owner = value
                case "調教師名":
                    trainer_code, trainer_name, trainer_affiliation = extract_dd_trainer(str(item.select_one("dd")))
                case "生産牧場":
                    birth_place = value

        # read the table of prize
        temp = soup.select("div.prize.mt10 li.div2")
        for item in temp:
            key = item.select_one("dt").get_text(strip=True)
            unit = item.select_one("dd span").get_text(strip=True)
            assert (unit == "円"), f"the unit of prize for {key} is not 円"
            value = item.select_one("dd").get_text(strip=True).replace(unit, "").replace(",", "")
            match key:
                case "総賞金":
                    prize_total = int(value)
                    """self.basic_info.set_info(horse_prize_total=int(value))"""
                case "内付加賞":
                    prize_fujia = int(value)
                    """self.basic_info.set_info(horse_prize_fujia=int(value))"""
                case "内地方賞金":
                    prize_difang = int(value)
                    """self.basic_info.set_info(horse_prize_difang=int(value))"""
                case "内海外賞金":
                    prize_haiwai = int(value)
                    """self.basic_info.set_info(horse_prize_haiwai=int(value))"""
                case "収得賞金（平地）":
                    prize_pingdi = int(value)
                    """self.basic_info.set_info(horse_prize_pingdi=int(value))"""
                case "収得賞金（障害）":
                    prize_zhanghai = int(value)
                    """self.basic_info.set_info(horse_prize_zhanghai=int(value))"""

        # define the horse
        horse = Horse(code=horse_code, name=name, name_en=name_en, rest=rest, father_code=father_code, father_name=father_name, mother_code=mother_code, mother_name=mother_name, father_of_mother_code=father_of_mother_code, father_of_mother_name=father_of_mother_name, mother_of_mother_code=mother_of_mother_code, mother_of_mother_name=mother_of_mother_name, sex=sex, birth_date=birth_date, color=color, owner=owner, trainer_code=trainer_code, trainer_name=trainer_name, trainer_affiliation=trainer_affiliation, birth_place=birth_place, prize_total=prize_total, prize_fujia=prize_fujia, prize_difang=prize_difang, prize_haiwai=prize_haiwai, prize_pingdi=prize_pingdi, prize_zhanghai=prize_zhanghai)

        # find the table "出走レース"
        result_table = soup.select_one("table.basic.narrow-xy.striped")

        # read the race code and arrival order of the horse in the race
        rows = result_table.select("tbody tr")
        for row in rows:
            columns = row.select("td")
            date = datetime.strptime(columns[0].get_text(strip=True), "%Y年%m月%d日")
            place = columns[1].get_text(strip=True)
            code, name = extract_class_race(str(columns[2]))
            surface_distance = columns[3].get_text(strip=True)
            condition = columns[4].get_text(strip=True)
            num_of_horses = int(columns[5].get_text(strip=True))
            pop_str = columns[6].get_text(strip=True)
            pop = int(pop_str) if pop_str else 0
            arrival_order_str = columns[7].get_text(strip=True)
            jockey_code, jockey_name = extract_class_jockey(str(columns[8]))
            weight = float(columns[9].get_text(strip=True)) if columns[9].get_text(strip=True) else float(0.0)
            horse_weight = float(columns[10].get_text(strip=True)) if columns[10].get_text(strip=True) else float(0.0)
            time = minsec_to_sec(columns[11].get_text(strip=True)) if columns[11].get_text(strip=True) else float(0.0)
            rt = columns[12].get_text(strip=True)
            # define the result
            result = ResultOfHorse(date=date, place=place, name=name, code=code, surface_distance=surface_distance, condition=condition, num_of_horses=num_of_horses, pop=pop, arrival_order_str=arrival_order_str, jockey_code=jockey_code, jockey_name=jockey_name, weight=weight, horse_weight=horse_weight, time=time, rt=rt)
            horse.results.append(result)

        return horse
