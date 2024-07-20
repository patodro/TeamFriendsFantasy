import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

commishChannelID = 1256234378443362376
generalChannelID = 1237187300547367036
infoChannelID = 1256224215011557448

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    print('------')
    for server in client.guilds:
        for channel in server.channels:
            print(f'{channel.type} | {channel} | {channel.id}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
        
        
tokFile = open("token.txt", "r")
token = tokFile.readline()
client.run(token)