# base.py

import inspect
import logging
import os
import hashlib
import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from bs4 import BeautifulSoup

from ..models.models import DataType, CodeNameLinkAction
from ..storage.html_storage import HTMLStorage
from ..config import DIR_FOR_SAVE_HTML
from ..utils.logging import get_logger
from ..utils.misc import safe_dir

T = TypeVar("T")

@dataclass
class ParseResult(Generic[T]):
    # entity (None if no entity）
    entity: Optional[T] = None
    # collections of links: keys determined by the parser
    links: Dict[DataType, List[CodeNameLinkAction]] = field(default_factory=dict)
    # list of summary or history of the entity
    history: List[T] = field(default_factory=list)
    # errors and warnings logged when parsing HTML
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    # metadata: parser name, version, source url, context, failed_html_path...
    _meta: Dict[str, Any] = field(default_factory=dict)

class ParseError(Exception):
    pass

# ----- BaseParser -----

class BaseParser:
    data_type = DataType.BASE
    parser_name = data_type.value
    parser_version = "0.1"

    def __init__(self):
        self.logger = get_logger(f"cheval.parsers.{self.parser_name}")

    def parse(self, html: str, entity_code: str = None, entity_name: str = None,
              save_html: Optional[bool] = True, keep_history: Optional[bool] = None, 
              root_dir_for_save: str = DIR_FOR_SAVE_HTML,
              context: Optional[Dict[str, Any]] = None) -> ParseResult[Any]:
        """
        Public entry point: Each subclass implements _parse_impl and returns a ParseResult[T] (no exception handling).
        This method is responsible for catching exceptions, saving the HTML, and recording information in the returned ParseResult._meta .
        context: Any dictionary used to record contextual information such as year/month/race number/horse index (for easy backtracking).
        """
        self.logger.info(f"begin to parse the HTML by {inspect.currentframe().f_code.co_name} of {self.__class__}\n\tentity_code={entity_code}, entity_name={entity_name},\n\tsave_html={save_html}, keep_history={keep_history}, root_dir_for_save={root_dir_for_save},\n\tcontext: {context}")
        if save_html:
            HTMLStorage(root_dir=root_dir_for_save).save_html(page_type=self.data_type, code=entity_code, html=html, keep_history=keep_history)
        try:
            result: ParseResult[Any] = self._parse_impl(html, entity_code, entity_name)
            result._meta.setdefault("parser", self.parser_name)
            result._meta.setdefault("version", self.parser_version)
            if context:
                result._meta.setdefault("context", context)
            return result
        except Exception as e:
            filepath = HTMLStorage(root_dir=root_dir_for_save).save_html(page_type=DataType.FAILED, code=entity_code, html=html, keep_history=keep_history)
            self.logger.exception(f"A fatal parser error in {inspect.currentframe().f_code.co_name} of {self.__class__}!")
            self.logger.exception(f"Information: code={entity_code}, HTML file path={filepath}\n\tcontext: {context}")
            self.logger.exception(f"{str(e)}")
            raise e

    def _parse_impl(self, html: str, entity_code: str = None, entity_name: str = None) -> ParseResult[Any]:
        """
        This method is overridden by subclasses. It only performs parsing and does not handle exceptions.
        Return:
            ParseResult[...]
        """
        raise NotImplementedError