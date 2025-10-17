# horse_parser.py

from datetime import datetime
from typing import List

from bs4 import BeautifulSoup
from bs4.element import Tag

from ..utils.misc import parse_float, parse_int, parse_minsec, extract_cname_code, extract_doaction_code, extract_dd_horse, extract_class_jockey, extract_dd_trainer
from ..models.models import Horse, ResultOfHorse, DataType
from .base import BaseParser, ParseResult

class HorseParser(BaseParser):
    data_type = DataType.HORSE
    parser_name = data_type.value

    def _parse_impl(self, html: str, entity_code: str = None, entity_name: str = None, father_entity_code: str = None):
        """read the html string of a horse page"""

        parse_result = ParseResult[Horse]()

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
        else:
            rest = None
        
        # 抹消, whether deleted and the deleted date
        temp = soup.select_one("div.header_line.no-mb span.inner span.opt span")
        deleted = True if temp else False
        if deleted:
            deleted_date = datetime.strptime(temp.get_text(strip=True).replace("抹消年月日", "").strip(), "%Y年%m月%d日") if temp else None
        else:
            deleted_date = None

        # read the table of baisc informations
        temps: List[Tag] = list(soup.select("div.profile.mt20 li"))
        for item in temps:
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
                case "生産者":
                    birth_place = value

        # read the table of prize
        temps: List[Tag] = list(soup.select("div.prize.mt10 li.div2"))
        for item in temps:
            key = item.select_one("dt").get_text(strip=True)
            unit = item.select_one("dd span").get_text(strip=True)
            assert (unit == "円"), f"the unit of prize for {key} is not 円"
            value = item.select_one("dd").get_text(strip=True).replace(unit, "").replace(",", "")
            match key:
                case "総賞金":
                    prize_total = parse_int(value)
                case "内付加賞":
                    prize_fujia = parse_int(value)
                case "内地方賞金":
                    prize_difang = parse_int(value)
                case "内海外賞金":
                    prize_haiwai = parse_int(value)
                case "収得賞金（平地）":
                    prize_pingdi = parse_int(value)
                case "収得賞金（障害）":
                    prize_zhanghai = parse_int(value)

        # find the table "出走レース"
        result_table = soup.select_one("table.basic.narrow-xy.striped")

        # read the race code and arrival order of the horse in the race
        result_table_rows: List[Tag] = list(result_table.select("tbody tr"))
        result_list: List[ResultOfHorse] = []
        for row in result_table_rows:
            if row.select_one("td.race") is None:
                continue
            columns: List[Tag] = list(row.select("td"))
            date = datetime.strptime(columns[0].get_text(strip=True), "%Y年%m月%d日")
            place = columns[1].get_text(strip=True)
            race_name = columns[2].get_text(strip=True)
            temp = columns[2].select_one("a[href]")
            race_code = extract_cname_code(temp["href"]) if temp else None
            surface_distance = columns[3].get_text(strip=True)
            condition = columns[4].get_text(strip=True)
            num_of_horses = parse_int(columns[5].get_text(strip=True))
            pop_str = columns[6].get_text(strip=True)
            pop = parse_int(pop_str)
            arrival_order_str = columns[7].get_text(strip=True)
            jockey_name = columns[8].get_text(strip=True)
            temp = columns[8].select_one("a[onclick]")
            jockey_code = extract_doaction_code(temp["onclick"]) if temp else None
            weight = parse_float(columns[9].get_text(strip=True))
            horse_weight = parse_float(columns[10].get_text(strip=True))
            # horse_weight may be 計不
            time = parse_minsec(columns[11].get_text(strip=True))
            rt = columns[12].get_text(strip=True)
            # define the result
            result = ResultOfHorse(horse_code=entity_code, date=date, place=place, race_name=race_name, race_code=race_code, surface_distance=surface_distance, condition=condition, num_of_horses=num_of_horses, pop=pop, arrival_order_str=arrival_order_str, jockey_code=jockey_code, jockey_name=jockey_name, weight=weight, horse_weight=horse_weight, time=time, rt=rt)
            result_list.append(result)

        # define the horse
        horse = Horse(code=entity_code, name=name, name_en=name_en, rest=rest, deleted=deleted, deleted_date=deleted_date, father_code=father_code, father_name=father_name, mother_code=mother_code, mother_name=mother_name, father_of_mother_code=father_of_mother_code, father_of_mother_name=father_of_mother_name, mother_of_mother_code=mother_of_mother_code, mother_of_mother_name=mother_of_mother_name, sex=sex, birth_date=birth_date, color=color, owner=owner, trainer_code=trainer_code, trainer_name=trainer_name, trainer_affiliation=trainer_affiliation, birth_place=birth_place, prize_total=prize_total, prize_fujia=prize_fujia, prize_difang=prize_difang, prize_haiwai=prize_haiwai, prize_pingdi=prize_pingdi, prize_zhanghai=prize_zhanghai, _result_list=result_list)

        parse_result.entity = horse
        return parse_result
