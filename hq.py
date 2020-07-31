import discord, asyncio
import requests
import math
import random
import os
import dict_scrape
import urban_dic
import luke_methods
import counters
from bs4 import BeautifulSoup
from random import randint
from discord.ext import commands
from discord import User
from asyncio import sleep
from urllib import request, response, error, parse
from urllib.request import urlopen
from prettytable import PrettyTable

client = commands.Bot(command_prefix='?')
# for the initial help command it provides
client.remove_command("help")                   

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
async def build(ctx, champion, lane):
    if getCorrectLane(lane) != False:
        lane = getCorrectLane(lane)
    else: 
        await ctx.channel.send("try again but don't type it weirdly")
    await ctx.channel.send("```" + luke_methods.get_build(champion, lane) + "```")

@client.command()
async def skills(ctx, champion, lane):
    if getCorrectLane(lane) != False:
        lane = getCorrectLane(lane)
    else: 
        await ctx.channel.send("try again but don't type it weirdly")
    await ctx.channel.send("```" + luke_methods.get_skills(champion, lane) + "```")

@client.command()
async def getinfo(ctx, summoner_name):
    channel = ctx.channel
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
    
    await channel.send(rank + "\n" + "------------" + "\n")
    await channel.send("```" + str(table) + "```")

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
    count = 0                             
    # this stuff has to happen because 2000 limit per message in discord                  
    for i in range(roundDownLength):
        top.add_row([numArray[i], champArray[i], winRateArray[i], pickRateArray[i]])
        count+=1

    # submit as code block because of spacing restrictions
    await channel.send('```' + str(top) + '```')            

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
    
    await channel.send('```' + fullTrees + '```')

@client.command()
async def get_counters(ctx, champion):
    await ctx.channel.send("```" + counters.best_pick(champion) + "```") 
    await ctx.channel.send("```" + counters.worst_picks(champion) + "```") 
    await ctx.channel.send("```" + counters.best_lane_picks(champion) + "```")
    

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

@client.command()
async def ball(ctx, question):
    responses = ['You should ask Tahseen',
                'You can count on it',
                'oh god no',
                'yea',
                'that\'s a dumb question',
                'Try again later',
                'My guts say no',
                'lol you\'re on your own bud',
                'YEAH DEFINITELY',
                'WHY WOULD YOU EVEN ASK THIS?',
                'Maybe you should ask again; I couldn\'t hear you over the sound of Rikesh',
                'no',
                'ya',
                'Hard no from me',
                'you wish',
                'you\'re not only wrong, you\'re stupid',
                'HELL YEAH BROTHER',
                'not quite',
                'obviously not']
    rikesh_responses = ['how are you this dumb?',
                        'please just shut up',
                        'ur mom',
                        'i don\'t like your tone']
    if (ctx.message.author == "RikeshPatel"):
        random_response_index = randint(0, len(rikesh_responses) - 1)
        await ctx.channel.send(rikesh_responses[random_response_index])
    else:
        random_response_index = randint(0, len(responses) - 1)
        await ctx.channel.send(responses[random_response_index])


@client.command()
async def rand_usr(ctx, member: discord.Member):
    username = dict_scrape.get_word()
    await member.edit(nick=username)
    await ctx.channel.send('Nickname was changed to ' + username)
    # replace spaces in URL with the appropriate characters
    if " " in username:
        space_index = username.index(" ")
        temp = list(username)
        temp[space_index] = "%20"
        username = "".join(temp)
    await ctx.channel.send("```" + dict_scrape.get_definition(username) + "```")

@client.command()
async def get_def(ctx, word):
    if " " in word:
        space_index = word.index(" ")
        temp = list(word)
        temp[space_index] = "%20"
        word = "".join(temp)
    await ctx.channel.send(dict_scrape.get_definition(word))

@client.command()
async def rand_urban_def(ctx):
    await ctx.channel.send(urban_dic.get_rand_urban())

@client.command()
async def urb_usr(ctx, member: discord.Member):
    definition = urban_dic.get_rand_urban()
    username = definition.split("\n")[0]
    await member.edit(nick=username)
    await ctx.channel.send('Nickname was changed to ' + username)
    await ctx.channel.send(definition)

@client.command()
async def help(ctx):
    await ctx.channel.send('getinfo - usage: `?getinfo <summoner_name>` - (make sure to use underscores) it retrieves some info on that summoner \n' \
                           'tier - usage: `?tier <lane>` - retrieves tier list for that lane \n' \
                           'runes - usage: `?runes <champion> <lane>` - retrieves rune for that role and champ \n' \
                           'spam - usage: `?spam <user>` - spams a user in the discord \n' \
                           'flip - usage: `?flip` - flips a coin \n' \
                           'ball - usage: `?ball <question>` - asks the 8ball \n' \
                           'rand_usr - usage: `?rand_usr <user>` - it will change their nickname to a random word \n' \
                           'get_def - usage: `?get_def <word>` - it will return a definition from wordnik.com \n' \
                           'rand_urban_def - usage: `?rand_urban_def` - grab a random definition from urban dictionary \n' \
                           'urb_usr - usage: `?urb_usr <user>` - change a nickname to a random urban dictionary word and then will display the definition \n' \
                           'build - usage: `?build <champion> <lane>` - retrieve the build for a champion (first three main items) \n' \
                           'skills - usage: `?skills <champion> <lane>` - retrieve the skill max order for a champion \n' \
                           'get_counters - usage: ?get_counters <champion> - get the best picks, worst picks, and best lane picks for a champion')

@client.event
async def on_ready():
    print('bot is online')


client.run(os.environ.get('MY_TOKEN'))