# html_storage.py

import os
from datetime import datetime
from typing import Optional

import gzip

from ..models.models import DataType
from ..config import DIR_FOR_SAVE_HTML
from ..utils.misc import safe_dir

class HTMLStorage:
    """
    Store HTML pages and automatically organizing directories and file naming.
    """

    def __init__(self, root_dir=DIR_FOR_SAVE_HTML):
        self.root_dir = root_dir
    
    def save_html(self, page_type: DataType, code: str, html: str,
              url: str = None, metadata: dict = None, keep_history: Optional[bool] = None):
        """
        Save HTML pages as gzip files and log additional information.
        Parameters:
        - page_type: page type
        - code: unique identifier of the object
        - html: string of the HTML
        - url: page source URL (optional)
        - metadata: other metadata (optional)
        - keep_history: whether to retain historical snapshots
        """
        if keep_history is None:
            if page_type in [DataType.MATCH_LIST, DataType.MATCH, DataType.RACE]:
                keep_history = False
            else:
                keep_history = True

        #subdir = os.path.join(self.root_dir, self._map_page_type(page_type))
        subdir = os.path.join(self.root_dir, page_type.value)
        os.makedirs(subdir, exist_ok=True)

        filename = self._make_filename(safe_dir(code), keep_history)
        filepath = os.path.join(subdir, filename)

        with gzip.open(filepath, "wt", encoding="utf-8") as f:
            f.write(html)

        """
        # 预留扩展：记录索引信息
        record = {
            "page_type": page_type,
            "identifier": code,
            "filepath": filepath,
            "url": url,
            "metadata": metadata or {},
            "saved_at": datetime.now().isoformat()
        }
        # 这里先写到控制台，未来可改写成 CSV/JSON/SQLite
        print("Saved record:", record)
        """

        return filepath

    def _map_page_type(self, page_type: DataType) -> str:
        """映射页面类型到子目录"""
        mapping = {
            DataType.MATCH_LIST: "matche_lists",
            DataType.MATCH: "matches",
            DataType.RACE: "races",
            DataType.HORSE: "horses",
            DataType.JOCKEY: "jockeys",
            DataType.JOCKEY_SUMMARY: "jockey_histories",
            DataType.TRAINER: "trainers",
            DataType.TRAINER_SUMMARY: "trainer_histories",
        }
        if page_type not in mapping:
            raise ValueError(f"Unknown type of html page: {page_type}")
        return mapping[page_type]

    def _make_filename(self, identifier: str, keep_history: bool) -> str:
        """generate the file name, name with timestamp if keep_history is True"""
        if keep_history:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"{identifier}_{timestamp}.html.gz"
        else:
            return f"{identifier}.html.gz"