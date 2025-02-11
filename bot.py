import discord, asyncio
from discord.ext import commands
import requests
import math
import random
import dict_scrape
import urban_dic
import luke_methods
import counters
import config
import imgur
import stats
import os
import strikes
from datetime import datetime
from bs4 import BeautifulSoup
from random import randint
from discord.ext import commands, tasks
from discord import User
from asyncio import sleep
from urllib import request, response, error, parse
from urllib.request import urlopen, Request
from prettytable import PrettyTable

client = commands.Bot(command_prefix='?')

# for the initial help command it provides
client.remove_command("help")                   

hq_channel = 412851300255006730
dad_bot_ID = 503720029456695306

@client.command()
async def counter(ctx, champion):
    await ctx.channel.send("```" + counters.best_pick(champion) + "```") 
    await ctx.channel.send("```" + counters.worst_picks(champion) + "```") 
    await ctx.channel.send("```" + counters.best_lane_picks(champion) + "```")


# imgur

@client.command()
async def imgur_search(ctx, query):
    await ctx.channel.send(imgur.imgur_search(query))

# non application commands below

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
                        'i don\'t like your tone',
                        'PLEASE PLEASE PLEASE shut up',
                        "leave the server"]
    if (ctx.message.author.name == "RikeshPatel"):
        random_response_index = randint(0, len(rikesh_responses) - 1)
        await ctx.channel.send(rikesh_responses[random_response_index])
    else:
        random_response_index = randint(0, len(responses) - 1)
        await ctx.channel.send(responses[random_response_index])

# dictionary username changes

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

# end dict methods

@client.command()
async def rand_num(ctx, min, max):
    if min.isnumeric() and max.isnumeric():
        min = int(min)
        max = int(max)
        if min > max:
            min, max = max, min
        result = randint(min, max)
        await ctx.channel.send(str(result))
    else:
        await ctx.channel.send("please enter numbers")

@client.command()
async def me_delete(ctx, num_of_messages):
    count = 0
    messages = await ctx.channel.history(limit=200).flatten()
    for msg in messages:
        if msg.author == ctx.message.author:
            await msg.delete()
            count += 1
        if count == int(num_of_messages) + 1:
            break

@client.command()
async def mass_delete(ctx, num_of_messages):
    count = 0
    messages = await ctx.channel.history(limit=200).flatten()
    for msg in messages:
        await msg.delete()
        count += 1
        if count == int(num_of_messages) + 1:
            break

@client.command()
async def help(ctx):
    await ctx.channel.send('**LEAGUE RELATED (mainly deprecated im sorry)** \n' \
                           '`?counter <champion>` - get the best picks, worst picks, and best lane picks for a champion \n' \
                           '**DEFINITIONS** \n' \
                           '`?rand_usr <user>` - it will change their nickname to a random word \n' \
                           '`?get_def <word>` - it will return a definition from wordnik.com \n' \
                           '`?rand_urban_def` - grab a random definition from urban dictionary \n' \
                           '`?urb_usr <user>` - change a nickname to a random urban dictionary word and then will display the definition \n\n' \
                           '**MISC** \n' \
                           '`?mass_delete <number>` - deletes all messages up to your number \n' 
                           '`?me_delete <number>` - deletes your past messages to a certain number of them \n' \
                           '`?rand_num <min> <max>` - picks a random number between two arguments \n' \
                           '`?spam <user>` - spams a user in the discord \n' \
                           '`?imgur_search <query>` - searches a query on imgur.com \n' \
                           '`?strike <user>` - adds a strike to a discord user\n' \
                           '`?rm_strike <user>` - removes a strike from a discord user on the board\n' \
                           '`?view_strike` - views the current strikes in a bar graph' \
                           '`?ball <question>` - asks the 8ball')

@client.event
async def on_ready():
    print('bot is online')
    
@client.command()
async def strike(ctx, member: discord.Member):
    strikes.add_strike(member.name)
    strikes.show_strike_graph()
    await ctx.channel.send(file=discord.File('./images/strikegraph.png'))
    os.remove("./images/strikegraph.png")
        
@client.command()
async def rm_strike(ctx, member: discord.Member):
    strikes.remove_strike(member.name)
    strikes.show_strike_graph()
    await ctx.channel.send(file=discord.File('./images/strikegraph.png'))
    os.remove("./images/strikegraph.png")

@client.command()
async def view_strike(ctx):
    strikes.show_strike_graph()
    await ctx.channel.send(file=discord.File('./images/strikegraph.png'))
    os.remove("./images/strikegraph.png")   
        
# specifically made to combat dad bot
@client.event
async def on_message(message):
    if message.author.id == dad_bot_ID:
        bot_message = await message.channel.send("shut up dad")
        await message.delete(delay=2)
        await bot_message.delete(delay=2)
    await client.process_commands(message)
    
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.channel.send("That command wasn't found! Sorry :(")
    elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
        await ctx.channel.send("That member wasn't found! Sorry :(")

# for routine posture checks
@tasks.loop(hours=6)
async def scheduled():
    message_channel = client.get_channel(hq_channel)
    print(f"Got channel {message_channel}")
    await message_channel.send("POSTURE CHECK")

@scheduled.before_loop
async def before():
    await client.wait_until_ready()
    print("Finished waiting")

scheduled.start()

client.run(config.MY_TOKEN)