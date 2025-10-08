# waiter.py

import inspect
import random
import time
from typing import Optional

#from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

import src.cheval.config as config
#from browser import Browser

class Waiter:
    TIME_OUT = config.WAIT_TIMEOUT
    TIME_OUT_MAX = config.WAIT_TIMEOUT
    TIME_OUT_MIN = 20
    TIME_LONG = 10
    TIME_LONG_MIN = 8
    TIME_LONG_MAX = 12
    TIME_MEDIUM = 6
    TIME_MEDIUM_MIN = 4
    TIME_MEDIUM_MAX = 8
    TIME_SHORT = 2
    TIME_SHORT_MIN = 1
    TIME_SHORT_MAX = 3
    TIME_INTERVAL = 1

    def __init__(self):
        #self.browser = browser
        #self.driver = browser.driver
        pass

    @staticmethod
    def get_wait_time(min_time: int, max_time: int):
        return random.randint(min_time, max_time)

    @staticmethod
    def wait(wait_time: int):
        if wait_time > 0:
            time.sleep(wait_time)

    @staticmethod
    def get_wait_time_long():
        return Waiter.get_wait_time(min_time=Waiter.TIME_LONG_MIN, max_time=Waiter.TIME_LONG_MAX)

    @staticmethod
    def wait_long():
        Waiter.wait(Waiter.get_wait_time_long())

    @staticmethod
    def get_wait_time_medium():
        return Waiter.get_wait_time(min_time=Waiter.TIME_MEDIUM_MIN, max_time=Waiter.TIME_MEDIUM_MAX)

    @staticmethod
    def wait_medium():
        Waiter.wait(Waiter.get_wait_time_medium())

    @staticmethod
    def get_wait_time_short():
        return Waiter.get_wait_time(min_time=Waiter.TIME_SHORT_MIN, max_time=Waiter.TIME_SHORT_MAX)

    @staticmethod
    def wait_short():
        Waiter.wait(Waiter.get_wait_time_short())

