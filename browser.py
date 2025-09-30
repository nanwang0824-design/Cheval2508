# browser.py

import inspect
import time
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from waiter import Waiter

class Browser:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--log-level=3")
        #options.add_argument("--headless")
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=options)

    def get(self, url: str, wait_time_before: Optional[int] = None, wait_time_after: Optional[int] = None):
        if wait_time_before is None:
            wait_time_before = int(0)
        if wait_time_after is None:
            wait_time_after = Waiter.get_wait_time_medium()
        try:
            Waiter.wait(wait_time_before)
            self.driver.get(url)
            Waiter.wait(wait_time_after)
        except Exception as e:
            print(f"An exception in {inspect.currentframe().f_code.co_name} of {self.__class__}!")
            print(f"Information: url={url}")
            raise e
        
    def switch_to_window(self, window_index: int, wait_time_before: Optional[int] = None, wait_time_after: Optional[int] = None):
        if wait_time_before is None:
            wait_time_before = int(0)
        if wait_time_after is None:
            wait_time_after = Waiter.get_wait_time_short()
        try:
            Waiter.wait(wait_time_before)
            self.driver.switch_to.window(self.driver.window_handles[window_index])
            Waiter.wait(wait_time_after)
        except Exception as e:
            print(f"An exception in {inspect.currentframe().f_code.co_name} of {self.__class__}!")
            print(f"Information: window_index={window_index}")
            raise e
        
    def back(self, wait_time_before: Optional[int] = None, wait_time_after: Optional[int] = None):
        if wait_time_before is None:
            wait_time_before = int(0)
        if wait_time_after is None:
            wait_time_after = Waiter.get_wait_time_medium()
        try:
            Waiter.wait(wait_time_before)
            self.driver.back()
            Waiter.wait(wait_time_after)
        except Exception as e:
            print(f"An exception in {inspect.currentframe().f_code.co_name} of {self.__class__}!")
            raise e

    def close(self, wait_time_before: Optional[int] = None, wait_time_after: Optional[int] = None):
        if wait_time_before is None:
            wait_time_before = int(0)
        if wait_time_after is None:
            wait_time_after = Waiter.get_wait_time_short()
        Waiter.wait(wait_time_before)
        self.driver.quit()
        Waiter.wait(wait_time_after)

    def get_html(self):
        return self.driver.page_source
        
    def click(self, by: str, detail: str, time_out: Optional[int] = None, wait_time_before: Optional[int] = None, wait_time_after: Optional[int] = None):
        if time_out is None:
            time_out = Waiter.TIME_OUT
        if wait_time_before is None:
            wait_time_before = int(0)
        if wait_time_after is None:
            wait_time_after = Waiter.get_wait_time_short()
        try:
            element = WebDriverWait(self.driver, timeout=time_out).until(EC.presence_of_element_located((by, detail)))
            Waiter.wait(wait_time_before)
            element.click()
            Waiter.wait(wait_time_after)
        except Exception as e:
            print(f"An exception in {inspect.currentframe().f_code.co_name} of {self.__class__}!")
            print(f"Information: by={by}, detail={detail}")
            raise e
        return element
        
    def find_one_element(self, by: str, detail: str, time_out: Optional[int] = None, wait_time_before: Optional[int] = None, wait_time_after: Optional[int] = None):
        if time_out is None:
            time_out = Waiter.TIME_OUT
        if wait_time_before is None:
            wait_time_before = int(0)
        if wait_time_after is None:
            wait_time_after = Waiter.get_wait_time_short()
        try:
            Waiter.wait(wait_time_before)
            element = WebDriverWait(self.driver, time_out).until(EC.presence_of_element_located((by, detail)))
            Waiter.wait(wait_time_after)
        except Exception as e:
            print(f"An exception in {inspect.currentframe().f_code.co_name} of {self.__class__}!")
            print(f"Information: by={by}, detail={detail}")
            raise e
        return element
        
    def find_all_elements(self, by: str, detail: str, time_out: Optional[int] = None, interval_time: Optional[int] = None, wait_time_before: Optional[int] = None, wait_time_after: Optional[int] = None):
        if time_out is None:
            time_out = Waiter.TIME_OUT
        if interval_time is None:
            interval_time = Waiter.TIME_INTERVAL
        if wait_time_before is None:
            wait_time_before = int(0)
        if wait_time_after is None:
            wait_time_after = Waiter.get_wait_time_short()
        last_count = -1
        start_time = time.time()
        until_time_out = True
        try:
            while time.time() - start_time < time_out:
                current_count = len(self.driver.find_elements(by, detail))
                if current_count == last_count:
                    until_time_out = False
                    break
                last_count = current_count
                Waiter.wait(interval_time)
            if until_time_out:
                print(f"Time out in {inspect.currentframe().f_code.co_name} of {self.__class__}!")
            Waiter.wait(wait_time_before)
            elements = self.driver.find_elements(by, detail)
            Waiter.wait(wait_time_after)
        except Exception as e:
            print(f"An exception in {inspect.currentframe().f_code.co_name} of {self.__class__}!")
            print(f"Information: by={by}, detail={detail}")
            raise e
        return elements
    
    def select_value(self, by: str, detail: str, value: str, time_out: Optional[int] = None, wait_time_before: Optional[int] = None, wait_time_after: Optional[int] = None):
        if time_out is None:
            time_out = Waiter.TIME_OUT
        if wait_time_before is None:
            wait_time_before = int(0)
        if wait_time_after is None:
            wait_time_after = Waiter.get_wait_time_short()
        try:
            Waiter.wait(wait_time_before)
            element = Select(self.driver.find_element(by, detail))
            element.select_by_value(value)
            Waiter.wait(wait_time_after)
        except Exception as e:
            print(f"An exception in {inspect.currentframe().f_code.co_name} of {self.__class__}!")
            print(f"Information: by={by}, detail={detail}, value={value}")
            raise e
        
    def execute_script(self, script, args, wait_time_before: Optional[int] = None, wait_time_after: Optional[int] = None):
        if wait_time_before is None:
            wait_time_before = int(0)
        if wait_time_after is None:
            wait_time_after = Waiter.get_wait_time_medium()
        try:
            Waiter.wait(wait_time_before)
            self.driver.execute_script(script, args)
            Waiter.wait(wait_time_after)
        except Exception as e:
            print(f"An exception in {inspect.currentframe().f_code.co_name} of {self.__class__}!")
            print(f"Information: script={script}, args={args}")
            raise e