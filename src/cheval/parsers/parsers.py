# parsers.py

from .match_list_parser import MatchListParser
from .match_parser import MatchParser
from .race_parser import RaceParser
from .horse_parser import HorseParser
from .jockey_parser import JockeyParser, JockeySummaryParser
from .trainer_parser import TrainerParser, TrainerSummaryParser

class Parsers:

    def __init__(self):
        self.match_list = MatchListParser()
        self.match = MatchParser()
        self.race = RaceParser()
        self.horse = HorseParser()
        self.jockey = JockeyParser()
        self.joceky_summary = JockeySummaryParser()
        self.trainer = TrainerParser()
        self.trainer_summary = TrainerSummaryParser()