import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import re
import os


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

    # All Books Links
    array_product_page_url = []
    array_universal_product_code = []
    array_title = []
    array_price_incl_tax = []
    array_price_excl_tax = []
    array_numb_available = []
    array_description = []
    array_category = []
    array_img_url = []
    array_rating = []

    for i in arrayLinksBooksTxt:
        req = requests.get(i)
        if req.ok:
            res = BeautifulSoup(req.content, 'html.parser')
            # make an array of books links
            product_page_url = url
            array_product_page_url.append(product_page_url)
            # make an array of UPC
            universal_product_code = res.find(
                "th", text="UPC").find_next_sibling("td").text
            array_universal_product_code.append(universal_product_code)
            # make an array of titles
            title = (res.find("h1")).string
            array_title.append(title)
            # make an array of price include taxes
            price_including_tax = float((res.find(
                "th", text="Price (incl. tax)").find_next_sibling("td").text).split('£')[1])
            array_price_incl_tax.append(price_including_tax)
            # make an array of price excl taxes
            price_excluding_tax = float((res.find(
                "th", text="Price (excl. tax)").find_next_sibling("td").text).split('£')[1])
            array_price_excl_tax.append(price_excluding_tax)
            # make an array of number available
            stringSplit = (
                res.find("th", text="Availability").find_next_sibling("td").text)
            number_available = (re.split("[( | )]", stringSplit))[3]
            array_numb_available.append(number_available)
            # make an array of category
            findCategory = (
                res.find("li", {"class": "active"})).find_previous_sibling("li")
            category = (findCategory.find("a")).string
            array_category.append(category)
            # make an array of image link
            image_url = "https://books.toscrape.com/" + \
                ((((res.find(class_="item active")).find(
                    "img")).get("src")).split("../"))[2]
            array_img_url.append(image_url)
            # make an array of rating
            ratingStar = {
                "One": "1 sur 5",
                "Two": "2 sur 5",
                "Three": "3 sur 5",
                "Four": "4 sur 5",
                "Five": "5 sur 5"
            }
            find_rating = (((res.find(class_="instock availability")
                             ).find_next_sibling("p")).get("class"))[1]
            review_rating = ratingStar.get(find_rating)
            array_rating.append(review_rating)
            # make an array of description
            description = (
                (res.find(class_="sub-header")).find_next_sibling("p"))
            if description is not None:
                get_description = description.text
                array_description.append(get_description)
            else:
                description = None
                array_description.append(description)

    data_dict = {
        'product_page_url': array_product_page_url,
        'universal_ product_code': array_universal_product_code,
        'title': array_title,
        'price_including_tax (£)': array_price_incl_tax,
        'price_excluding_tax (£)': array_price_excl_tax,
        'number_available': array_numb_available,
        'product_description': array_description,
        'category': array_category,
        'review_rating': array_rating,
        'image_url': array_img_url
    }

    # Create DataFrame
    data = pd.DataFrame(data_dict)
    # Write to CSV file
    data.to_csv("products.csv")

    # read DataFrame
    data = pd.read_csv("products.csv")
    if not os.path.isdir('./categories'):
        os.makedirs("./categories")
        for (Category), group in data.groupby(['category']):
            group.to_csv(f'categories/{Category}.csv', index=False)

    # Download Images
    # check if there is a folder call "images" in Directory if not creact it
    if not os.path.isdir('./images'):
        os.makedirs("./images")
        for i in range(len(array_img_url)):
            image_name_dir = 'images/' + str(i) + '.png'
            request_url = array_img_url[i]
            response = requests.get(request_url)
            if response.ok:
                with open(image_name_dir, 'wb') as img_file:
                    img_file.write(requests.get(request_url).content)
