# parsers.py

from .month_parser import MonthParser
from .match_parser import MatchParser
from .race_parser import RaceParser
from .horse_parser import HorseParser
from .jockey_parser import JockeyParser, JockeySummaryParser
from .trainer_parser import TrainerParser, TrainerSummaryParser
from .odds_tan_parser import OddsTanParser

class Parsers:

    def __init__(self):
        self.month = MonthParser()
        self.match = MatchParser()
        self.race = RaceParser()
        self.odds_tan = OddsTanParser()
        self.horse = HorseParser()
        self.jockey = JockeyParser()
        self.joceky_summary = JockeySummaryParser()
        self.trainer = TrainerParser()
        self.trainer_summary = TrainerSummaryParser()