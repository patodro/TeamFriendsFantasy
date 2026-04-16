import discord
from discord.ext import tasks, commands
import requests
import random
import os
from pathlib import Path
import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

commishChannelID = 1256234378443362376
generalChannelID = 1237187300547367036
testChannelID = 1265092780393238749
infoChannelID = 1256224215011557448
guildID = 1237187300547367033

web = "https://patodro.github.io/TeamFriendsFantasy"

script_dir = Path(__file__).resolve().parent
tokenPath = script_dir / "discordToken.txt"
tenorPath = script_dir / "tenor.txt"
#---------API KEYS----------------------------------
tokFile = open(tokenPath, "r")
discordToken = tokFile.readline()
tenorFile = open(tenorPath, "r")
tenorKey = tenorFile.readline()
tokFile.close()
tenorFile.close()
#---------------------------------------------------

data_dir = Path(__file__).parent.parent / "dataStore"
time = datetime.time(hour=12)

# Global client instance for external access
client = None

memberDict = {
    'dave':'dc1133._10969',
    'stephen':'hashedfuzzy',
    'tony':'tcarbone31_24880',
    'sean':'sean1928',
    'katie':'karmy0804',
    'josh':'joshwsutton',
    'z':'zman9074',
    'bobby':'bobbygiambra',
    'mike':'obiwan088',
    'andy':'hopscotch33',
    'pat':'patodro',
    'lepo':'johnlepo_06200'
}


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # an attribute we can access from our task
        self.counter = 0
    
    async def setup_hook(self) -> None:
        #start tasks in background
        print('background')
        self.readTeams.start()

    async def on_ready(self):
        print(f'We have logged in as {self.user}')
        print('------')
    
    async def on_message(self, message):
        if message.author == self.user:
            return
            
        if message.content.startswith('$Roger'):
            goodellGIF = tenorGIF("goodell")
            embed = discord.Embed(color=discord.Color.purple())
            embed.set_image(url=goodellGIF)
            await message.channel.send(embed=embed)
            
        if (message.content.startswith('%repeat') and message.channel.name == 'test'):
            await self.send_CommishMsg(message.content.replace('%repeat',""))
        
    #send <message> to the defined <channel>
    async def send_CommishMsg(self, message):
        cnlCommish = self.get_channel(commishChannelID)
        await cnlCommish.send(message)

    #make Roger pimp the website
    async def send_CommishWebsite(self):
        cnlCommish = self.get_channel(commishChannelID)
        await cnlCommish.send(web)
        
    #send hi score message to commish channel
    async def send_HiScore(self, message):
        cnlGeneral = self.get_channel(testChannelID)
        embed = discord.Embed(title="Weekly High Score", description=message, color=discord.Color.gold())
        await cnlGeneral.send(embed=embed)
        
    @tasks.loop(time=time)
    async def readTeams(self):
        print('Checking for updated teamnames....')
        for file in os.listdir(data_dir):
            if file.endswith(".name"):
                with open(os.path.join(data_dir, file), 'r+') as tf:
                    newName = tf.readline()
                owner = Path(os.path.join(data_dir, file)).stem
                os.remove(os.path.join(data_dir, file))
                await self.chnick(owner, newName)    
        
    #update nicknames based on dataStore info
    async def chnick(self, owner, newNick):
        member = self.guilds[0].get_member_named(memberDict[owner])
        print(f'{member.name} changed their teamname')
        await member.edit(nick=newNick)
        

def tenorGIF(search_term):
	lmt = 12
	
	r = requests.get("https://tenor.googleapis.com/v2/search?q=%s&key=%s&limit=%s" % (search_term, tenorKey, lmt))
	results = []
	
	if r.status_code == 200:
		gifs = r.json()
		
		for i in range(lmt):
			gif_format = gifs["results"][random.randint(1,(lmt-1))]["media_formats"]["gif"]
			
			if gif_format["dims"][0] >= gif_format["dims"][1]:
				url = gif_format["url"]
				dims = gif_format["dims"]
				
				results.append(url)
				
		if len(results) > 0:
			gif = random.choice(results)
			print(f"Printing 1 random result of {len(results)}")
			print(gif)
		else:
			print(f"ERROR: There are no results for {search_term}.")
	else:
		gifs = None
		print("ERROR: Something failed during the TENOR API request")			
	return gif

            
client = MyClient(intents=intents)


# ---- External API Functions ----
# These functions can be imported and called from other Python files

async def send_hiscore_message(message):
    """Send a formatted hi-score message to the commish channel"""
    if client.is_ready():
        await client.send_HiScore(message)
    else:
        print("ERROR: Bot is not ready. Cannot send message.")


async def send_commish_message(message):
    """Send a plain message to the commish channel"""
    if client.is_ready():
        await client.send_CommishMsg(message)
    else:
        print("ERROR: Bot is not ready. Cannot send message.")


def get_bot_client():
    """Return the bot client instance for direct access if needed"""
    return client


if __name__ == "__main__":
    client.run(discordToken)