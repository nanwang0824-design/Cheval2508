# utils.py

import re
from typing import List, Tuple

def order_str_to_int(order_str: str):
    """transform the string of arrival order to int"""
    mapping = {"失格": -20, "中止": -30, "除外": -40, "取消": -50}
    order = mapping.get(order_str)
    if order:
        return order
    else:
        return int(order_str)
    
def sexage_to_sex_age(sexage: str):
    """transform the string (牝3, 牡5, せん6, and so on) of sex and age to seperated values"""
    pattern = r"(.+?)(\d+)"
    match = re.match(pattern, sexage)
    if match:
        sex: str = match.group(1)
        age = int(match.group(2))
        return sex, age
    else:
        return str(""), int(0)
    
def minsec_to_sec(minsec: str):
    temp = minsec.split(":")
    return float(temp[0]) * 60 + float(temp[1])

def extract_class_race(html: str):
    """"""
    pattern = r'''<td class="race">(?:<a href="/JRADB/accessS\.html\?CNAME=([^"]+)">)?([^<]+)(?:</a>)?</td>'''
    match = re.search(pattern, html)
    if match:
        code = match.group(1)
        name = match.group(2)
        return code, name
    else:
        return None, None

def extract_class_jockey(html: str):
    """"""
    pattern = r'''<td class="jockey">(?:<a href="#" onclick="return doAction\(\'/JRADB/accessK\.html\', \'(.*?)\'\);">)?(.*?)(?:</a>)?</td>'''
    match = re.search(pattern, html)
    if match:
        code = match.group(1)
        name = match.group(2)
        return code, name
    else:
        return None, None
    
def extract_dd_horse(html: str):
    """"""
    pattern = r'''<dd>(?:<a href="/JRADB/accessU\.html\?CNAME=([^"]+)">)?([^<]+)(?:</a>)?(?:<span class="sanku">.*?</span>)?</dd>'''
    match = re.search(pattern, html)
    if match:
        code = match.group(1)
        name = match.group(2)
        return code, name
    else:
        return None, None
    
def extract_dd_trainer(html: str):
    """"""
    pattern = r'''<dd><a href="#" onclick="return doAction\(\'/JRADB/accessC\.html\', \'(.*?)\'\);">(.*?)</a>(.*?)</dd>'''
    match = re.search(pattern, html)
    if match:
        code = match.group(1)
        name = match.group(2)
        affiliation = match.group(3).replace("（", "").replace("）", "")
        return code, name, affiliation
    else:
        return None, None, None


def extract_doaction_code(onclick_str):
    """Extract the second parameter from the doAction JS call"""
    match = re.search(r"doAction\([^,]+,\s*'([^']+)'\)", onclick_str)
    return match.group(1) if match else None

def extract_cname_code(link_str):
    """Extract the parameter from the href with the form /JRADB/accessS.html?CNAME="""
    match = re.search(r"CNAME=([^&]+)", link_str)
    return match.group(1) if match else None

def year_month_range(start_year: int, start_month: int, end_year: int, end_month: int) -> List[Tuple[int, int]]:
    """
    Generate a list of months from the start year and month to the end year and month (not included)
    Example: month_range(2021, 10, 2022, 3)
         -> [(2021, 10), (2021, 11), (2021, 12), (2022, 1), (2022, 2)]
    """
    result = []
    year, month = start_year, start_month
    while (year, month) < (end_year, end_month):
        result.append((year, month))
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
    return result

if __name__ == "__main__":
    # example of extract_class_race
    html = '<td class="race">金沢城賞</td>'
    print(extract_class_race(html))
    html = '''<td class="race"><a href="/JRADB/accessS.html?CNAME=pw01sde1009202401040720240303/55">4歳上1勝クラス</a></td>'''
    print(extract_class_race(html))

    # example
    html = '''<td class="jockey">田中 学</td>'''
    print(extract_class_jockey(html))
    html = '''<td class="jockey"><a href="#" onclick="return doAction('/JRADB/accessK.html', 'pw04kmk001122/66');">三浦 皇成</a></td>'''
    print(extract_class_jockey(html))

    # example of extract_dd_horse
    html = '<dd>American Pharoah</dd>'
    print(extract_dd_horse(html))
    html = '''<dd>Limari<span class="sanku"><a href="#" onclick="return doAction('/JRADB/accessU.html', 'pj01snk101240035026/16');">産駒</a></span></dd>'''
    print(extract_dd_horse(html))
    html = '''<dd><a href="/JRADB/accessU.html?CNAME=pw01dud101992109618/50">フジキセキ</a></dd>'''
    print(extract_dd_horse(html))
    html = '''<dd><a href="/JRADB/accessU.html?CNAME=pw01dud102000102682/39">ピサノヒビキ</a><span class="sanku"><a href="#" onclick="return doAction('/JRADB/accessU.html', 'pj01snk101220049933/3A');">産駒</a></span></dd>'''
    print(extract_dd_horse(html))

    # example of order_str_to_int
    print(order_str_to_int("5"), order_str_to_int("失格"), order_str_to_int("取消"))