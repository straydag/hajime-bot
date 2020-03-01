#!/usr/bin/env python3
import json
import discord
from discord.ext import commands

#grabs token from config file
with open('config.json') as config_file:
    token = json.load(config_file)["token"]

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
        await message.channel.send('hello there ' + message.author.name)

client.run(token)
