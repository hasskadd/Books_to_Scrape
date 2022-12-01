import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/index.html"
req = requests.get(url)
res = BeautifulSoup(req.text, "html.parser")
liste = res.find(class_="nav nav-list")
lien = liste.findAll("a")
arrayTest = []
for test in lien:
    arrayTest.append(test)
print(arrayTest[1])
