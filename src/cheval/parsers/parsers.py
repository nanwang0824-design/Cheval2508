# parsers.py

from .match_list_parser import MatchListParser
from .match_parser import MatchParser
from .race_parser import RaceParser
from .horse_parser import HorseParser
from .jockey_parser import JockeyParser
from .trainer_parser import TrainerParser

class Parsers:

    def __init__(self):
        self.match_list = MatchListParser()
        self.match = MatchParser()
        self.race = RaceParser()
        self.horse = HorseParser()
        self.jockey = JockeyParser()
        self.trainer = TrainerParser()