import discord
from discord.ext import commands

client = discord.Client()

@client.event
async def on_ready():
    print('bot is ready')

@client.event
async def on_message(message):
    if message.content.startswith('hajime'):
        await message.channel.send('hello ' + message.author.name)


client.run("Njc5MjEzNTg4NDI1OTk4MzM3.Xkvz3g.kOWAVZMkKo73ZIMf4c2pybfZgRk")

