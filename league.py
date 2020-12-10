import requests
from bs4 import BeautifulSoup
from urllib import request, response, error, parse
from urllib.request import urlopen, Request
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
        return 'Wrong'

# from league of graphs - lots of good information
def playedChamps(summoner_name):
    URL = "https://www.leagueofgraphs.com/summoner/champions/na/" + summoner_name + "/all#championsData-all-queues"
    hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    req = Request(URL,headers=hdr)
    html = request.urlopen(req)
    soup = BeautifulSoup(html, 'html.parser')

    champ_name_array = []
    KDA_array = []
    kill_array = []
    death_array = []
    assist_array = []
    game_num_array = []
    winrate_array = []

    # the 6th occurence of the content class
    table = soup.find_all('div', class_='content')[6]
    kills = table.find_all('span', class_='kills')
    deaths = table.find_all('span', class_='deaths')
    assists = table.find_all('span', class_='assists')
    names = table.find_all('span', class_='name')
    games_winrate = table.find_all('a', class_='full-cell', href=True)

    for x in kills:
        kill_text = x.get_text()
        kill_array.append(kill_text)
    for x in deaths:
        death_text = x.get_text()
        death_array.append(death_text)
    for x in assists:
        assist_text = x.get_text()
        assist_array.append(assist_text)

    for i in range(len(kill_array)):
        KDA_array.append(kill_array[i] + "/" + death_array[i] + "/" + assist_array[i])

    # this is a pain in THE ASS just to get winrates/games
    for i, x in enumerate(games_winrate):
        if (i % 2 == 0):
            progress_bar = x.find_all('progressbar')
            game_value = ''.join(map(str, progress_bar)) 
            find_index = game_value.find('data-value=')
            if (find_index != -1):
                new_string = game_value[find_index:find_index + 20]
                split_string = new_string.split('"')
                data = split_string[1]
                game_num_array.append(data)
        else:
            progress_bar = x.find_all('progressbar')
            game_value = ''.join(map(str, progress_bar)) 
            find_index = game_value.find('data-value=')
            if (find_index != -1):
                new_string = game_value[find_index:find_index + 20]
                split_string = new_string.split('"')
                data = "{:.2%}".format(float(split_string[1]))
                winrate_array.append(data)

    for x in names:
        name_wrapper = x.get_text().strip()
        champ_name_array.append(name_wrapper)

    pretty_table = PrettyTable(['Champion', 'Games', 'Winrate', 'KDA'])

    for i in range(len(names)):
        pretty_table.add_row([champ_name_array[i], game_num_array[i], str(winrate_array[i]), KDA_array[i]])

    return pretty_table        

def getinfo(summoner_name):
    URL = "https://na.op.gg/summoner/userName=" + summoner_name
    html = urlopen(URL)
    soup = BeautifulSoup(html, 'html.parser')

    KDAArray = []
    namesArray = []
    gameTypeArray = []
    gameResultArray = []

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

    if getCorrectLane(lane) != 'Wrong':
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