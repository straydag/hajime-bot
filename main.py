'''
NOTE: Before commit: change version number.
Version: 0.0.2

'''
#!/usr/bin/env python3
import json
import asyncio
import sqlite3
import discord
import requests
import aiohttp
import aiosqlite
import os.path
from requests_oauthlib import OAuth1Session
from discord.ext import commands

#grabs tokens from config file
with open('config.json') as config_file:
    data = json.load(config_file)
    discord_token = data["discord_token"]
    trello_token = data["trello_token"] 
    path_to_db = data["path_to_db"]

#creates client object
client = discord.Client()

#on ready
@client.event()
async def on_ready():
    print('Bot is ready')

#whenever a user sends a message
@client.event()
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
                        
                        #adds the user's discord username to the database along with their trello id
                        conn = await aiosqlite.connect(path_to_db)                                                     
                        curs = await conn.cursor()
                        await curs.execute("CREATE TABLE IF NOT EXISTS users (discord_id TEXT, trello_id TEXT, is_logged_in INTEGER)")
                        await curs.execute("INSERT INTO users VALUES (?, ?, ?)", (message.author.id, reply.content, 1))
                        await conn.commit() 
                        await conn.close()
                        
                        #puts the json response into a response variable and send a message to the user welcoming them
                        response = json.loads(response)
                        await message.author.send('welcome ' + response.get("fullName"))  

                    else:
                        await message.author.send('error logging in')

            except asyncio.TimeoutError:
                await message.author.send('timed out, please try again')

            # checks for command
        elif message.content.startswith('hajime') and "to do" in message.content:
            # connects to db
            db = await aiosqlite.connect(...)
            # checks to find user
            cursor = await db.execute('SELECT trello_id FROM users where discord_id=?', (message.author,))
            member_trello_id = await cursor.fetchone()
            await cursor.close()
            await db.close()
            # uses token to get into trello
            querystring = {"filter": "visible", "key": trello_token, "token": member_trello_id}
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.trello.com/1/members/" + member_trello_id + "/cards", params=querystring) as resp:
                    # sends status and message
                    await message.send(resp.status)
                    await message.send(await resp.text())


'''
RUN
'''
client.run(discord_token)

