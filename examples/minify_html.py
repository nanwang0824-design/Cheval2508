# minify_html.py

import re
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from examples import html

def minify_html(html: str, filename: str ="minified_html.html"):
    """
    compress an HTML string into a single line HTML, removes extra spaces and line breaks, and saves it to the specified file
    Parameters:
        html: HTML string
        filepath: output file name
    Returns:
        compressed HTML string
    """
    # remove whitespace between tags
    compressed = re.sub(r">\s+<", "><", html)
    # shrink consecutive spaces into one space
    compressed = re.sub(r"\s+", " ", compressed)
    compressed = compressed.strip()
    # write result to file
    current_dir = os.path.dirname(__file__)
    filepath = os.path.join(current_dir, filename)
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(compressed)
    return compressed

if __name__ == "__main__":
  html = html.html_jockey_summary_1
  minify_html(html)