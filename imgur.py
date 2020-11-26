import requests
from random import randint
from bs4 import BeautifulSoup
from urllib import request, response, error, parse
from urllib.request import urlopen, Request
# from prettytable import PrettyTable

def imgur_search(query):
    URL = "https://imgur.com/search/relevance?q=" + query + "&qs=thumbs"
    hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    req = Request(URL,headers=hdr)
    html = request.urlopen(req)
    soup = BeautifulSoup(html, 'html.parser')

    images = soup.find_all("a", class_ = "image-list-link", href=True)

    if (not images):
        return "none were found, sorry :("

    image_array = []

    for image in images:
        image_array.append(image['href'])
    
    index = randint(0, len(image_array) - 1)

    return "https://imgur.com" + image_array[index]
