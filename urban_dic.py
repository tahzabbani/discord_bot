import requests
from bs4 import BeautifulSoup
from urllib import request, response, error, parse
from urllib.request import urlopen, Request
from random import randint
import urbandictionary as ud

def get_rand_urban():
    rand = ud.random()
    rand_selection = randint(0, len(rand) - 1)
    return rand[rand_selection].word + '\n\n' + rand[rand_selection].definition + '\n\nExample:\n' + rand[rand_selection].example

