import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/index.html"
req = requests.get(url)

if req.ok:
    res = BeautifulSoup(req.text, "html.parser")
    liste = res.find(class_="nav nav-list")
    lien = liste.findAll("a")
    for link in lien:
        print('http://books.toscrape.com/' + link.get('href'))
    """"
    arrayTest = []
    for test in lien:
        arrayTest.append(test)
    print(arrayTest[1:])
    """
