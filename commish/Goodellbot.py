import discord
from discord.ext import commands
import requests
import random
import os

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

data_dir = Path(__file__).parent.parent / "dataStore"

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
        embed = discord.Embed(color=discord.Color.purple())
        embed.set_image(url=goodellGIF)
        await message.channel.send(embed=embed)
        
#send <message> to the defined <channel>
async def send_CommishMsg(message):
    await cnlCommish.send(message)

#make Roger pimp the website
async def send_CommishWebsite():
    await cnlCommit.send(web)
    
#make some noise for the hi score of the week
#async def hiScore():
	#something here
	
#update nicknames based on dataStore info
@client.command(pass_context=True)
async def chnick(ctx, member: discord.Member, nick):
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


client.run(discordToken)