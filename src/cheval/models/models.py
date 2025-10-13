# models.py

import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, unique
from typing import ClassVar, Dict, List, Optional

import sqlalchemy
from sqlalchemy.types import TypeDecorator, String
from sqlalchemy.orm import reconstructor
from sqlmodel import Field, SQLModel, create_engine, Session, Relationship
from pydantic import PrivateAttr, model_validator

from ..utils.misc import order_str_to_int, sexage_to_sex_age, match_name_to_kai_place_nichi

@unique
class DataType(Enum):
    """type of the data"""
    BASE = "base"
    FAILED = "failed"
    MATCH_LIST = "match_list"
    MATCH = "match"
    RACE = "race"
    RACE_RESULT = "race_result"
    HORSE = "horse"
    HORSE_RESULT = "horse_result"
    JOCKEY = "jockey"
    JOCKEY_SUMMARY = "jockey_summary"
    TRAINER = "trainer"
    TRAINER_SUMMARY = "trainer_summary"
    JOCKEY_TRAINER_SUMMARY = "trainer_trainer_summary"
    ODDS_TAN = "odds_tan"

def data_type_to_its_history(data_type: DataType):
    match data_type:
        case DataType.JOCKEY:
            return DataType.JOCKEY_SUMMARY
        case DataType.TRAINER:
            return DataType.TRAINER_SUMMARY
        case _:
            return None

@dataclass(slots=True, kw_only=True)
class CodeNameLinkAction:
    thetype: DataType
    code: Optional[str] = None
    name: Optional[str] = None
    link: Optional[str] = None
    action: Optional[str] = None

class SummaryOfJockeyTrainer(SQLModel, table=True):
    __tablename__ = DataType.JOCKEY_TRAINER_SUMMARY.value
    id: Optional[int] = Field(default=None, primary_key=True)
    summary_code: Optional[str] = Field(default=None)
    "code of summay, empty for 本年成績 or 累計成績, and obtained in HTML of jockey or trainer for 過去成績"
    jockey_trainer_code: Optional[str] = Field(default=None)
    "code of jockey or trainer"
    title: Optional[str] = Field(default=None)
    "title of the summary table: 本年成績, 累計成績, 2024年, ..."
    type: Optional[str] = Field(default=None)
    "type of the summary table: 平地, 障害, JRA合計, 地方, 海外, 総合計"
    num_no1: Optional[int] = Field(default=None)
    "1着, number of no 1"
    num_no2: Optional[int] = Field(default=None)
    "2着, number of no 2"
    num_no3: Optional[int] = Field(default=None)
    "3着, number of no 3"
    num_no4: Optional[int] = Field(default=None)
    "4着, number of no 4"
    num_no5: Optional[int] = Field(default=None)
    "5着, number of no 5"
    num_out5: Optional[int] = Field(default=None)
    "着外, number of outside the top 5"
    num_rides: Optional[int] = Field(default=None)
    "騎乗回数, number of rides"
    winning_rate: Optional[float] = Field(default=None)
    "勝率, winning rate"
    quinella_rate: Optional[float] = Field(default=None)
    "連対率, quinella rate"
    top3_rate: Optional[float] = Field(default=None)
    "3着内率, top 3 rate"
    update_time: Optional[datetime] = Field(default_factory=datetime.now)
    "date and time of update"

    def normalize(self):
        return self
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.normalize()

"""
class SummaryOfJockey(SummaryOfJockeyTrainer):
    __tablename__ = DataType.JOCKEY_SUMMARY.value

class SummaryOfJockey(SummaryOfJockeyTrainer):
    __tablename__ = DataType.TRAINER_SUMMARY.value
"""

class Trainer(SQLModel, table=True):
    __tablename__ = DataType.TRAINER.value
    code: Optional[str] = Field(default=None, primary_key=True)
    "code of the trainer"
    name: Optional[str] = Field(default=None)
    "name of trainer"
    name_kana: Optional[str] = Field(default=None)
    "kana name of trainer"
    retired: Optional[bool] = Field(default=None)
    "retired or not"
    birth_date: Optional[datetime] = Field(default=None)
    "生年月日, birthday of the trainer"
    birth_place: Optional[str] = Field(default=None)
    "出身地, birth place of the trainer"
    license_acquisition_year: Optional[int] = Field(default=None)
    "免許取得年, license acquisition year of the trainer"
    affiliation: Optional[str] = Field(default=None)
    "所属, affiliation of the trainer"
    first_race: Optional[str] = Field(default=None)
    "初出走, first race of the trainer"
    first_victory: Optional[str] = Field(default=None)
    "初勝利, first victory of the trainer"
    _summary_this_year: List[SummaryOfJockeyTrainer] = PrivateAttr(default_factory=list)
    "summary of the results in this year"
    _summary_total: List[SummaryOfJockeyTrainer] = PrivateAttr(default_factory=list)
    "summary of the total results"
    _summary_past: List[SummaryOfJockeyTrainer] = PrivateAttr(default_factory=list)
    "summary of the past results"
    update_time: Optional[datetime] = Field(default_factory=datetime.now)
    "date and time of update"

    def normalize(self):
        return self
    
    def __init__(self, *args, _summary_this_year=None, _summary_total=None, _summary_past=None, **kwargs):
        super().__init__(*args, **kwargs)
        if _summary_this_year is not None:
            self._summary_this_year = _summary_this_year
        if _summary_total is not None:
            self._summary_total = _summary_total
        if _summary_past is not None:
            self._summary_past = _summary_past
        self.normalize()

    @reconstructor
    def init_on_load(self):
        if getattr(self, "__pydantic_private__", None) is None:
            object.__setattr__(self, "__pydantic_private__", {})
        if "_summary_this_year" not in self.__pydantic_private__:
            self.__pydantic_private__["_summary_this_year"] = []
        if "_summary_total" not in self.__pydantic_private__:
            self.__pydantic_private__["_summary_total"] = []
        if "_summary_past" not in self.__pydantic_private__:
            self.__pydantic_private__["_summary_past"] = []

class Jockey(SQLModel, table=True):
    __tablename__ = DataType.JOCKEY.value
    code: Optional[str] = Field(default=None, primary_key=True)
    "code of the jockey, example: pw04kmk001144/54"
    name: Optional[str] = Field(default=None)
    "name of jockey"
    name_kana: Optional[str] = Field(default=None)
    "kana name of jockey"
    retired: Optional[bool] = Field(default=None)
    "retired or not"
    birth_date: Optional[datetime] = Field(default=None)
    "生年月日, birthday of the jockey"
    height: Optional[float] = Field(default=None)
    "身長, height of the jockey"
    height_unit: Optional[str] = Field(default=None)
    "height unit of the jockey, センチメートル"
    weight: Optional[float] = Field(default=None)
    "体重, weight of the jockey"
    weight_unit: Optional[str] = Field(default=None)
    "weight unit of the jockey, キログラム"
    blood_type: Optional[str] = Field(default=None)
    "blood type of the jockey"
    first_license_year: Optional[int] = Field(default=None)
    "初免許年, first license year of the jockey"
    license_type: Optional[str] = Field(default=None)
    "免許種類, license type of the jockey"
    birth_place: Optional[str] = Field(default=None)
    "出身地, birth place of the jockey"
    affiliation: Optional[str] = Field(default=None)
    "所属, affiliation of the jockey"
    affiliated_stable: Optional[str] = Field(default=None)
    "所属厩舎, affiliated stable of the jockey"
    first_ride: Optional[str] = Field(default=None)
    "初騎乗, first ride of the jockey"
    first_victory: Optional[str] = Field(default=None)
    "初勝利, first victory of the jockey"
    _summary_this_year: List[SummaryOfJockeyTrainer] = PrivateAttr(default_factory=list)
    "summary of the results in this year"
    _summary_total: List[SummaryOfJockeyTrainer] = PrivateAttr(default_factory=list)
    "summary of the total results"
    _summary_past: List[SummaryOfJockeyTrainer] = PrivateAttr(default_factory=list)
    "summary of the past results"
    summary_past_code: Optional[str] = Field(default=None)
    "code of the summary of the past results"
    update_time: Optional[datetime] = Field(default_factory=datetime.now)
    "date and time of update"

    def normalize(self):
        return self
    
    def __init__(self, *args, _summary_this_year=None, _summary_total=None, _summary_past=None, **kwargs):
        super().__init__(*args, **kwargs)
        if _summary_this_year is not None:
            self._summary_this_year = _summary_this_year
        if _summary_total is not None:
            self._summary_total = _summary_total
        if _summary_past is not None:
            self._summary_past = _summary_past
        self.normalize()

    @reconstructor
    def init_on_load(self):
        if getattr(self, "__pydantic_private__", None) is None:
            object.__setattr__(self, "__pydantic_private__", {})
        if "_summary_this_year" not in self.__pydantic_private__:
            self.__pydantic_private__["_summary_this_year"] = []
        if "_summary_total" not in self.__pydantic_private__:
            self.__pydantic_private__["_summary_total"] = []
        if "_summary_past" not in self.__pydantic_private__:
            self.__pydantic_private__["_summary_past"] = []

class ResultOfHorse(SQLModel, table=True):
    __tablename__ = DataType.HORSE_RESULT.value
    id: Optional[int] = Field(default=None, primary_key=True)
    horse_code: Optional[str] = Field(default=None)
    "code of the horse"
    date: Optional[datetime] = Field(default=None)
    "年月日, date of the race"
    place: Optional[str] = Field(default=None)
    "場, place of the race"
    race_name: Optional[str] = Field(default=None)
    "レース名, name of the race"
    race_code: Optional[str] = Field(default=None)
    "code of the race, may be an empty string"
    surface_distance: Optional[str] = Field(default=None)
    "距離, surface and distance of the race, example: 芝2000, 芝ダ2910"
    condition: Optional[str] = Field(default=None)
    "馬場, condition of the surface, example: 稍重, 良/良"
    num_of_horses: Optional[int] = Field(default=None)
    "頭数, number of horses in the race"
    pop: Optional[int] = Field(default=None)
    "人気, win popularity of the horse"
    arrival_order_str: Optional[str] = Field(default=None)
    "着順, string of the arrival order"
    arrival_order: Optional[int] = Field(default=None)
    "着順, arrival order, initialization is not necessary"
    jockey_code: Optional[str] = Field(default=None)
    "code of the jockey"
    jockey_name: Optional[str] = Field(default=None)
    "騎手名, name of the jockey"
    weight: Optional[float] = Field(default=None)
    "負担重量, weight to carry of the horse"
    horse_weight: Optional[float] = Field(default=None)
    "馬体重, horse weight"
    time: Optional[float] = Field(default=None)
    "タイム, race time"
    rt: Optional[str] = Field(default=None)
    "Rt, may be an empty string"
    update_time: Optional[datetime] = Field(default_factory=datetime.now)
    "date and time of update"

    def normalize(self):
        if self.arrival_order_str and (not self.arrival_order):
            self.arrival_order = order_str_to_int(self.arrival_order_str)
        return self
    
    def __init__(self, *args, _result_list=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.normalize()

class Horse(SQLModel, table=True):
    __tablename__ = DataType.HORSE.value
    code: Optional[str] = Field(default=None, primary_key=True)
    "code of the horse, example: pw01dud102022104401/B0"
    name: Optional[str] = Field(default=None)
    "馬名, name of the horse"
    name_en: Optional[str] = Field(default=None)
    "english name of the horse"
    rest: Optional[str] = Field(default=None)
    "rest state of the horse, may be an empty string, expamle: 放牧"
    deleted: Optional[bool] = Field(default=None)
    "deleted or not, 抹消"
    father_code: Optional[str] = Field(default=None)
    "code of the father of the horse, may be an empty string"
    father_name: Optional[str] = Field(default=None)
    "父, name of the father of the horse"
    mother_code: Optional[str] = Field(default=None)
    "code of the mother of the horse, may be an empty string"
    mother_name: Optional[str] = Field(default=None)
    "母, name of the mother of the horse"
    father_of_mother_code: Optional[str] = Field(default=None)
    "code of the father of mother of the horse, may be an empty string"
    father_of_mother_name: Optional[str] = Field(default=None)
    "母の父, name of the father of mother of the horse"
    mother_of_mother_code: Optional[str] = Field(default=None)
    "code of the mother of mother of the horse, may be an empty string"
    mother_of_mother_name: Optional[str] = Field(default=None)
    "母の母, name of the mother of mother of the horse"
    sex: Optional[str] = Field(default=None)
    "性別, sex of the horse"
    birth_date: Optional[datetime] = Field(default=None)
    "生年月日, birthday of the horse"
    color: Optional[str] = Field(default=None)
    "毛色, color"
    owner: Optional[str] = Field(default=None)
    "馬主名, owner of the horse"
    trainer_code: Optional[str] = Field(default=None)
    "code of trainer"
    trainer_name: Optional[str] = Field(default=None)
    "調教師名, name of trainer"
    trainer_affiliation: Optional[str] = Field(default=None)
    "place of trainer"
    birth_place: Optional[str] = Field(default=None)
    "生産牧場, birth place of the horse"
    prize_total: Optional[int] = Field(default=None)
    "総賞金, the default unit of prize is 円"
    prize_fujia: Optional[int] = Field(default=None)
    "付加賞"
    prize_difang: Optional[int] = Field(default=None)
    "地方賞金"
    prize_haiwai: Optional[int] = Field(default=None)
    "海外賞金"
    prize_pingdi: Optional[int] = Field(default=None)
    "収得賞金（平地）"
    prize_zhanghai: Optional[int] = Field(default=None)
    "収得賞金（障害）"
    _result_list: List[ResultOfHorse] = PrivateAttr(default_factory=list)
    "result of the horse"
    update_time: Optional[datetime] = Field(default_factory=datetime.now)
    "date and time of update"

    def normalize(self):
        return self
    
    def __init__(self, *args, _result_list=None, **kwargs):
        super().__init__(*args, **kwargs)
        if _result_list is not None:
            self._result_list = _result_list
        self.normalize()

    @reconstructor
    def init_on_load(self):
        if getattr(self, "__pydantic_private__", None) is None:
            object.__setattr__(self, "__pydantic_private__", {})
        if "_corner_list" not in self.__pydantic_private__:
            self.__pydantic_private__["_result_list"] = []

@dataclass(slots=True, kw_only=True)
class OddsTan:
    """単勝オッズ, odds tan, used when parse the HTML of odds tan page, the data will be wrinten in ResultOfRace"""
    code: Optional[str] = None
    'code of the odds, obtained from list of races, example: pw151ou1008202401010120240106Z/F7'
    odds: Dict[int, Optional[float]] = field(default_factory=dict)
    "odds tan of each horses"
    update_time: Optional[datetime] = None
    "date and time of update"

    def __post_init__(self):
        self.update_time = datetime.now()

class ResultOfRace(SQLModel, table=True):
    __tablename__ = DataType.RACE_RESULT.value
    id: Optional[int] = Field(default=None, primary_key=True)
    race_code: Optional[str] = Field(default=None)
    "code of the race"
    arrival_order_str: Optional[str] = Field(default=None)
    "着順, string of the arrival order"
    arrival_order: Optional[int] = Field(default=None)
    "着順, arrival order, initialization is not necessary"
    waku: Optional[int] = Field(default=None)
    "枠 or 枠番, number of gate"
    waku_color: Optional[str] = Field(default=None)
    "color of 枠"
    num: Optional[int] = Field(default=None)
    "馬番, index of the horse"
    horse_code: Optional[str] = Field(default=None)
    "code of the horse"
    horse_name: Optional[str] = Field(default=None)
    "馬名, name of the horse"
    horse_icon: Optional[str] = Field(default=None)
    "競走馬に付く記号, icon of the horse, example: マルチ, ..."
    blinker: Optional[bool] = Field(default=None)
    "ブリンカー, whether the horse wears blinkers"
    sex_and_age: Optional[str] = Field(default=None)
    "性齢, sex and age of the horse, example: 牝3 or 牡5 or せん6"
    sex: Optional[str] = Field(default=None)
    "sex of the horse, value: 牝 or 牡 or せん, initialization is not necessary"
    age_year: Optional[int] = Field(default=None)
    "age of the horse, counting by year, initialization is not necessary"
    age_day: Optional[int] = Field(default=None)
    "age of the horse, counting by day, initialization is not necessary"
    weight: Optional[float] = Field(default=None)
    "負担重量, weight to carry of the horse"
    jockey_code: Optional[str] = Field(default=None)
    "code of the jockey"
    jockey_name: Optional[str] = Field(default=None)
    "騎手名, name of the jockey"
    time: Optional[float] = Field(default=None)
    "タイム, race time"
    margin: Optional[str] = Field(default=None)
    "着差, margin"
    _corner_list: List[Optional[int]] = PrivateAttr(default_factory=list)
    "コーナー通過順位, orders of passing each corner"
    order_corner_1: Optional[int] = Field(default=None)
    "第1コーナー通過順位, order of passing corner 1"
    order_corner_2: Optional[int] = Field(default=None)
    "第2コーナー通過順位, order of passing corner 2"
    order_corner_3: Optional[int] = Field(default=None)
    "第3コーナー通過順位, order of passing corner 3"
    order_corner_4: Optional[int] = Field(default=None)
    "第4コーナー通過順位, order of passing corner 4"
    f_time: Optional[float] = Field(default=None)
    "推定上り or 平均1F"
    horse_weight: Optional[float] = Field(default=None)
    "馬体重, horse weight"
    horse_weight_delta: Optional[float] = Field(default=None)
    "馬体重増減, gain/loss of horse weight"
    trainer_code: Optional[str] = Field(default=None)
    "code of trainer"
    trainer_name: Optional[str] = Field(default=None)
    "調教師名, name of trainer"
    pop: Optional[int] = Field(default=None)
    "単勝人気, win popularity of the horse"
    odds_tan: Optional[float] = Field(default=None)
    "単勝オッズ, odds_tan of the horse"
    update_time: Optional[datetime] = Field(default_factory=datetime.now)
    "date and time of update"

    def normalize(self):
        orders = [0, 0, 0, 0]
        for i in range(min(len(orders), len(self._corner_list))):
            orders[i] = self._corner_list[i]
        self.order_corner_1 = orders[0]
        self.order_corner_2 = orders[1]
        self.order_corner_3 = orders[2]
        self.order_corner_4 = orders[3]
        if self.arrival_order_str and (not self.arrival_order):
            self.arrival_order = order_str_to_int(self.arrival_order_str)
        if self.sex_and_age:
            sex, age = sexage_to_sex_age(self.sex_and_age)
            if not self.sex:
                self.sex = sex
            if not self.age_year:
                self.age_year = age
        return self
    
    def __init__(self, *args, _corner_list=None, **kwargs):
        super().__init__(*args, **kwargs)
        if _corner_list is not None:
            self._corner_list = _corner_list
        self.normalize()

    @reconstructor
    def init_on_load(self):
        if getattr(self, "__pydantic_private__", None) is None:
            object.__setattr__(self, "__pydantic_private__", {})
        if "_corner_list" not in self.__pydantic_private__:
            self.__pydantic_private__["_corner_list"] = []

@dataclass(slots=True, kw_only=True)
class Prize:
    """賞金, used as the member of some lists in Race"""
    name: Optional[str] = None
    "name of the prize, example: 本賞金, 付加賞"
    unit: Optional[str] = None
    "unit of the prize, example: 万円"
    data: List[float] = field(default_factory=list)
    "prize for 1着, 2着, ..."

class Race(SQLModel, table=True):
    __tablename__ = DataType.RACE.value
    code: Optional[str] = Field(default=None, primary_key=True)
    "code of the race, obtained from list of races, example: pw01sde1006202405020420241201/59"
    match_code: Optional[str] = Field(default=None)
    "code of the match which the race belongs to"
    name: Optional[str] = Field(default=None)
    "レース名, name of a race, obtained from list of races, example: 2歳新馬（混合）［指定］"
    title: Optional[str] = Field(default=None)
    "title of a race (part of レース名), may be an empty string, example: メイクデビュー中山"
    index: Optional[int] = Field(default=None)
    "one-based index of a race in a match, ordered by start time"
    distance: Optional[int] = Field(default=None)
    "距離, distance of the race"
    distance_unit: Optional[str] = Field(default=None)
    "unit of distance (part of 距離), maybe always メートル"
    surface: Optional[str] = Field(default=None)
    "馬場, surface of the track, value: ダート, 芝, or something like 芝→ダート"
    number_horses_in_race: Optional[int] = Field(default=None)
    "出走頭数, how many horse in the race"
    time: Optional[datetime] = Field(default=None)
    "start time of the race"
    weather: Optional[str] = Field(default=None)
    "天候, weather"
    turf_condition: Optional[str] = Field(default=None)
    "condition of the turf track, conditions of turf and dirt tracks may occur together when the surface is something like 芝→ダート"
    dirt_condition: Optional[str] = Field(default=None)
    "condition of the dirt track, conditions of turf and dirt tracks may occur together when the surface is something like 芝→ダート"
    category: Optional[str] = Field(default=None)
    "div class='cell category' part of レース条件, example: 2歳"
    theclass: Optional[str] = Field(default=None)
    "div class='cell class' part of レース条件, example: 新馬"
    rule: Optional[str] = Field(default=None)
    "div class='cell rule' part of レース条件, example: （混合）［指定］"
    weight: Optional[str] = Field(default=None)
    "div class='cell weight' part of レース条件, example: 馬齢"
    course_detail: Optional[str] = Field(default=None)
    "span class='detail' part of レース条件, example: （芝・右）"
    _prize_list: List[Prize] = PrivateAttr(default_factory=list)
    "prizes of the race"
    number_prizes: Optional[int] = None
    "number of prize kinds"
    prize_no_1: Optional[float] = Field(default=None)
    "total prize for no.1, unit=万円"
    prize_no_2: Optional[float] = Field(default=None)
    "total prize for no.2, unit=万円"
    prize_no_3: Optional[float] = Field(default=None)
    "total prize for no.3, unit=万円"
    prize_no_4: Optional[float] = Field(default=None)
    "total prize for no.4, unit=万円"
    prize_no_5: Optional[float] = Field(default=None)
    "total prize for no.5, unit=万円"
    _result_list: List[ResultOfRace] = PrivateAttr(default_factory=list)
    "results of the race"
    number_corners: Optional[int] = Field(default=None)
    "number of corners"
    update_time: Optional[datetime] = Field(default_factory=datetime.now)
    "date and time of update"

    def normalize(self):
        self.number_prizes = len(self._prize_list)
        total_prize = [float(0.0), float(0.0), float(0.0), float(0.0), float(0.0)]
        for prize in self._prize_list:
            assert (prize.unit == "万円")
            for i in range(min(len(prize.data), len(total_prize))):
                total_prize[i] += prize.data[i]
        self.prize_no_1 = total_prize[0]
        self.prize_no_2 = total_prize[1]
        self.prize_no_3 = total_prize[2]
        self.prize_no_4 = total_prize[3]
        self.prize_no_5 = total_prize[4]
        if len(self._result_list) > 0:
            self.number_corners = max([len(result._corner_list) for result in self._result_list])
        return self
    
    def __init__(self, *args, _prize_list=None, _result_list=None, **kwargs):
        super().__init__(*args, **kwargs)
        if _prize_list is not None:
            self._prize_list = _prize_list
        if _result_list is not None:
            self._result_list = _result_list
        self.normalize()

    @reconstructor
    def init_on_load(self):
        if getattr(self, "__pydantic_private__", None) is None:
            object.__setattr__(self, "__pydantic_private__", {})
        if "_prize_list" not in self.__pydantic_private__:
            self.__pydantic_private__["_prize_list"] = []
        if "_result_list" not in self.__pydantic_private__:
            self.__pydantic_private__["_result_list"] = []

    def add_odds_tan(self, odds_tan: OddsTan):
        assert(len(self._result_list) == len(odds_tan.odds))
        for result in self._result_list:
            result.odds_tan = odds_tan.odds[result.num]

def add_odds_tan_to_race(race: Race, odds_tan: OddsTan):
    for result in race._result_list:
        result.odds_tan = odds_tan.odds[result.num]

class Match(SQLModel, table=True):
    __tablename__ = DataType.MATCH.value
    code: Optional[str] = Field(default=None, primary_key=True)
    "unique code of the match, example: pw01srl10062024050220241201/6F"
    date: Optional[datetime] = Field(default=None)
    "date (year, month, day) of the match"
    name: Optional[str] = Field(default=None)
    "name of the match, example: 5回中山2日"
    number_races_in_match: Optional[int] = None
    "how many races in the match"
    kai: Optional[int] = Field(default=None)
    "5 of 5回中山2日"
    place: Optional[str] = Field(default=None)
    "中山 of 5回中山2日"
    nichi: Optional[int] = Field(default=None)
    "2 of 5回中山2日"
    _races: Dict[str, str] = PrivateAttr(default_factory=dict)
    "dict of races (code: name) in the match; not saved in database"
    update_time: datetime = Field(default_factory=datetime.now)
    "date and time of update"

    def normalize(self):
        kai, place, nichi = match_name_to_kai_place_nichi(self.name)
        self.kai = kai
        self.place = place
        self.nichi = nichi
        return self
    
    def __init__(self, **data):
        super().__init__(**data)
        self.normalize()

    @reconstructor
    def init_on_load(self):
        if getattr(self, "__pydantic_private__", None) is None:
            object.__setattr__(self, "__pydantic_private__", {})
        if "_races" not in self.__pydantic_private__:
            self.__pydantic_private__["_races"] = {}

class EnumType(TypeDecorator):
    """A general type for converting between Enum and String.
    Stored as strings in the database, but automatically converted to Enum in Python."""
    impl = String
    cache_ok = True

    def __init__(self, enumtype, *args, **kwargs):
        self._enumtype = enumtype
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        """Called when writing to the database"""
        if isinstance(value, Enum):
            return value.value
        return value

    def process_result_value(self, value, dialect):
        """Called when reading from the database"""
        if value is None:
            return None
        return self._enumtype(value)

class CodeRecorder(SQLModel, table=True):
    __tablename__ = "code"
    id: Optional[int] = Field(default=None, primary_key=True)
    code: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    datetype: DataType = Field(sa_column=sqlalchemy.Column(EnumType(DataType)))
    count: int = Field(default=int(1))
    __table_args__ = (
        sqlalchemy.UniqueConstraint("code", "datetype", name="uq_code_datetype"),
    )