import discord, asyncio
import requests
import math
import random
import os
from bs4 import BeautifulSoup
from random import randint
from discord.ext import commands
from discord import User
from asyncio import sleep
from urllib import request, response, error, parse
from urllib.request import urlopen
from prettytable import PrettyTable

client = commands.Bot(command_prefix='?')

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


@client.command()
async def getinfo(ctx, summoner_name):
    channel = ctx.channel
    URL = "https://na.op.gg/summoner/userName=" + summoner_name
    html = urlopen(URL)
    soup = BeautifulSoup(html, 'html.parser')

    KDAArray = []
    namesArray = []
    gameTypeArray = []
    finishedArray = []

    div = soup.find_all('div', class_='GameItemList')
    rank = soup.find('div', class_='TierRank').get_text()

    for elem in div:
        wrappers = elem.find_all('div', class_='KDA')
        for x in wrappers:
            innerKDA = x.find_all('div', class_="KDA")      # this is from op.gg's html that puts a KDA inside KDA to prevent duplication
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
            gameType = x.find('div', class_='GameType').get_text().replace("\t", "").replace("\n", "")    # replace for the weird formatting gotten from op.gg                                                
            gameTypeArray.append(gameType)

    for i in range(10):
        finishedArray.append(namesArray[i] + " " + KDAArray[i] + " --- " + gameTypeArray[i])
    
    await channel.send(rank + "\n" + "------------" + "\n")
    await channel.send('\n'.join(finishedArray))

@client.command()
async def tier(ctx, lane):
    channel = ctx.channel
    URL = "https://na.op.gg/champion/statistics"
    html = urlopen(URL)
    soup = BeautifulSoup(html, 'lxml')

    if getCorrectLane(lane) != False:
        lane = getCorrectLane(lane)
    else: 
        await channel.send("try again but don't type it weirdly")
    
    champArray = []
    pickRateArray = []
    winRateArray = []
    numArray = []

    laneClass = 'tabItem champion-trend-tier-' + lane
    wrapper = soup.find_all('tbody', class_=laneClass)
    
    for x in wrapper:
        numWrapper = x.find_all('td', 'champion-index-table__cell champion-index-table__cell--rank')
        print(numWrapper)
        for i in numWrapper:
            champNum = i.get_text()
            numArray.append(champNum)
        champWrapper = x.find_all('td', class_="champion-index-table__cell champion-index-table__cell--champion")
        for i in champWrapper:
            champName = i.find('div', class_='champion-index-table__name').get_text()
            champArray.append(champName)

        winValueWrapper = x.find_all('td', 'champion-index-table__cell champion-index-table__cell--value')
        for i, y in enumerate(winValueWrapper):
            if i % 3 == 0:
                winValue = y.get_text()
                winRateArray.append(winValue)
            elif i % 3 == 1:
                pickRate = y.get_text()
                pickRateArray.append(pickRate)
            else:
                continue

    top = PrettyTable(['Number','Champion', 'Win Rate', 'Pick Rate'])
    bottomHalf = PrettyTable(['Number','Champion', 'Win Rate', 'Pick Rate'])

    roundDownLength = math.floor(len(champArray)/2)
    count = 0                                               # this stuff has to happen because 2000 limit per message in discord
    for i in range(roundDownLength):
        top.add_row([numArray[i], champArray[i], winRateArray[i], pickRateArray[i]])
        count+=1

    await channel.send('```' + str(top) + '```')            # submit as code block because of spacing restrictions

    while count < len(champArray):
        bottomHalf.add_row([numArray[count], champArray[count], winRateArray[count], pickRateArray[count]])
        count += 1

    await channel.send('```' + str(bottomHalf) + '```')

@client.command()
async def runes(ctx, champ, lane):
    channel = ctx.channel
    URL = "https://na.op.gg/champion/" + champ + "/statistics/" + lane
    html = urlopen(URL)
    soup = BeautifulSoup(html, 'lxml')

    if getCorrectLane(lane) != False:
        lane = getCorrectLane(lane)
    else: 
        await channel.send("try again but don't type it weirdly")
    
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
    
    await channel.send(fullTrees)

@client.command()
async def flip(ctx):
    channel = ctx.channel
    random_num = randint(0,1)
    if random_num == 0:
        await channel.send("HEADS")
    elif random_num == 1:
        await channel.send("TAILS")

@client.command()
async def spam(ctx, user: User):
    for _ in range(20):
        await ctx.send(user.mention)
        await sleep(1)


@client.event
async def on_ready():
    print('bot is online')


client.run(os.environ.get('MY_TOKEN'))