import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/index.html"
req = requests.get(url)
res = BeautifulSoup(req.text, "html.parser")

print(res)
