import discord
#import json
import sys

#Init client
client = discord.Client()
#Joking name for tracker on # of messages with E
# try:
#     file = open("book_of_sin.json", "r")
#     all_sins = json.load(file)
#     file.close()
# except:
all_sins = {}
try:
    file = open("client.secret", "r")
    secret = file.read().strip()
except:
    print("Could not find client secret!")
    sys.exit(1)


#TODO: Ensure persistency while also maintaining clean async code!

#Yes I am like this and no I'm not sorry
@client.event
async def on_ready():
    print("Hewwo wowd! I am {}".format(client.user))

@client.event
async def on_message(message):
    #Prevent feedback loop and being obnoxious elsewhere
    if message.author == client.user or str(message.channel) != "no-letter-e":
        return
    #Custom emoji by server- hardcoding because not intending to scale
    #This is using custom emoji id- obtain this by escaping custom emoji!!
    if message.guild.id == 403050820268064788:
        emoji = client.get_emoji(736461993850044438)
    else:
        emoji = client.get_emoji(736223799455776879)
    #get_emoji fails silently so check if none-type or not
    if not emoji:
        emoji = "🇪"

    #Ensure values are init'ed- DRY!
    try:
        sins = all_sins[message.guild.id]
    except KeyError:
        all_sins[message.guild.id] = {}
    try:
        sin_count = all_sins[message.guild.id][message.author.id]
    except KeyError:
        all_sins[message.guild.id][message.author.id] = 0
        sin_count = 0

    #User can check own sins
    if message.content == "~sins":  
        await message.channel.send("Sins of {}: {}".format(message.author.display_name, sin_count))
    
    #Check 10 worse sinners
    elif message.content == "~sinners":
        #weird sorting magic
        sin_list = sorted(all_sins[message.guild.id].items(), key=lambda x: x[1])
        #Prevent printing rankings lower than #10
        low_rank = 10
        if len(sin_list) < 10:
            low_rank = len(sin_list)
        #Iterate through ranks, store top sinners in string
        sin_msg = ""
        for num in range(0,low_rank):
            name = client.get_user(sin_list[num][0])
            sin_count = sin_list[num][1]
            sin_msg += "#{}: {} - {} sin(s)".format(num + 1, name, sin_count)
        #Send it!
        await message.channel.send(sin_msg)
    
    #React to e messages
    elif "e" in message.content or "E" in message.content:
        await message.add_reaction(emoji)
        all_sins[message.guild.id][message.author.id] = sin_count + 1

# async def file_write(sins):
#     try:
#         file = open("book_of_sin.json", "w")
#         file.write(sins.dump())
#         file.flush()
#     except:
#         print("Error: can't dump data")

client.run(secret)