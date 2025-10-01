# models.py

import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from ..utils.misc import order_str_to_int, sexage_to_sex_age

@dataclass(slots=True, kw_only=True)
class CodeNameLinkAction:
    code: str = None
    name: str = None
    link: str = None
    action: str = None

@dataclass(slots=True, kw_only=True)
class SummaryOfJockeyTrainer:
    title: str = None
    "title of the summary table: 本年成績, 累計成績, 2024年, ..."
    type: str = None
    "type of the summary table: 平地, 障害, JRA合計, 地方, 海外, 総合計"
    num_no1: int = None
    "1着, number of no 1"
    num_no2: int = None
    "2着, number of no 2"
    num_no3: int = None
    "3着, number of no 3"
    num_no4: int = None
    "4着, number of no 4"
    num_no5: int = None
    "5着, number of no 5"
    num_out5: int = None
    "着外, number of outside the top 5"
    num_rides: int = None
    "騎乗回数, number of rides"
    winning_rate: float = None
    "勝率, winning rate"
    quinella_rate: float = None
    "連対率, quinella rate"
    top3_rate: float = None
    "3着内率, top 3 rate"
    update_time: datetime = None
    "date and time of update"

    def __post_init__(self):
        self.update_time = datetime.now()

@dataclass(slots=True, kw_only=True)
class Trainer:
    code: str = None
    "code of the trainer"
    name: str = None
    "name of trainer"
    name_kana: str = None
    "kana name of trainer"
    birth_date: datetime = None
    "生年月日, birthday of the trainer"
    birth_place: str = None
    "出身地, birth place of the trainer"
    license_acquisition_year: int = None
    "免許取得年, license acquisition year of the trainer"
    affiliation: str = None
    "所属, affiliation of the trainer"
    first_race: str = None
    "初出走, first race of the trainer"
    first_victory: str = None
    "初勝利, first victory of the trainer"
    summary_this_year: List[SummaryOfJockeyTrainer] = field(default_factory=list)
    "summary of the results in this year"
    summary_total: List[SummaryOfJockeyTrainer] = field(default_factory=list)
    "summary of the total results"
    summary_past: List[SummaryOfJockeyTrainer] = field(default_factory=list)
    "summary of the past results"
    update_time: datetime = None
    "date and time of update"

    def __post_init__(self):
        self.update_time = datetime.now()

@dataclass(slots=True, kw_only=True)
class Jockey:
    code: str = None
    "code of the jockey, example: pw04kmk001144/54"
    name: str = None
    "name of jockey"
    name_kana: str = None
    "kana name of jockey"
    birth_date: datetime = None
    "生年月日, birthday of the jockey"
    height: float = None
    "身長, height of the jockey"
    height_unit: str = None
    "height unit of the jockey, センチメートル"
    weight: float = None
    "体重, weight of the jockey"
    weight_unit: str = None
    "weight unit of the jockey, キログラム"
    blood_type: str = None
    "blood type of the jockey"
    first_license_year: int = None
    "初免許年, first license year of the jockey"
    license_type: str = None
    "免許種類, license type of the jockey"
    birth_place: str = None
    "出身地, birth place of the jockey"
    affiliation: str = None
    "所属, affiliation of the jockey"
    affiliated_stable: str = None
    "所属厩舎, affiliated stable of the jockey"
    first_ride: str = None
    "初騎乗, first ride of the jockey"
    first_victory: str = None
    "初勝利, first victory of the jockey"
    summary_this_year: List[SummaryOfJockeyTrainer] = field(default_factory=list)
    "summary of the results in this year"
    summary_total: List[SummaryOfJockeyTrainer] = field(default_factory=list)
    "summary of the total results"
    summary_past: List[SummaryOfJockeyTrainer] = field(default_factory=list)
    "summary of the past results"
    update_time: datetime = None
    "date and time of update"

    def __post_init__(self):
        self.update_time = datetime.now()

@dataclass(slots=True, kw_only=True)
class ResultOfHorse:
    date: datetime = None
    "年月日, date of the race"
    place: str = None
    "場, place of the race"
    name: str = None
    "レース名, name of the race"
    code: str = None
    "code of the race, may be an empty string"
    surface_distance: str = None
    "距離, surface and distance of the race, example: 芝2000, 芝ダ2910"
    condition: str = None
    "馬場, condition of the surface, example: 稍重, 良/良"
    num_of_horses: int = None
    "頭数, number of horses in the race"
    pop: int = None
    "人気, win popularity of the horse"
    arrival_order_str: str = None
    "着順, string of the arrival order"
    arrival_order: int = None
    "着順, arrival order, initialization is not necessary"
    jockey_code: str = None
    "code of the jockey"
    jockey_name: str = None
    "騎手名, name of the jockey"
    weight: float = None
    "負担重量, weight to carry of the horse"
    horse_weight: float = None
    "馬体重, horse weight"
    time: float = None
    "タイム, race time"
    rt: str = None
    "Rt, may be an empty string"
    update_time: datetime = None
    "date and time of update"

    def normalize(self):
        if self.arrival_order_str and (not self.arrival_order):
            self.arrival_order = order_str_to_int(self.arrival_order_str)

    def __post_init__(self):
        self.update_time = datetime.now()
        self.normalize()

@dataclass(slots=True, kw_only=True)
class Horse:
    code: str = None
    "code of the horse, example: pw01dud102022104401/B0"
    name: str = None
    "馬名, name of the horse"
    name_en: str = None
    "english name of the horse"
    rest: str = None
    "rest state of the horse, may be an empty string, expamle: 放牧"
    father_code: str = None
    "code of the father of the horse, may be an empty string"
    father_name: str = None
    "父, name of the father of the horse"
    mother_code: str = None
    "code of the mother of the horse, may be an empty string"
    mother_name: str = None
    "母, name of the mother of the horse"
    father_of_mother_code: str = None
    "code of the father of mother of the horse, may be an empty string"
    father_of_mother_name: str = None
    "母の父, name of the father of mother of the horse"
    mother_of_mother_code: str = None
    "code of the mother of mother of the horse, may be an empty string"
    mother_of_mother_name: str = None
    "母の母, name of the mother of mother of the horse"
    sex: str = None
    "性別, sex of the horse"
    birth_date: datetime = None
    "生年月日, birthday of the horse"
    color: str = None
    "毛色, color"
    owner: str = None
    "馬主名, owner of the horse"
    trainer_code: str = None
    "code of trainer"
    trainer_name: str = None
    "調教師名, name of trainer"
    trainer_affiliation: str = None
    "place of trainer"
    birth_place: str = None
    "生産牧場, birth place of the horse"
    prize_total: int = None
    "総賞金, the default unit of prize is 円"
    prize_fujia: int = None
    "付加賞"
    prize_difang: int = None
    "地方賞金"
    prize_haiwai: int = None
    "海外賞金"
    prize_pingdi: int = None
    "収得賞金（平地）"
    prize_zhanghai: int = None
    "収得賞金（障害）"
    results: List[ResultOfHorse] = field(default_factory=list)
    "result of the horse"
    update_time: datetime = None
    "date and time of update"

    def __post_init__(self):
        self.update_time = datetime.now()

@dataclass(slots=True, kw_only=True)
class ResultOfRace:
    race_code: str = None
    "code of the race"
    arrival_order_str: str = None
    "着順, string of the arrival order"
    arrival_order: int = None
    "着順, arrival order, initialization is not necessary"
    waku: int = None
    "枠 or 枠番, number of gate"
    waku_color: str = None
    "color of 枠"
    num: int = None
    "馬番, index of the horse"
    horse_code: str = None
    "index of the horse"
    #horse_link: str = None
    #"link of the horse"
    horse_name: str = None
    "馬名, name of the horse"
    horse_icon: str = None
    "競走馬に付く記号, icon of the horse, example: マルチ, ..."
    blinker: bool = None
    "ブリンカー, whether the horse wears blinkers"
    sex_and_age: str = None
    "性齢, sex and age of the horse, example: 牝3 or 牡5 or せん6"
    sex: str = None
    "sex of the horse, value: 牝 or 牡 or せん, initialization is not necessary"
    age_year: int = None
    "age of the horse, counting by year, initialization is not necessary"
    age_day: int = None
    "age of the horse, counting by day, initialization is not necessary"
    weight: float = None
    "負担重量, weight to carry of the horse"
    jockey_code: str = None
    "code of the jockey"
    jockey_name: str = None
    "騎手名, name of the jockey"
    time: float = None
    "タイム, race time"
    margin: str = None
    "着差, margin"
    corner_list: List[Optional[int]] = field(default_factory=list)
    "コーナー通過順位, orders of passing each corner"
    f_time: float = None
    "推定上り or 平均1F"
    horse_weight: float = None
    "馬体重, horse weight"
    horse_weight_delta: float = None
    "馬体重増減, gain/loss of horse weight"
    trainer_code: str = None
    "code of trainer"
    trainer_name: str = None
    "調教師名, name of trainer"
    pop: int = None
    "単勝人気, win popularity of the horse"
    update_time: datetime = None
    "date and time of update"

    def normalize(self):
        if self.arrival_order_str and (not self.arrival_order):
            self.arrival_order = order_str_to_int(self.arrival_order_str)
        if self.sex_and_age:
            sex, age = sexage_to_sex_age(self.sex_and_age)
            if not self.sex:
                self.sex = sex
            if not self.age_year:
                self.age_year = age

    def __post_init__(self):
        self.update_time = datetime.now()
        self.normalize()

@dataclass(slots=True, kw_only=True)
class Prize:
    "賞金"
    name: str = None
    "name of the prize, example: 本賞金, 付加賞"
    unit: str = None
    "unit of the prize, example: 万円"
    data: List[float] = field(default_factory=list)
    "prize for 1着, 2着, ..."

@dataclass(slots=True, kw_only=True)
class Race:
    code: str = None
    'code of the race, obtained from list of races, example: pw01sde1006202405020420241201/59'
    name: str = None
    'レース名, name of a race, obtained from list of races, example: 2歳新馬（混合）［指定］'
    title: str = None
    'title of a race (part of レース名), may be an empty string, example: メイクデビュー中山'
    index: int = None
    "one-based index of a race in a match, ordered by start time"
    distance: int = None
    '距離, distance of the race'
    distance_unit: str = None
    'unit of distance (part of 距離), maybe always メートル'
    surface: str = None
    '馬場, surface of the track, value: ダート, 芝, or something like 芝→ダート'
    number_horses_in_race: int = None
    '出走頭数, how many horse in the race'
    time: datetime = None
    'start time of the race'
    weather: str = None
    '天候, weather'
    turf_condition: str = None
    "condition of the turf track, conditions of turf and dirt tracks may occur together when the surface is something like 芝→ダート"
    dirt_condition: str = None
    "condition of the dirt track, conditions of turf and dirt tracks may occur together when the surface is something like 芝→ダート"
    category: str = None
    'div class="cell category" part of レース条件, example: 2歳'
    theclass: str = None
    'div class="cell class" part of レース条件, example: 新馬'
    rule: str = None
    'div class="cell rule" part of レース条件, example: （混合）［指定］'
    weight: str = None
    'div class="cell weight" part of レース条件, example: 馬齢'
    course_detail: str = None
    'span class="detail" part of レース条件, example: （芝・右）'
    prize_list: List[Prize] = field(default_factory=list)
    "prize of the race"
    result_list: List[ResultOfRace] = field(default_factory=list)
    "results of the race"
    update_time: datetime = None
    "date and time of update"

    def __post_init__(self):
        self.update_time = datetime.now()

@dataclass(slots=True, kw_only=True)
class Match:
    code: str = None
    "unique code of the match, example: pw01srl10062024050220241201/6F"
    date: datetime = None
    "date (year, month, day) of the match"
    name: str = None
    "name of the match, example: 5回中山2日"
    number_races_in_match: int = None
    "how many races in the match"
    kai: int = field(init=False)
    "5 of 5回中山2日"
    place: str = field(init=False)
    "中山 of 5回中山2日"
    nichi: str = field(init=False)
    "2 of 5回中山2日"
    races: List[str] = field(default_factory=list)
    "list of race codes in the match"
    update_time: datetime = None
    "date and time of update"

    def normalize(self):
        if hasattr(self, "name"):
            kai, place, nichi = self.long_name_to_kai_place_nichi(self.name)
            self.kai = kai
            self.place = place
            self.nichi = nichi

    def __post_init__(self):
        self.update_time = datetime.now()
        self.normalize()

    @staticmethod
    def long_name_to_kai_place_nichi(name: str):
        pattern = r"^(\d+)回(.+?)(\d+)日$"
        match = re.match(pattern, name)
        if match:
            kai = int(match.group(1))
            place: str = match.group(2)
            nichi = int(match.group(3))
            return kai, place, nichi
        else:
            return int(0), str(""), int(0)


if __name__ == "__main__":
    print(Match.long_name_to_kai_place_nichi("15回中山22日"))
    print(Match.long_name_to_kai_place_nichi("回中山2日"))
    thematch = Match(name="15回中山22日")
    print(thematch)
    race =Race(code="pw01sde1006202405020920241201/E2")
    p1 = Prize(name="本賞金", unit="万円", data={3.0, 2.0})
    p2 = Prize(name="付加賞", unit="万円", data={2.0, 1.0})
    race.prize_list.append(p1)
    race.prize_list.append(p2)
    print(race)
    resultofrace1 = ResultOfRace(arrival_order_str="失格", sex_and_age="せん6")
    print(resultofrace1)
    resultofrace2 = ResultOfRace(arrival_order_str="66", sex_and_age="せん6")
    print(resultofrace2)