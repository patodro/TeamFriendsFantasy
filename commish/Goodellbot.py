import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

commishChannelID = 1256234378443362376
generalChannelID = 1237187300547367036
infoChannelID = 1256224215011557448

cnlCommish = client.get_channel(commishChannelID)

web = "https://patodro.github.io/TeamFriendsFantasy"

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    print('------')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    if message.content.startswith('$Roger'):
        await send_CommishMsg("I'm the captain now")
        
#send <message> to the defined <channel>
async def send_CommishMsg(message):
    await cnlCommish.send(message)

#make Roger pimp the website
async def send_CommishWebsite():
    await cnlCommit.send(web)

tokFile = open("token.txt", "r")
token = tokFile.readline()
client.run(token)