import re

from parsers.horse_parser import HorseParser
from parsers.jockey_parser import JockeyParser
from parsers.trainer_parser import TrainerParser
from parsers.race_parser import RaceParser
from parsers.match_parser import MatchParser
from parsers.match_list_parser import MatchListParser
import examples.html

def minify_html(html: str, filepath: str ="minified.html"):
    """
    将HTML字符串压缩为单行HTML，去掉多余的空格和换行，并保存到指定的文件。
    
    参数:
        html : HTML字符串
        filepath     : 输出文件路径 (默认 "minified.html")
    返回:
        压缩后的 HTML 字符串
    """
    # 删除标签之间的空白
    compressed = re.sub(r">\s+<", "><", html)
    # 连续空格缩成一个空格
    compressed = re.sub(r"\s+", " ", compressed)
    #compressed = compressed.strip()
    # 写入文件
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(compressed)
    return compressed

if __name__ == "__main__":
  
  #html = examples.html.html_race_1
  #minify_html(html)
  #exit()
  
  html = examples.html.html_macth_list_1
  #minify_html(html)
  parser = MatchListParser()
  d1 = parser.parse(html=html)
  print(d1)
  
  html = examples.html.html_macth_list_2
  #minify_html(html)
  parser = MatchListParser()
  d1 = parser.parse(html=html)
  print(d1)
  exit()

  html = examples.html.html_match_1
  #minify_html(html)
  parser = MatchParser()
  thematch, d1, d2 = parser.parse(html=html)
  print(thematch)
  print(d1)
  print(d2)
  exit()

  html = examples.html.html_race_1
  #minify_html(html)
  parser = RaceParser()
  race, d1, d2, d3 = parser.parse(html=html)
  print(race)
  print(d1)
  print(d2)
  print(d3)
  exit()

  html = examples.html.html_trainer_1
  #minify_html(html)
  parser = TrainerParser()
  trainer = parser.parse(html=html)
  html = examples.html.html_trainer_summary_1
  trainer.summary_past = parser.parse_for_past(html=html)
  print(trainer)
  exit()

  html = examples.html.html_jockey_1
  #minify_html(html)
  parser = JockeyParser()
  jockey = parser.parse(html=html)
  #print(jockey.summary_this_year)
  #print(jockey.summary_total)
  html = examples.html.html_jockey_summary_1
  jockey.summary_past = parser.parse_for_past(html=html)
  print(jockey)
  #print(f"this year: {len(jockey.summary_this_year)}\ntotal: {len(jockey.summary_total)}\npast: {len(jockey.summary_past)}")
  exit()

  html = examples.html.html_horse_1
  #minify_html(html)
  parser = HorseParser()
  horse = parser.parse(html=html)
  print(horse)
  exit()
  