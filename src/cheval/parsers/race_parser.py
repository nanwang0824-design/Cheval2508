# race_parser.py

import re
from datetime import datetime
from typing import List

from bs4 import BeautifulSoup
from bs4.element import Tag

from ..utils.misc import extract_doaction_code
from ..models.models import Race, Prize, ResultOfRace, CodeNameLinkAction

class RaceParser:

    def __init__(self):
        pass

    def parse(self, html: str, race_code: str = None, race_name: str = None, return_links: bool = True):
        """read the html string of a race, and save the informations;
        return the links of horses, jockeys and trainers if return_links=True"""

        links_of_horses: List[CodeNameLinkAction] = []
        links_of_jockeys: List[CodeNameLinkAction] = []
        links_of_trainers: List[CodeNameLinkAction] = []

        soup = BeautifulSoup(html, "html.parser")

        # read the date
        temp = soup.select_one("div.race_header div.date_line div.cell.date")
        date = datetime.strptime(temp.get_text(strip=True).split("（")[0], "%Y年%m月%d日")

        # read the start time
        temp = soup.select_one("div.race_header div.date_line div.cell.time strong")
        time_text = temp.get_text(strip=True)
        [hour, minute] = time_text.replace("分", "").split("時")
        time = date.replace(hour=int(hour), minute=int(minute))

        # read the weather
        temp = soup.select_one("div.race_header li.weather span.txt")
        weather = temp.get_text(strip=True)

        # read the condition of the surface
        # some races have two surfaces and two conditions
        temp = soup.select_one("div.race_header li.turf span.txt")
        turf_condition = temp.get_text(strip=True) if temp else ""
        temp = soup.select_one("div.race_header li.durt span.txt")
        dirt_condition = temp.get_text(strip=True) if temp else ""
        
        # read the index of the race
        temp = soup.select_one("div.race_header div.race_title div.race_number img")
        index = int(str(temp["alt"]).replace("レース", ""))
        
        # read the title of the race
        temp = soup.select_one("div.race_header div.race_title span.race_name")
        title = temp.get_text(strip=True)
        if title == race_name:
            title = ""
        
        # read the category of the race
        temp = soup.select_one("div.race_header div.race_title div.cell.category")
        category = temp.get_text(strip=True)

        # read the class of the race
        temp = soup.select_one("div.race_header div.race_title div.cell.class")
        theclass = temp.get_text(strip=True)

        # read the rule of the race
        temp = soup.select_one("div.race_header div.race_title div.cell.rule")
        rule = temp.get_text(strip=True)

        # read the weight of the race
        temp = soup.select_one("div.race_header div.race_title div.cell.weight")
        weight = temp.get_text(strip=True)

        # read the detail of the course
        temp = soup.select_one("div.race_header div.race_title div.cell.course span.detail")
        course_detail = temp.get_text(strip=True)
        course_detail = re.sub("（|）", "", course_detail)
        surface = course_detail.split("・")[0]

        # read the distance and its unit of the race
        temp = soup.select_one("div.race_header div.race_title div.cell.course")
        distance = int(''.join(temp.find_all(text=True, recursive=False)).strip().replace(",", ""))
        distance_unit = temp.select_one("span.unit").get_text(strip=True)

        race = Race(code=race_code, name=race_name, title=title, index=index, distance=distance, distance_unit=distance_unit, surface=surface, number_horses_in_race=None, time=time, weather=weather, turf_condition=turf_condition, dirt_condition=dirt_condition, category=category, theclass=theclass, rule=rule, weight=weight, course_detail=course_detail)

        """
        # write the informations obtained above
        self.basic_info.set_info(hour=int(hour),
                                 minute=int(minute),
                                 weather=weather,
                                 turf_condition=turf_condition,
                                 dirt_condition=dirt_condition,
                                 race_category=category,
                                 race_class=theclass,
                                 race_rule=rule,
                                 race_weight=weight,
                                 race_course_detail=course_detail)
        """
        
        # read the prizes of the race
        # some races have two or more lists of prizes
        prizes = soup.select("div.race_header ul.prize div.prize_unit")
        for prize in prizes:
            prize_name = prize.select_one("div.cell.cap").get_text(strip=True)
            prize_unit = prize.select_one("span.unit").get_text(strip=True)
            prize_name = prize_name.replace(prize_unit, "")
            prize_unit = re.sub("（|）", "", prize_unit)
            prize_list = [float(num.get_text(strip=True).replace(",", "")) for num in prize.select("span.num")]
            race_prize = Prize(name=prize_name, unit=prize_unit, data=prize_list)
            race.prize_list.append(race_prize)
            #race_prize = BasicInfo.Prize(name=prize_name, unit=prize_unit, prize_list=prize_list)
            #self.basic_info.append_prize(race_prize)

        # read the result of every horse in the race
        results: List[Tag] = list(soup.select('table.basic.narrow-xy.striped tbody tr'))
        number_horses_in_race = len(results)
        race.number_horses_in_race = number_horses_in_race
        for result in results:
            # 着順, or "place" called by the html
            # special values: '失格', '中止', '除外', '取消'
            arrival_order = result.select_one("td.place").get_text(strip=True)
            #print(f"\t\t\t the horse with arrival order={arrival_order}.")
            # 枠
            temp = result.select_one("td.waku img")["alt"].replace("枠", "")
            waku = re.findall("\d+", temp)[0]
            waku_color = temp.replace(waku, "")
            waku = int(waku)
            # 馬番
            num = int(result.select_one("td.num").get_text(strip=True))
            # 馬名, its code and link
            temp = result.select_one("td.horse a")
            horse_link = temp["href"] # if (temp and "href" in temp.attrs) else None
            horse_code = horse_link.split("=")[1]
            horse_name = temp.get_text(strip=True)
            if return_links:
                links_of_horses.append(CodeNameLinkAction(code=horse_code, name=horse_name, link=horse_link))
            # 性齢
            sex_and_age = result.select_one("td.age").get_text(strip=True)
            # 負担重量
            weight = float(result.select_one("td.weight").get_text(strip=True))
            # 騎手名 and his/her code, the code may not exist
            temp = result.select_one("td.jockey a")
            if temp:
                jockey_code = extract_doaction_code(temp["onclick"])
                jockey_name = temp.get_text(strip=True)
                jockey_action = temp["onclick"].replace("return ", "")
                if return_links:
                    links_of_jockeys.append(CodeNameLinkAction(code=jockey_code, name=jockey_name, action=jockey_action))
                    #links_of_jockeys[jockey_code] = temp["onclick"].replace("return ", "")
            else:
                jockey_code = None #BasicInfo.Result.JOCKEY_CODE_EMPTY
                jockey_name = result.select_one("td.jockey").get_text(strip=True)
            # タイム, the value in html may be an empty string
            temp = result.select_one("td.time").get_text(strip=True)
            if temp:
                temp = temp.split(":")
                time = float(temp[0]) * 60 + float(temp[1])
            else:
                time = None #BasicInfo.Result.TIME_EMPTY
            # 着差
            margin = result.select_one("td.margin").get_text(strip=True)
            # コーナー通過順位, the values in html may be empty strings
            temp = result.select("div.corner_list li")
            #corner_list = [int(li.get_text(strip=True)) if li.get_text(strip=True) else BasicInfo.Result.CORNER_LIST_ITME_EMPTY for li in temp]
            corner_list = [int(li.get_text(strip=True)) if li.get_text(strip=True) else None for li in temp]
            # 平均1F or 推定上り, the value in html may be an empty string
            temp = result.select_one("td.f_time")
            f_time = float(temp.get_text(strip=True)) if temp.get_text(strip=True) else None #BasicInfo.Result.F_TIME_EMPTY
            # 馬体重（増減）, the value of 増減 in html may be empty
            temp = result.select_one("td.h_weight")
            horse_weight = temp.contents[0]
            try:
                horse_weight = float(horse_weight)
            except:
                horse_weight = None #BasicInfo.Result.HORSE_WEIGHT_EMPTY
            try:
                horse_weight_delta = float(re.sub("\(|\)", "", temp.contents[1].text))
            except:
                horse_weight_delta = None #BasicInfo.Result.HORSE_WEIGHT_DELTA_EMPTY
            # 調教師名 and his/her code, the code may not exist
            temp = result.select_one("td.trainer a")
            if temp:
                trainer_code = extract_doaction_code(temp["onclick"])
                trainer_name = temp.get_text(strip=True)
                trainer_action = temp["onclick"].replace("return ", "")
                if return_links:
                    links_of_trainers.append(CodeNameLinkAction(code=trainer_code, name=trainer_name, action=trainer_action))
                    #links_of_trainers[trainer_code] = temp["onclick"].replace("return ", "")
            else:
                trainer_code = None #BasicInfo.Result.TRAINER_CODE_EMPTY
                trainer_name = result.select_one("td.trainer").get_text(strip=True)
            # 単勝人気, the value in html may be an empty string
            temp = result.select_one("td.pop")
            pop = int(temp.get_text(strip=True)) if temp.get_text(strip=True) else None #BasicInfo.Result.POP_EMPTY
            # ブリンカー
            #temp = result.select_one("td.horse div.icon.blinker")
            blinker = True if result.select_one("td.horse div.icon.blinker") else False
            # ブリンカー
            temp = result.select_one("td.horse span.horse_icon img")
            horse_icon = temp["alt"] if temp else None

            race_result = ResultOfRace(race_code=race_code, arrival_order_str=arrival_order, waku=waku, waku_color=waku_color, num=num, horse_code=horse_code, horse_name=horse_name, horse_icon=horse_icon, blinker=blinker, sex_and_age=sex_and_age, weight=weight, jockey_code=jockey_code, jockey_name=jockey_name, time=time, margin=margin, corner_list=corner_list, f_time=f_time, horse_weight=horse_weight, horse_weight_delta=horse_weight_delta, trainer_code=trainer_code, trainer_name=trainer_name, pop=pop)
            #print(race_result)
            race.result_list.append(race_result)

            """
            # generate the result of this horse and append it to the list of results
            race_result = BasicInfo.Result(arrival_order=arrival_order, 
                                           waku=waku, 
                                           waku_color=waku_color, 
                                           num=num, 
                                           horse_code=horse_code, 
                                           horse_name=horse_name, 
                                           blinker=blinker,
                                           age=age, weight=weight, 
                                           jockey_code=jockey_code, 
                                           jockey_name=jockey_name, 
                                           time=time, 
                                           margin=margin, 
                                           corner_list=corner_list, 
                                           f_time=f_time, 
                                           horse_weight=horse_weight, 
                                           horse_weight_delta=horse_weight_delta, 
                                           trainer_code=trainer_code, 
                                           trainer_name=trainer_name, 
                                           pop=pop)
            self.basic_info.append_result(race_result)
        #self.basic_info.print()
        """

        #print(race)

        return race, links_of_horses, links_of_jockeys, links_of_trainers