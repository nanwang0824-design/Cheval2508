# parsers.py

from parsers.match_list_parser import MatchListParser
from parsers.match_parser import MatchParser
from parsers.race_parser import RaceParser
from parsers.horse_parser import HorseParser
from parsers.jockey_parser import JockeyParser
from parsers.trainer_parser import TrainerParser

class Parsers:

    def __init__(self):
        self.match_list = MatchListParser()
        self.match = MatchParser()
        self.race = RaceParser()
        self.horse = HorseParser()
        self.jeckey = JockeyParser()
        self.trainer = TrainerParser()