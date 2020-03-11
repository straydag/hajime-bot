# hajime-bot
A discord bot to assist with organizational needs

## how to use
guide to getting the bot to work

### 1.) Tokens
You will need 2 tokens to activate the discord bot. if you are assisting in the development of this bot you can just ask the account holder for the tokens and skip this section, otherwise you'll have to follow this section to obtain the tokens.

##### Discord Token
Go to the discord bot's bot panel on discord and click "reveal token" and copy that

##### Trello Token
Go to https://trello.com/app-key/ and grab the first key. You'll need to be signed in to trello, Trello reccomends making a second trello account for developing applications that use their API

### 2.) Configuration
Once you've acquired the tokens, you'll need to put them inside the config.json file as well as the path to the user database. The problem with this is that if you push to github it will push the tokens as well which isn't good for security, you can delete them from config.json before pushing but if you're pushing multiple changes then you'd have to take them out each time and put the back in when you want to make changes and test. it's best to tell github to not track the config.json file. You can do that by using the following git commands:

`git update-index --assume-unchanged config.json` Tells git to not track config.json

`git update-index --no-assume-unchanged config.json` Tells git to track config.json

### 3.) Requirements
Lastly you need to install the required modules/libraries, you can use this pip3 command: `pip3 install -r requirements.txt` It will recursivley install everything in the requirements.txt file

### 4.) Done
That's about it, now you can run main.py and it should work
