# config.py

import os

BEGIN_URL = "https://jra.jp/faq/pop02/1_6.html"
BASE_URL = "https://jra.jp"
WAIT_TIMEOUT = 30
DIR_FOR_DATA = "data"
DIR_FOR_LOG = os.path.join(DIR_FOR_DATA, "log")
DIR_FOR_SAVE_HTML = os.path.join(DIR_FOR_DATA, "html")
