import requests
from bs4 import BeautifulSoup
from urllib import request, response, error, parse
from urllib.request import urlopen, Request
from prettytable import PrettyTable


def best_pick(champion):
    URL = "https://u.gg/lol/champions/" + champion + "/counter?rank=overall"
    hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    req = Request(URL,headers=hdr)
    html = request.urlopen(req)
    soup = BeautifulSoup(html, 'html.parser')

    best_names = []
    best_wr = []
    num_of_games = []

    best_wrapper = soup.find_all("a", class_="counter-list-card best-win-rate")

    for x in best_wrapper:
        best_names.append(x.find("div", class_="champion-name").get_text())
        best_wr.append(x.find("div", class_="win-rate").get_text())
        num_of_games.append(x.find("div", class_="total-games").get_text())
    
    table = PrettyTable(['Rank', 'Name', 'Win Rate', 'Total Games'])

    for i in range(len(best_names)):
        table.add_row([i + 1, best_names[i], best_wr[i], num_of_games[i]])

    return "Overall Counters for " + champion + "\n" + str(table)

def worst_picks(champion):
    URL = "https://u.gg/lol/champions/" + champion + "/counter?rank=overall"
    hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    req = Request(URL,headers=hdr)
    html = request.urlopen(req)
    soup = BeautifulSoup(html, 'html.parser')

    worst_names =[]
    worst_wr = []
    num_of_games = []

    worst_wrapper = soup.find_all("a", class_="counter-list-card worst-win-rate")

    for x in worst_wrapper:
        worst_names.append(x.find("div", class_="champion-name").get_text())
        worst_wr.append(x.find("div", class_="win-rate").get_text())
        num_of_games.append(x.find("div", class_="total-games").get_text())

    table = PrettyTable(['Rank', 'Name', 'Win Rate', 'Total Games'])

    for i in range(len(worst_names)):
        table.add_row([i + 1, worst_names[i], worst_wr[i], num_of_games[i]])

    return "Worst Picks Against " + champion + "\n" + str(table)

def best_lane_picks(champion):
    URL = "https://u.gg/lol/champions/" + champion + "/counter?rank=overall"
    hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    req = Request(URL,headers=hdr)
    html = request.urlopen(req)
    soup = BeautifulSoup(html, 'html.parser')

    best_lane_names =[]
    gold_dif = []
    num_of_games = []

    worst_wrapper = soup.find_all("a", class_="counter-list-card gold-diff")

    for x in worst_wrapper:
        best_lane_names.append(x.find("div", class_="champion-name").get_text())
        gold_dif.append(x.find("div", class_="win-rate").get_text())
        num_of_games.append(x.find("div", class_="total-games").get_text())

    table = PrettyTable(['Rank', 'Name', 'Gold Diff at 15', 'Total Games'])

    for i in range(len(best_lane_names)):
        table.add_row([i + 1, best_lane_names[i], gold_dif[i], num_of_games[i]])

    return "Best Lane Picks Against " + champion + "\n" + str(table)
