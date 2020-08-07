import requests
from bs4 import BeautifulSoup
from urllib import request, response, error, parse
from urllib.request import urlopen
from prettytable import PrettyTable

def getCorrectLane(lane):
    if lane == 'mid' or lane == 'middle':
        return 'MID'
    elif lane == 'top':
        return 'TOP'
    elif lane == 'bot' or lane =='bottom' or lane == 'adc':
        return 'ADC'
    elif lane == 'sup' or lane == 'supp' or lane == 'support':
        return 'SUPPORT'
    elif lane == 'jg' or lane == 'jungle':
        return 'JUNGLE'
    else:
        return False

def getinfo(summoner_name):
    URL = "https://na.op.gg/summoner/userName=" + summoner_name
    html = urlopen(URL)
    soup = BeautifulSoup(html, 'html.parser')

    KDAArray = []
    namesArray = []
    gameTypeArray = []
    gameResultArray = []
    finishedArray = []

    div = soup.find_all('div', class_='GameItemList')
    rank = soup.find('div', class_='TierRank').get_text()

    for elem in div:
        wrappers = elem.find_all('div', class_='KDA')
        for x in wrappers:
            # this is from op.gg's html that puts a KDA inside KDA to prevent duplication
            innerKDA = x.find_all('div', class_="KDA")      
            for i in innerKDA:
                kill = i.find('span', class_="Kill").get_text()
                death = i.find('span', class_="Death").get_text()
                assist = i.find('span', class_="Assist").get_text()
                KDAArray.append(kill + "/" + death + "/" + assist)
        names = elem.find_all('div', class_='ChampionName')
        for x in names:
            name = x.find('a').get_text()
            namesArray.append(name)
        gameStats = elem.find_all('div', class_='GameStats')
        for x in gameStats:
             # replace for the weird formatting gotten from op.gg   
            gameType = x.find('div', class_='GameType').get_text().replace("\t", "").replace("\n", "")        
            gameResult = x.find('div', class_='GameResult').get_text().replace("\t", "").replace("\n", "")                                         
            gameTypeArray.append(gameType)
            gameResultArray.append(gameResult)

    table = PrettyTable(['Result', 'Champion', 'KDA', 'Game Type'])

    for i in range(10):
        table.add_row([gameResultArray[i], namesArray[i], KDAArray[i], gameTypeArray[i]])
    
    return rank + "\n" + "-----------" + "\n" + "```" + str(table) + "```"

def runes(champ, lane):
    URL = "https://na.op.gg/champion/" + champ + "/statistics/" + lane
    html = urlopen(URL)
    soup = BeautifulSoup(html, 'html.parser')

    if getCorrectLane(lane) != False:
        lane = getCorrectLane(lane)
    else: 
        return "try again but don't type it weirdly"
    
    fullTrees = ''
    tree = []
    count = 1
    statArray = []

    splitTrees = soup.find_all('div', class_='perk-page-wrap')
    stats1 = soup.find_all('tbody', class_='tabItem ChampionKeystoneRune-1')
    stats2 = soup.find_all('tbody', class_='tabItem ChampionKeystoneRune-2')
    stats = [stats1, stats2]

    winRate = ''
    pickRate = ''

    for j in stats:
        for i in j:
            separateStats = i.find_all('td', class_='champion-overview__stats champion-overview__stats--pick')
            for x in separateStats:
                pickRate = x.find('span', class_='pick-ratio__text')
                pr_value = pickRate.find_next('strong').get_text()
                winRate = x.find('span', class_='win-ratio__text')
                wr_value = winRate.find_next('strong').get_text()
                statArray.append('Pick Rate: ' + pr_value + '\tWin Rate: ' + wr_value)

    for i in splitTrees:
        keystoneWrapper = i.find_all('div', class_='perk-page__item perk-page__item--keystone perk-page__item--active')
        for x in keystoneWrapper:
            rune = x.find('img', alt=True)
            tree.append(rune.get('alt'))
        otherRuneWrapper = i.find_all('div', class_='perk-page__item perk-page__item--active')
        for x in otherRuneWrapper:
            lowerRune = x.find('img', alt=True)
            tree.append(lowerRune.get('alt'))
        fullTrees += 'RUNE PAGE ' + str(count) + '\t' + statArray[count - 1] + '\n' + str(tree) + '\n\n'
        tree.clear()
        count += 1
    
    return '```' + fullTrees + '```'