import requests
array_test_url = ["https://books.toscrape.com/media/cache/6d/41/6d418a73cc7d4ecfd75ca11d854041db.jpg",
                  "https://books.toscrape.com/media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg"]
for i in range(len(array_test_url)):
    image_name_dir = 'images/' + str(i) + '.png'
    #f = open(image_name_dir, 'wb')
    request_url = array_test_url[i]
    req = requests.get(request_url)
    if req.ok:
        with open(image_name_dir, 'wb') as img_file:
            img_file.write(requests.get(request_url).content)
        # f.write(requests.get(request_url).content)
        # f.close()
