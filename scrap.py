import requests
from bs4 import BeautifulSoup
import csv

url = "http://books.toscrape.com/index.html"
req = requests.get(url)

if req.ok:
    res = BeautifulSoup(req.text, "html.parser")
    liste = res.find(class_="nav nav-list")
    links = liste.findAll("a")
    arrayLinks = []
    for link in links:
        arrayLinks.append('http://books.toscrape.com/' + link.get('href'))
    # print(arrayLinks)
    with open("links.csv", 'w') as dataLinks:
        writer = csv.writer(dataLinks, delimiter='\n')
        writer.writerow(arrayLinks)
