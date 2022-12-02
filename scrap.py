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
        arrayLinks.append('http:'+'//books.toscrape.com/' + link.get('href'))
    # print(arrayLinks)
    with open("links.txt", 'w') as dataLinks:
        for link in arrayLinks:
            dataLinks.write(link + '\n')

    with open("links.txt", 'r') as file:
        next(file)  # Lire a partir de la deuxieme ligne du fichier
        arrayLinksBooksTxt = []
        for row in file:
            # print(row)

            url = row.strip()
            requete = requests.get(url)
            # print(requete)
            arrayBooksLink = []

            if requete.ok:
                res = BeautifulSoup(requete.text, "html.parser")
                liste = res.findAll(class_="image_container")
                linkNext = res.find(class_="current")
                arrayLinksBooks = []
                urlSplit = url.split('/index.html')[0]

                if linkNext:
                    numberOfPage = (linkNext.string).split('of')[1].strip()
                    for i in range(1, int(numberOfPage) + 1):
                        urlNext = urlSplit + '/' + 'page-'+str(i)+'.html'
                        req = requests.get(urlNext)
                        res = BeautifulSoup(req.text, "html.parser")
                        liste = res.findAll(class_="image_container")
                        for link in liste:
                            for col in link.findAll('a'):
                                linkNative = col.get('href').split('../')[3]
                                # print(
                                # 'https://books.toscrape.com/catalogue/' + linkNative)
                                arrayLinksBooksTxt.append(
                                    'https://books.toscrape.com/catalogue/' + linkNative)
                else:
                    for link in liste:
                        for col in link.findAll('a'):
                            linkNative = col.get('href').split('../')[3]
                            # print(
                            # 'https://books.toscrape.com/catalogue/' + linkNative)
                            arrayLinksBooksTxt.append(
                                'https://books.toscrape.com/catalogue/' + linkNative)
        print(arrayLinksBooksTxt)
        with open("allBooksLinks.txt", 'w') as dataF:
            for link in arrayLinksBooksTxt:
                dataF.write(link + '\n')
        print('_____________________________')
