import requests
from bs4 import BeautifulSoup
from urllib import request, response, error, parse
from urllib.request import urlopen, Request
from prettytable import PrettyTable

def get_usa_cases():
    URL = "https://www.worldometers.info/coronavirus/country/us/"
    # hdr used because worldometers thinks we are a bot
    hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    req = Request(URL,headers=hdr)
    html = request.urlopen(req)
    soup = BeautifulSoup(html, 'html.parser')

    # main = soup.find_all('div', class_='maincounter-number')
    # for x in main:
    #     num = x.find('span').get_text()
    # print("total: "+ num)
    total_usa = ""
    usa_graph_wrapper = soup.find_all('table', id="usa_table_countries_today")
    for x in usa_graph_wrapper:
        total_usa = x.find('td')
        print(total_usa)

get_usa_cases()
