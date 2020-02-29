import json
import discord
from discord.ext import commands

#grabs token from config file
with open('config.json') as config_file:
    token = json.load(config_file)["token"]


client = discord.Client()

@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_message(message):
    if message.content.startswith('hajime'):
        await message.channel.send('hello ' + message.author.name)

client.run(token)
