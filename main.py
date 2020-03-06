#!/usr/bin/env python3
import json
import asyncio
import discord
import requests
import aiohttp
from requests_oauthlib import OAuth1Session
from discord.ext import commands


#grabs tokens from config file
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

        #sends user commands
        if "help" in message.content:
            await message.channel.send('no')

        #bot will reply with hi [username]
        elif "hello" in message.content:
            await message.channel.send('hi ' + message.author.name)

        #used to login to trello
        elif "login" in message.content:  

            #send user a link to trello popup and asks the user to input authorization code
            await message.channel.send('okay, i dm-ed you the sign in info')
            await message.author.send('here you go: ' + 'https://trello.com/1/authorize?expiration=never&name=Hajime&scope=read,write&response_type=token&key=' + trello_token)
            await message.author.send('please enter the authorization code in your next message to complete sign in (will timeout in 2 minutes): ') 
           
            #this function makes sure the reply is only acknowledged by the bot if in private message with the same user that sent the message
            def check(reply_message): 
                return reply_message.author == message.author and reply_message.channel == message.channel
            
            #try block used for timeout exception
            try:
                #waits for the user to input the authorization code and uses check function
                reply = await client.wait_for('message', timeout=120.0, check=check) 
       
                #this code block fetches from trello userinfo endpoint and lets the user know if it was successfull
                async with aiohttp.ClientSession() as session:

                    #uses token key from config file and user token from reply var in request to trello's userinfo endpoint and stores response in data var
                    raw_response = await session.get("https://api.trello.com/1/members/me/?key=" + trello_token + "&token=" + reply.content)
                    #reads data var's body using text() function and stores returned str in response var
                    response = await raw_response.text()
                   
                    #if response valid, extracts user's name from response json data and sends welcome message with name, else sends user failure message
                    if response != 'invalid token':
                        response = json.loads(response)
                        await message.author.send('welcome ' + response.get("fullName"))  

                    else:
                        await message.author.send('error logging in')

            except asyncio.TimeoutError:
                await message.author.send('timed out')


client.run(discord_token)



