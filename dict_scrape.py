import requests
from bs4 import BeautifulSoup
from urllib import request, response, error, parse
from urllib.request import urlopen, Request

def get_word():
    URL = "https://www.wordnik.com/words/?random=true"
    hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    req = Request(URL,headers=hdr)
    html = request.urlopen(req)
    soup = BeautifulSoup(html, 'html.parser')
    word = soup.find("h1", class_="tain ascenders").get_text().replace("\t", "").replace("\n", "") 
    return word

def get_definition(word):
    URL = "https://www.wordnik.com/words/" + word
    hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    req = Request(URL,headers=hdr)
    html = request.urlopen(req)
    soup = BeautifulSoup(html, 'html.parser')
    definition_wrapper = soup.find_all('div', class_="guts active")
    definition = []
    count = 1
    if soup.find_all("p", class_="weak"):
        return 'no definition found'
    for x in definition_wrapper:
        definitions = x.find_all('ul')
        for i in definitions:
            singular_def = i.find('li').get_text()
            definition.append(str(count) + ". " + singular_def)
            count += 1
    return "\n".join(definition)
