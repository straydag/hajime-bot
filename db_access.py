import aiosqlite
import asyncio

class db_access:
   
    def __init__(self, path_to_db):
        self.path_to_db = path_to_db

    async def is_logged_in(self: str, discord_id: str) -> bool:
        '''
            is_logged_in(trello_id <STR>)

            checks to see if user passed in as argument is logged in
            returns: True if yes and False if no

        '''

        conn = await aiosqlite.connect(self.path_to_db)
        curs = await conn.cursor()

        await curs.execute("SELECT * FROM users WHERE discord_id=?", (discord_id, ))
        user_info = await curs.fetchall()

        return (user_info != [] and user_info[0][2] != 0)
        
    async def add_user(self, discord_id: str, trello_id: str):
        '''
            add_user(discord_id <STR>, trello_id <STR>)
           
            adds a user into the database
        ''' 

        conn = await aiosqlite.connect(self.path_to_db)                                                     
        curs = await conn.cursor()
    
        await curs.execute("CREATE TABLE IF NOT EXISTS users (discord_id TEXT, trello_id TEXT, is_logged_in INTEGER)")
        await curs.execute("INSERT INTO users VALUES (?, ?, ?)", (discord_id, trello_id, 1))
        await conn.commit()  
        await conn.close()
        
        return

    async def get_user_info(self, discord_id: str) -> dict:
        '''
            get_user(discord_id <STR>)
            
            queries the database for the user matching the discord_id and returns all their data in the form of a dictionary 
            returns: dictionary
        '''

        conn = await aiosqlite.connect(self.path_to_db)
        curs = await conn.cursor()
    
        await curs.execute("SELECT * FROM users WHERE discord_id = ?", (discord_id, ))
        user_data = await curs.fetchall()
        await conn.close()  
    
        return {"discord_id": user_data[0][0], "trello_id": user_data[0][1], "is_logged_in": user_data[0][2]}

