# navigator.py

import inspect

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from src.cheval.browser.browser import Browser

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

    def back(self):
        """Go back"""
        self.browser.back()

    def close(self):
        """Close"""
        self.browser.close()

    def get_match_html(self, action: str):
        """Enter the page of a match and get its html"""
        self.browser.open_window_by_action(action=action, wait_time_before=0, wait_time_after=0)
        self.browser.wait_for_load(wait_time_before=0, wait_time_after=0)
        self.browser.find_all_elements(by=By.CSS_SELECTOR, detail="th.race_num[scope='row']")
        return self.browser.get_html()

    def get_race_html(self, link: str):
        """Enter the page of a race and get its html"""
        self.browser.get(url=link, wait_time_before=0, wait_time_after=0)
        self.browser.wait_for_load(wait_time_before=0, wait_time_after=0)
        self.browser.find_one_element(by=By.CSS_SELECTOR, detail="div.block_header")
        return self.browser.get_html()

    def get_horse_html(self, link: str):
        """Enter the page of a race and get its html"""
        self.browser.get(url=link, wait_time_before=0, wait_time_after=0)
        self.browser.wait_for_load(wait_time_before=0, wait_time_after=0)
        self.browser.find_all_elements(by=By.CSS_SELECTOR, detail="td.date")
        return self.browser.get_html()

    def get_jockey_trainer_html(self, action: str):
        """Enter the page of a jockey or trainer or his/her summary and get its html"""
        self.browser.open_window_by_action(action=action, wait_time_before=0, wait_time_after=0)
        self.browser.wait_for_load(wait_time_before=0, wait_time_after=0)
        self.browser.find_all_elements(by=By.CSS_SELECTOR, detail="th.row")
        return self.browser.get_html()

    def get_odds_tan_html(self, action: str):
        """Enter the page of a odds tan (単勝オッズ) and get its html"""
        self.browser.open_window_by_action(action=action, wait_time_before=0, wait_time_after=0)
        self.browser.wait_for_load(wait_time_before=0, wait_time_after=0)
        self.browser.find_all_elements(by=By.CSS_SELECTOR, detail="tr th.horse")
        return self.browser.get_html()