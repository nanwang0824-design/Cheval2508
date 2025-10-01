# base_parser.py

class BaseParser:
    def parse(self, html: str):
        raise NotImplementedError("Subclasses must implement parse()")