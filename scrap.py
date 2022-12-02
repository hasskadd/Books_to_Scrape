import requests
from bs4 import BeautifulSoup
import csv
import time

url = "http://books.toscrape.com/index.html"
req = requests.get(url)

if req.ok:
    res = BeautifulSoup(req.text, "html.parser")
    liste = res.find(class_="nav nav-list")
    links = liste.findAll("a")
    arrayLinks = []
    for link in links:
        arrayLinks.append('http:'+'//books.toscrape.com/' + link.get('href'))
    # print(arrayLinks)
    with open("links.txt", 'w') as dataLinks:
        # writer = csv.writer(dataLinks, delimiter='\n')
        # writer.writerow(arrayLinks[1:2])
        for link in arrayLinks:
            dataLinks.write(link + '\n')

    with open("links.txt", 'r') as file:
        next(file)  # Lire a partir de la deuxieme ligne du fichier
        for row in file:
            print(row)
            url = row.strip()
            requete = requests.get(url)
            print(requete)
            if requete.ok:
                res = BeautifulSoup(requete.text, "html.parser")
                liste = res.findAll(class_="image_container")
                #linksBooks = liste.findchildren('a')
               # print(liste.next_sibling)

                arrayLinksBooks = []
                for link in liste:
                    for col in link.findAll('a'):
                        linkNative = col.get('href').split('../')[3]
                        print(linkNative)

""""
                    # splitLink = link.get('href').split('../')[3]
                   # print(splitLink)
                    # arrayLinksBooks.append(
                    # 'http://books.toscrape.com/catalogue/' + splitLink)

                    # time.sleep(3)
                # print(arrayLinksBooks)

"""
