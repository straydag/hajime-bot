#!/usr/bin/env python3
import json
import discord
from requests_oauthlib import OAuth1Session
from discord.ext import commands


#grabs token from config file
with open('config.json') as config_file:
    data = json.load(config_file)
    discord_token = data["discord_token"]
    trello_token = data["trello_token"] 

#creates client object
client = discord.Client()

#on ready
@client.event
async def on_ready():
    print('Bot is ready.')

#whenever a user sends a message
@client.event
async def on_message(message):
    if message.content.startswith('hajime'):
        if "help" in message.content:
            await message.channel.send('no')
        elif "hello" in message.content:
            await message.channel.send('hi' + message.author)
        elif "login" in message.content:
            oauth = OAuth1Session(trello_token, client_secret="???")
            await message.channel.send('okay, i dm-ed you sign in info')

client.run(discord_token)



