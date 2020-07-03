import requests
from bs4 import BeautifulSoup
from urllib import request, response, error, parse
from urllib.request import urlopen

def get_word():
    URL = "https://www.wordnik.com/words/?random=true"
    html = urlopen(URL)
    soup = BeautifulSoup(html, 'html.parser')
    word = soup.find("h1", class_="tain ascenders").get_text().replace("\t", "").replace("\n", "") 
    return word

def get_definition(word):
    URL = "https://www.wordnik.com/words/" + word
    html = urlopen(URL)
    soup = BeautifulSoup(html, 'html.parser')
    definition_wrapper = soup.find_all('div', class_="guts active")
    definition = ''
    for x in definition_wrapper:
        definition = x.find('li').get_text()
    return definition
        
