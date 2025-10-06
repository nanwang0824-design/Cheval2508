# logging.py

import logging
import sys
from pathlib import Path

from ..config import DIR_FOR_LOG

# directory and files for storing logs
LOG_DIR = Path(DIR_FOR_LOG)
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "cheval.log"

# format of log
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# root logger, only configured once
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout), # utput to the console
        logging.FileHandler(LOG_FILE, encoding="utf-8") # write to the log file
    ]
)

def get_logger(name: str) -> logging.Logger:
    """
    Get the logger.
    No need to set a separate handler; just call it directly.
    """
    return logging.getLogger(name)