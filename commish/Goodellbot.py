import discord
from discord.ext import tasks, commands
import requests
import random
import os
from pathlib import Path
import datetime

intents = discord.Intents.default()
intents.message_content = True

commishChannelID = 1256234378443362376
generalChannelID = 1237187300547367036
infoChannelID = 1256224215011557448
guildID = 1237187300547367033

web = "https://patodro.github.io/TeamFriendsFantasy"

#---------API KEYS----------------------------------
tokFile = open("discordToken.txt", "r")
discordToken = tokFile.readline()
tenorFile = open("tenor.txt", "r")
tenorKey = tenorFile.readline()
tokFile.close()
tenorFile.close()
#---------------------------------------------------

data_dir = Path(__file__).parent.parent / "dataStore"
time = datetime.time(hour=12)

memberDict = {
    'dave' = ''
}


class MyClient(discord.Client):
    async def setup_hook(self) -> None:
        #start tasks in background
        print('background')
#        self.readTeams.start()
        #self.readTeams()

    async def on_ready(self):
        print(f'We have logged in as {self.user}')
        print('------')
        self.readTeams()
    
    async def on_message(self, message):
        if message.author == self.user:
            return
            
        if message.content.startswith('$Roger'):
            goodellGIF = tenorGIF("goodell")
            embed = discord.Embed(color=discord.Color.purple())
            embed.set_image(url=goodellGIF)
            await message.channel.send(embed=embed)
            
        if message.content.startswith('guild'):
            await message.channel.send(message.guild.id)
        
    #send <message> to the defined <channel>
    async def send_CommishMsg(self, message):
        cnlCommish = client.get_channel(commishChannelID)
        await cnlCommish.send(message)

    #make Roger pimp the website
    async def send_CommishWebsite():
        cnlCommish = client.get_channel(commishChannelID)
        await cnlCommish.send(web)
        
    #make some noise for the hi score of the week
    #async def hiScore():
        #something here
        
    #@tasks.loop(seconds=7.0)
    def readTeams(self):
        print('Checking for updated teamnames....')
        for file in os.listdir(data_dir):
            if file.endswith(".name"):
                with open(os.path.join(data_dir, file), 'r+') as tf:
                    newName = tf.readline()
                oldName = Path(os.path.join(data_dir, file)).stem
                os.remove(os.path.join(data_dir, file))
                self.chnick(oldName, newName)    
        
    #update nicknames based on dataStore info
    async def chnick(self, oldNick, newNick):
        self.get_all_members()
        await member.edit(nick=nick)
        await ctx.send(f'{member.mention} changed their teamname')

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
client.run(discordToken)