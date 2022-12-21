import requests
from bs4 import BeautifulSoup
import csv
import os
import re


url = "http://books.toscrape.com/index.html" 
req = requests.get(url)
if req.ok:
    res = BeautifulSoup(req.text, "html.parser")
    liste = res.find(class_="nav nav-list")
    links = liste.findAll("a")
    array_links = []
    for link in links:
        array_links.append('http:'+'//books.toscrape.com/' + link.get('href'))
   
    for i in array_links[1:]:
        req = requests.get(i)  
        if req.ok:
            print(req)
            array_links_book_txt = [] 
            res = BeautifulSoup(req.text, "html.parser")
            file_Name = res.find('h1').string
            #creer un fichier categorie
            if not os.path.isdir('./categories'):
                os.makedirs("./categories")
            with open("categories/" + file_Name + ".csv", 'w') as csv_file:
                liste = res.findAll(class_="image_container")
                link_next = res.find(class_="current")
                url_split = i.split('/index.html')[0]
                print("scapping...")
                if link_next:
                        number_of_page = (link_next.string).split('of')[1].strip()
                        for a in range(1, int(number_of_page) + 1):
                            url_next = url_split + '/' + 'page-'+str(a)+'.html'
                            req = requests.get(url_next)
                            res = BeautifulSoup(req.text, "html.parser")
                            liste = res.findAll(class_="image_container")
                            for link in liste:
                                for col in link.findAll('a'):
                                    link_native = col.get('href').split('../')[3]
                                    array_links_book_txt.append(
                                        'https://books.toscrape.com/catalogue/' + link_native)
                else:
                    for link in liste:
                        for col in link.findAll('a'):
                            link_native = col.get('href').split('../')[3]
                            array_links_book_txt.append(
                                'https://books.toscrape.com/catalogue/' + link_native)
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
                print("please wait...")
                for y in array_links_book_txt:
                    req = requests.get(y)
                    if req.ok:
                        res = BeautifulSoup(req.content, 'html.parser')
                        # make an array of books links
                        product_page_url = y
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
                en_tete = ['product_page_url', 'universal_product_code', 'title', 'price_incl_tax', 'price_excl_tax', 'numb_available', 'description', 'category', 'img_url', 'rating']
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow(en_tete)
                for product_page_url,universal_product_code, title,price_incl_tax, price_excl_tax, numb_available,description,category, img_url, rating in zip(array_product_page_url, array_universal_product_code, array_title, array_price_incl_tax, array_price_excl_tax, array_numb_available, array_description,array_category, array_img_url,array_rating):

                    writer.writerow([product_page_url,universal_product_code, title,price_incl_tax, price_excl_tax, numb_available,description,category, img_url, rating])
                print("your " + file_Name + " csv file is created")
                if not os.path.isdir('./images'+'/'+ file_Name):
                    os.makedirs("./images"+'/'+ file_Name)
                print("download image")
                for i in range(len(array_img_url)):
                    image_name_dir = 'images/'+ file_Name+'/'+ str(i) + '.png'
                    request_url = array_img_url[i]
                    response = requests.get(request_url)
                    if response.ok:
                        with open(image_name_dir, 'wb') as img_file:
                            img_file.write(requests.get(request_url).content)
        
print("Finish")          
