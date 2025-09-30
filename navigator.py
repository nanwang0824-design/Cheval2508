# navigator.py

import inspect

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from browser import Browser
from parsers.match_list_processor import MatchListProcessor

class Navigator:
    def __init__(self, browser: Browser):
        self.browser = browser

    def get_html(self):
        return self.browser.get_html()

    def go_to_search_page(self):
        """Enter the year and month selection page from the initial page"""
        try:
            self.browser.get("https://jra.jp/faq/pop02/1_6.html")
            self.browser.click(By.XPATH, "//a[contains(text(), 'レース結果')]")
            self.browser.click(By.XPATH, "//a[contains(text(), '過去レース結果検索')]")
            self.browser.find_one_element(By.ID, "kaisaiY_list")
            self.browser.find_one_element(By.ID, "kaisaiM_list")
            print("Open the search page successfully.")
        except Exception as e:
            print(f"An exception in {inspect.currentframe().f_code.co_name} of {self.__class__}!")
            raise e

    def search_by_year_month(self, year: int, month: int):
        """Select year and month and search"""
        #self.basic_info.set_info(year=year, month=month)
        try:
            self.browser.find_one_element(By.ID, "kaisaiY_list")
            self.browser.find_one_element(By.ID, "kaisaiM_list")
            self.browser.select_value(By.ID, "kaisaiY_list", str(year).zfill(4))
            self.browser.select_value(By.ID, "kaisaiM_list", str(month).zfill(2))
            self.browser.click(By.XPATH, "//a[contains(text(), '検索')]")
            match_day_blocks = self.browser.find_all_elements(By.CSS_SELECTOR, ".past_result_line_unit")
            print(f"Search by year = {year} and month = {month}: there are {len(match_day_blocks)} match day(s).")
        except Exception as e:
            print(f"An exception in {inspect.currentframe().f_code.co_name} of {self.__class__}!")
            print(f"Information: year={year}, month={month}")
            raise e

    def open_match_day(self, race_day_link):
        """点击进入单个比赛日页面"""
        pass