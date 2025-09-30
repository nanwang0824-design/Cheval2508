# scraper.py

from browser import Browser
from navigator import Navigator
from parsers import Parsers

class JRAScraper:
    def __init__(self, browser: Browser, navigator: Navigator, parsers: Parsers, storage):
        self.browser = browser
        self.navigator = navigator
        self.parsers = parsers
        self.storage = storage

    def run(self, start_year: int, start_month: int, end_year: int, end_month: int):
        pass