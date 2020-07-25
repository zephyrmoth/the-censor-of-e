import discord
import json
import sys
import time

#Init client
client = discord.Client()

#TODO: Add logging instead of system output.

#Joking name for tracker on # of messages with E- import as JSON
try:
    file = open("book_of_sin.json", "r")
    all_sins = json.load(file)
    print(all_sins)
    file.close()
except:
    all_sins = {}

#Read client secret from client.secret
try:
    file = open("client.secret", "r")
    secret = file.read().strip()
except:
    print("Could not find client secret!")
    sys.exit(1)

#Time value for last file write and boot time
last_backup_time = time.time()
boot_time = time.time()

#Yes I am like this and no I'm not sorry
@client.event
async def on_ready():
    print("Hewwo wowd! I am {}".format(client.user))

@client.event
async def on_message(message):
    global all_sins
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

    #Python's JSON lib converts ints to strings...
    guild_key = str(message.guild.id)
    author_key = str(message.author.id)
        
    #Ensure values are init'ed- DRY!
    #try:
    sins = all_sins[guild_key]
    # except KeyError:
    #     all_sins[message.guild.id] = {}
    # try:
    sin_count = int(all_sins[guild_key][author_key])
    # except KeyError:
    #     all_sins[message.guild.id][message.author.id] = 0
    #     sin_count = 0

    #Python doesn't have a switch/case unfortunately...
    #User can check own sins
    if message.content == "~sins":  
        await message.channel.send("Sins of {}: {}".format(message.author.display_name, sin_count))
        return
    #Check 10 worse sinners
    elif message.content == "~sinners":
        #weird sorting magic
        sin_list = sorted(all_sins[guild_key].items(), key=lambda x: x[1])
        #Prevent printing rankings lower than #10
        low_rank = 10
        if len(sin_list) < 10:
            low_rank = len(sin_list)
        #Iterate through ranks, store top sinners in string
        sin_msg = ""
        for num in range(0,low_rank):
            name = client.get_user(int(sin_list[num][0]))
            sin_count = sin_list[num][1]
            sin_msg += "#{}: {} - {} sin(s)\n".format(num + 1, name, sin_count)
        #Send it!
        await message.channel.send(sin_msg)
        return
    #Brief status message, mostly for my own sake
    elif message.content == "~status":
        uptime = time.time() - boot_time
        await message.channel.send("Uptime: {}\nLast Backup: {}".format(uptime, last_backup_time))
        return
    #React to e messages
    elif "e" in message.content or "E" in message.content:
        await message.add_reaction(emoji)
        #Gotta love weird typing
        all_sins[guild_key][author_key] = str(sin_count + 1)
        #Python async does not multithread so this *shouldn't* cause race conditions
        client.loop.create_task(file_write())
    return

async def file_write():
    #Only backup approx every hour
    #TODO: actually change from the test value
    global last_backup_time
    if (time.time() - last_backup_time) < 3600:
        return
    try:
        file = open("book_of_sin.json", "w")
        json.dump(all_sins, file)
        file.flush()
        last_backup_time = time.time()
    except:
        #Catch 
        print("Error: can't dump data!")

client.run(secret)