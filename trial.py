from urllib.request import urlopen
from bs4 import BeautifulSoup as beautifulsoup

url = "http://pythonscraping.com/pages/page1.html"

html = urlopen(url)

bs = beautifulsoup(html, "html.parser")

print(bs.title)
