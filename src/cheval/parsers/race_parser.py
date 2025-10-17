# race_parser.py

import re
from datetime import datetime
from typing import List

from bs4 import BeautifulSoup
from bs4.element import Tag

from ..utils.misc import extract_cname_code, extract_doaction_code, parse_float, parse_int, parse_minsec
from ..models.models import Race, Prize, ResultOfRace, CodeNameLinkAction, DataType
from .base import BaseParser, ParseResult

class RaceParser(BaseParser):
    data_type = DataType.RACE
    parser_name = data_type.value

    def _parse_impl(self, html: str, entity_code: str = None, entity_name: str = None, father_entity_code: str = None):
        """read the html string of a race, and save the informations"""

        links_of_horses: List[CodeNameLinkAction] = []
        links_of_jockeys: List[CodeNameLinkAction] = []
        links_of_trainers: List[CodeNameLinkAction] = []
        parse_result = ParseResult[Race]()

        soup = BeautifulSoup(html, "html.parser")

        # read the date
        temp = soup.select_one("div.race_header div.date_line div.cell.date")
        date = datetime.strptime(temp.get_text(strip=True).split("（")[0], "%Y年%m月%d日") if temp else None

        # read the start time
        temp = soup.select_one("div.race_header div.date_line div.cell.time strong")
        if temp is None:
            time = None
        else:
            time_text = temp.get_text(strip=True)
            [hour, minute] = time_text.replace("分", "").split("時")
            time = date.replace(hour=int(hour), minute=int(minute))

        # read the weather
        temp = soup.select_one("div.race_header li.weather span.txt")
        weather = temp.get_text(strip=True) if temp else None

        # read the condition of the surface
        # some race has two surfaces and two conditions
        temp = soup.select_one("div.race_header li.turf span.txt")
        turf_condition = temp.get_text(strip=True) if temp else None
        temp = soup.select_one("div.race_header li.durt span.txt")
        dirt_condition = temp.get_text(strip=True) if temp else None
        
        # read the index of the race
        temp = soup.select_one("div.race_header div.race_title div.race_number img[alt]")
        index = parse_int(str(temp.get("alt")).replace("レース", "")) if temp else None
        
        # read the title of the race
        temp = soup.select_one("div.race_header div.race_title span.race_name")
        title = temp.get_text(strip=True) if temp else None
        if title == entity_name:
            title = ""
        
        # read the category of the race
        temp = soup.select_one("div.race_header div.race_title div.cell.category")
        category = temp.get_text(strip=True) if temp else None

        # read the class of the race
        temp = soup.select_one("div.race_header div.race_title div.cell.class")
        theclass = temp.get_text(strip=True) if temp else None

        # read the rule of the race
        temp = soup.select_one("div.race_header div.race_title div.cell.rule")
        rule = temp.get_text(strip=True) if temp else None

        # read the weight of the race
        temp = soup.select_one("div.race_header div.race_title div.cell.weight")
        weight = temp.get_text(strip=True) if temp else None

        # read the detail of the course
        temp = soup.select_one("div.race_header div.race_title div.cell.course span.detail")
        course_detail = re.sub("（|）", "", temp.get_text(strip=True)) if temp else None
        surface = course_detail.split("・")[0] if course_detail else None

        # read the distance and its unit of the race
        temp = soup.select_one("div.race_header div.race_title div.cell.course")
        distance = int(''.join(temp.find_all(text=True, recursive=False)).strip().replace(",", "")) if temp else None
        temp = temp.select_one("span.unit")
        distance_unit = temp.get_text(strip=True) if temp else None
        
        # read the prizes of the race
        # some races have more than one lists of prizes
        temps: List[Tag] = list(soup.select("div.race_header ul.prize div.prize_unit"))
        prize_list: List[Prize] = []
        for prize_tag in temps:
            temp = prize_tag.select_one("div.cell.cap")
            prize_name = temp.get_text(strip=True) if temp else None
            temp = prize_tag.select_one("span.unit")
            prize_unit = temp.get_text(strip=True) if temp else None
            prize_name = prize_name.replace(prize_unit, "") if prize_unit else None
            prize_unit = re.sub("（|）", "", prize_unit) if prize_unit else None
            prize_data = [parse_float(num.get_text(strip=True).replace(",", "")) for num in prize_tag.select("span.num")]
            race_prize = Prize(name=prize_name, unit=prize_unit, data=prize_data)
            prize_list.append(race_prize)

        # read the result of every horse in the race
        temps: List[Tag] = list(soup.select('table.basic.narrow-xy.striped tbody tr'))
        number_horses_in_race = len(temps)
        result_list: List[ResultOfRace] = []
        for result_tag in temps:
            # 着順, or "place" called by the html
            # special values: '失格', '中止', '除外', '取消'
            temp = result_tag.select_one("td.place")
            arrival_order_str = temp.get_text(strip=True) if temp else None
            # 枠
            temp = result_tag.select_one("td.waku img[alt]")
            if temp is None:
                waku = None
                waku_color = None
            else:
                temp_str = str(temp.get("alt"))
                waku_str = str(re.findall("\d+", temp_str)[0])
                waku = parse_int(waku_str)
                waku_color = temp_str.replace("枠", "").replace(waku_str, "")
            # 馬番
            temp = result_tag.select_one("td.num")
            num = parse_int(temp.get_text(strip=True))
            # 馬名, its code and link
            temp = result_tag.select_one("td.horse a")
            horse_name = temp.get_text(strip=True) if temp else None
            if temp and ("href" in temp.attrs):
                horse_link = str(temp["href"])
                horse_code = extract_cname_code(horse_link)
                links_of_horses.append(CodeNameLinkAction(thetype=DataType.HORSE, code=horse_code, name=horse_name, link=horse_link))
            else:
                horse_link = None
                horse_code = None
            # 性齢
            temp = result_tag.select_one("td.age")
            sex_and_age = temp.get_text(strip=True) if temp else None
            # 負担重量
            temp = result_tag.select_one("td.weight")
            weight = parse_float(temp.get_text(strip=True)) if temp else None
            # 騎手名 and his/her code, the code may not exist
            temp = result_tag.select_one("td.jockey a")
            jockey_name = temp.get_text(strip=True) if temp else None
            if temp and ("onclick" in temp.attrs):
                jockey_code = extract_doaction_code(temp["onclick"])
                jockey_action = temp["onclick"]
                #jockey_action = temp["onclick"].replace("return ", "")
                links_of_jockeys.append(CodeNameLinkAction(thetype=DataType.JOCKEY, code=jockey_code, name=jockey_name, action=jockey_action))
            else:
                jockey_code = None
                jockey_action = None
            # タイム, the value in html may be an empty string
            temp = result_tag.select_one("td.time")
            time_for_race_result = parse_minsec(temp.get_text(strip=True)) if temp else None
            # 着差
            margin = result_tag.select_one("td.margin").get_text(strip=True)
            # コーナー通過順位, the values in html may be empty strings
            corner_list_tags: List[Tag] = list(result_tag.select("div.corner_list li"))
            corner_list = [parse_int(li.get_text(strip=True)) for li in corner_list_tags]
            #temp = result_tag.select("div.corner_list li")
            #corner_list = [int(li.get_text(strip=True)) if li.get_text(strip=True) else None for li in temp]
            # 平均1F or 推定上り, the value in html may be an empty string
            temp = result_tag.select_one("td.f_time")
            f_time = parse_float(temp.get_text(strip=True)) if temp else None
            # 馬体重（増減）, the value of 増減 in html may be empty
            temp = result_tag.select_one("td.h_weight")
            if temp is None:
                horse_weight = None
                horse_weight_delta = None
            else:
                horse_weight = parse_float(temp.contents[0]) if len(temp.contents) > 0 else None
                horse_weight_delta = parse_float(re.sub("\(|\)", "", temp.contents[1].text)) if len(temp.contents) > 1 else None
            '''
            horse_weight = temp.contents[0]
            try:
                horse_weight = float(horse_weight)
            except:
                horse_weight = None #BasicInfo.Result.HORSE_WEIGHT_EMPTY
            try:
                horse_weight_delta = float(re.sub("\(|\)", "", temp.contents[1].text))
            except:
                horse_weight_delta = None #BasicInfo.Result.HORSE_WEIGHT_DELTA_EMPTY
            '''
            # 調教師名 and his/her code, the code may not exist
            temp = result_tag.select_one("td.trainer a")
            trainer_name = temp.get_text(strip=True) if temp else None
            if temp and ("onclick" in temp.attrs):
                trainer_code = extract_doaction_code(temp["onclick"])
                trainer_action = temp["onclick"]
                links_of_trainers.append(CodeNameLinkAction(thetype=DataType.TRAINER, code=trainer_code, name=trainer_name, action=trainer_action))
            else:
                trainer_code = None
                trainer_action = None
            # 単勝人気, the value in html may be an empty string
            temp = result_tag.select_one("td.pop")
            pop = parse_int(temp.get_text(strip=True)) if temp else None
            # ブリンカー
            blinker = True if result_tag.select_one("td.horse div.icon.blinker") else False
            # icon, 馬に付く記号
            temp = result_tag.select_one("td.horse span.horse_icon img[alt]")
            horse_icon = temp["alt"] if temp else None

            race_result: ResultOfRace = ResultOfRace(race_code=entity_code, arrival_order_str=arrival_order_str, waku=waku, waku_color=waku_color, num=num, horse_code=horse_code, horse_name=horse_name, horse_icon=horse_icon, blinker=blinker, sex_and_age=sex_and_age, weight=weight, jockey_code=jockey_code, jockey_name=jockey_name, time=time_for_race_result, margin=margin, f_time=f_time, horse_weight=horse_weight, horse_weight_delta=horse_weight_delta, trainer_code=trainer_code, trainer_name=trainer_name, pop=pop, _corner_list=corner_list)
            result_list.append(race_result)

        race: Race = Race(code=entity_code, match_code=father_entity_code, name=entity_name, title=title, index=index, distance=distance, distance_unit=distance_unit, surface=surface, number_horses_in_race=number_horses_in_race, time=time, weather=weather, turf_condition=turf_condition, dirt_condition=dirt_condition, category=category, theclass=theclass, rule=rule, weight=weight, course_detail=course_detail, _prize_list=prize_list, _result_list=result_list)

        parse_result.entity = race
        parse_result.links[DataType.HORSE] = links_of_horses
        parse_result.links[DataType.JOCKEY] = links_of_jockeys
        parse_result.links[DataType.TRAINER] = links_of_trainers
        return parse_result