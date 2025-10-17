# test_database.py

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.cheval.storage.database import ChevalDB

def export_to_excel():
    db = ChevalDB()
    db.export_to_excel()

if __name__ == "__main__":
    print("Hello")
    export_to_excel()