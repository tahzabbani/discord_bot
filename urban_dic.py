import requests
from bs4 import BeautifulSoup
from urllib import request, response, error, parse
from urllib.request import urlopen
from random import randint

def get_rand_urban():
    rand_page_num = randint(1,1000)
    URL = "https://www.urbandictionary.com/random.php?page=" + str(rand_page_num)
    html = urlopen(URL)
    soup = BeautifulSoup(html, 'html.parser')
    word_list = []
    definition_list = []
    example_list = []

    panel_wrapper = soup.find_all('div', class_='def-panel')
    for x in panel_wrapper:
        word = x.find('div', class_='def-header').get_text()
        meaning = x.find('div', class_='meaning').get_text()
        example = x.find('div', class_='example').get_text()
        word_list.append(word)
        definition_list.append(meaning)
        example_list.append(example)

    random_word_num = randint(0, len(word_list) - 1)
    
    return word_list[random_word_num] + '\n\n' + definition_list[random_word_num] + '\n\nExample:\n' + example_list[random_word_num]