# test_misc.py

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import inspect

class Father:
    def __init__(self):
        self.name = "father name"
    def printname(self):
        print(self.name)
        print(f"method {inspect.currentframe().f_code.co_name} of {self.__class__}!")
        self._printname()
    def _printname(self):
        print(f"method {inspect.currentframe().f_code.co_name} of {self.__class__}!")

class Child(Father):
    def __init__(self):
        self.name = "child name"
    def printname(self):
        print(self.name)
        print(f"method {inspect.currentframe().f_code.co_name} of {self.__class__}!")
        self._printname()
    def _printname(self):
        print(f"method {inspect.currentframe().f_code.co_name} of {self.__class__}!")

if __name__ == "__main__":
    print("Hello")