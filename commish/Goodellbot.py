import discord
from discord.ext import commands
import requests
import random

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

commishChannelID = 1256234378443362376
generalChannelID = 1237187300547367036
infoChannelID = 1256224215011557448

cnlCommish = client.get_channel(commishChannelID)

web = "https://patodro.github.io/TeamFriendsFantasy"

#---------API KEYS----------------------------------
tokFile = open("discordToken.txt", "r")
discordToken = tokFile.readline()
tenorFile = open("tenor.txt", "r")
tenorKey = tenorFile.readline()
tokFile.close()
tenorFile.close()
#---------------------------------------------------

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    print('------')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    if message.content.startswith('$Roger'):
    		goodellGIF = tenorGIF("goodell")
    		embed = discord.Embed(title="Goodell",color=discord.Color.purple())	###does this need to be client.Embed?
    		embed.set_image(url=goodellGIF)
        
#send <message> to the defined <channel>
async def send_CommishMsg(message):
    await cnlCommish.send(message)

#make Roger pimp the website
async def send_CommishWebsite():
    await cnlCommit.send(web)
    
#make some noise for the hi score of the week
#async def hiScore():
	#something here

def tenorGIF(search_term):
	lmt = 12
	
	r = requests.get("https://tenor.googleapis.com/v2/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))
	results = []
	
	if r.status.code == 200:
		gifs = r.json()
		
		for i in range(lmt):
			gif_format = gifs["results"][random.randint(1,(lmt-1))]["media_formats"]["gif"]
			
			if gif_format["dims"][0] >= gif_format["dims"][1]:
				url = gif_format["url"]
				dims = gif_format["dims"]
				
				results.append(url)
				
		if len(results) > 0:
			gif = random.choice(results)
			print(f"Here are the results for {search_term} ({lmt} url limit) (gif horizontal or square embed discord format): ")
			print(f"Printing 1 random result of {len(results)}")
			print(gif)
		else:
			print(f"ERROR: There are no results for {search_term}.")
	else:
		gifs = None
		print("ERROR: Something failed during the TENOR API request")			
	return gif

client.run(token)