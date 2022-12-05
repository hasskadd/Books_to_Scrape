import requests
url = "https://books.toscrape.com/media/cache/6d/41/6d418a73cc7d4ecfd75ca11d854041db.jpg"
response = requests.get(url)
open('images/test.jpg', "wb").write(response.content)
