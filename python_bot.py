from discord import Client #you'll need this install
import discord
import random
import time
import subprocess #You'll need to install this and also download espeak and put in the same directory as this source code.
import threading
import os
import urllib.request
import json
from pathlib import Path
from datetime import datetime
from datetime import datetime,timedelta
import datetime
import csv
from collections import OrderedDict
from discord.utils import get
from dateutil.relativedelta import relativedelta
import calendar
from threading import Timer
from pyshorteners import Shortener
import config #Store bot token and giphy api key here
#test comment 2
global player
global voice_client
global voice_channel
global old_voice_members
global timecard_hour
global lunch_hour
global lunch_minute
global foos_time
global mess_with_kevin
global thirtyMinWarning
discordApiKey = config.bot_token #from config.py file
giphyApiKey = config.giphy_api_key #from config.py file

client = Client()

def member_change():
  global old_voice_members
  global player
  if not os.path.exists("VoiceFiles"):
    os.makedirs("VoiceFiles")
  if( not (Path("VoiceFiles/joined.wav").is_file())):
    textToWav("Has joined the channel", "VoiceFiles/joined.wav")
  if( not (Path("VoiceFiles/left.wav").is_file())):
    textToWav("Has left the channel", "VoiceFiles/left.wav")
  if( not (Path("VoiceFiles/init.wav").is_file())):
    textToWav("init", "VoiceFiles/init.wav")
  if not (len(old_voice_members) == len(voice_channel.voice_members)):
    print("member change")
    if(len(old_voice_members) > len(voice_channel.voice_members)):
      print("Someone Left") #Someone left
      for i in range(0, len(old_voice_members)):
        if old_voice_members[i] not in voice_channel.voice_members:
          name = old_voice_members[i].display_name
          old_voice_members = []
          for k in range(0, len(voice_channel.voice_members)):
            old_voice_members.append(voice_channel.voice_members[k])
          if(name.startswith('(')):
            parindex = name.find(')')
            name = name[parindex+1:]
          file_name = "VoiceFiles/"+name+".wav"
          if Path(file_name).is_file():
            player = voice_client.create_ffmpeg_player(file_name)
            player.volume= 100/100 #Change the left number to adjust over all volume
            player.start()
            while(not player.is_done()):
              count = 0
            player = voice_client.create_ffmpeg_player("VoiceFiles/left.wav")
            player.volume= 100/100
            player.start()
            while(not player.is_done()):
              waitCount = 0
          else:
            textToWav(name,file_name)
            player = voice_client.create_ffmpeg_player("VoiceFiles/"+name+".wav")
            player.volume= 100/100
            player.start()
            while(not player.is_done()):
              waitCount = 0
            player = voice_client.create_ffmpeg_player("VoiceFiles/left.wav")
            player.volume= 100/100
            player.start()
            while(not player.is_done()):
              waitCount = 0
          break
    elif(len(voice_channel.voice_members) > len(old_voice_members)):
      print("Someone joined")
      for i in range(0, len(voice_channel.voice_members)):
        if voice_channel.voice_members[i] not in old_voice_members:
          name = voice_channel.voice_members[i].display_name
          old_voice_members = []
          for k in range(0, len(voice_channel.voice_members)):
            old_voice_members.append(voice_channel.voice_members[k])
          if(name.startswith('(')):
            parindex = name.find(')')
            name = name[parindex+1:]
          file_name = "VoiceFiles/"+name+".wav"
          if Path(file_name).is_file():
            player = voice_client.create_ffmpeg_player(file_name)
            player.volume= 100/100
            player.start()
            while(not player.is_done()):
              waitCount = 0
            player = voice_client.create_ffmpeg_player("VoiceFiles/joined.wav")
            player.volume= 100/100
            player.start()
            while(not player.is_done()):
              waitCount = 0
          else:
            textToWav(name,file_name)
            player = voice_client.create_ffmpeg_player("VoiceFiles/"+name+".wav")
            player.volume= 100/100
            player.start()
            while(not player.is_done()):
              waitCount = 0
            player = voice_client.create_ffmpeg_player("VoiceFiles/joined.wav")
            player.volume= 100/100
            player.start()
            while(not player.is_done()):
              waitCount = 0
          break
  threading.Timer(.5, member_change).start()


def textToWav(text, file_name):
  subprocess.call(["espeak", "-vf2", "-w"+file_name, text]) #Change (or remove) "f2" to a voice file in ~/espeak/espeak-data/voice to change the voice
  print("File written")

async def giphy_command(messageContent, author, message):
  forbidden_gifs = ['/gamerescape', '/xivdb', '/giphy', '/tts', '/tenor', '/me', '/tableflip', '/unflip', '/shrug', '/nick']
  spaceIndex = messageContent.find(' ')
  if spaceIndex != -1 and messageContent[:spaceIndex] in forbidden_gifs:
    return
  elif spaceIndex == -1 and messageContent in forbidden_gifs:
    print("Returning due to forbidden gif search")
    return
  search_params = messageContent[1:]
  search_params_sb = ""
  first = True
  for i in range(0,len(search_params)):
    if search_params[i] == ' ':
      search_params_sb = search_params_sb + search_params[len(search_params_sb):i] + '+'
  search_params_sb = search_params_sb + search_params[len(search_params_sb):]
  data = json.loads((urllib.request.urlopen('http://api.giphy.com/v1/gifs/search?q='+search_params_sb+'&api_key=' + str(giphyApiKey) + '&limit=100').read()).decode('utf-8'))
  if(len(data["data"]) <= 0 ):
    await client.send_message(author, "Sorry, but '"+messageContent[1:] + "' returned no results from Giphy.")
  else:
    url = json.dumps(data["data"][random.randint(0,len(data["data"])-1)]["url"], sort_keys = True, indent = 4)
    displayName = ''
    if(hasattr(author, 'nick')):
      displayName = author.nick
    else:
      displayName = author.name
    await client.send_message(message.channel, url[1:len(url)-1] + ' \'' + messageContent[1:] + '\' by ' + displayName + ' with ' + str(len(data["data"])) + ' results')
  if(message and message.channel.name):
    await client.delete_message(message)

async def join_voice(channel_id):
  global player
  global voice_client
  global voice_channel
  global old_voice_members
  if not discord.opus.is_loaded():
    print("Not loaded!")
    discord.opus.load_opus("opuslib")
  else:
    print("Loaded apparently?")
  voice_channel = client.get_channel(channel_id)
  voice = await client.join_voice_channel(voice_channel)
  player = voice.create_ffmpeg_player('VoiceFiles/init.wav')
  print("about to start playing")
  voice_client = voice
  old_voice_members = []
  for i in range(0, len(voice_channel.voice_members)):
    old_voice_members.append(voice_channel.voice_members[i])
  member_change()

async def ping_command(message):
  d = datetime.datetime.utcnow() - message.timestamp
  s = d.seconds*1000 + d.microseconds//1000
  await client.send_message(message.channel, "Ping: {}ms".format(s))

async def help_command(message):
  channel = message.channel
  help_message = """Here are list of available commands:
  < !help >: *Displays a list of available commands*
  < !status >: *Replys indicating I am online*
  < !voice [channel_id] >: *Joins voice channel with specified Id (Special permissions required)*
  < !ping >: *Responds with your ping*
  < !stopvoice >: *Disconnects the bot from the current voice channel (Special permissions required)*
  < !clean [amount] >: *Removes all messages from the channel this command was invoked in that were sent by me or that were commands for the me*
  < !pizza >: *Just do it*
  < !downvote @user >: Downvotes a user and keeps track
  < !upvote @user >: Upvotes a user and keeps track
  < !votes >: Displays all votes
  < !lunchtime >: If it's 11:30AM it's lunch time!
  < /[emote] >: Invoking a slash command will make me search for a relevant gif and then post it
  My main purpose on this server is to announce when users leave or join the voice channel I am in.
  I am a little open source whore. See my birthday suit here: https://github.com/20BBrown14/Voice_Channel_Discord_Bot
  Nibikk is the creator of me, contact him if you have any questions.
  Last updated 02/21/2019""" #Change the text here to customize your help message.
  await client.send_message(channel, help_message)
  await client.delete_message(message)

async def stop_voice(message):
  global voice_client
  await voice_client.disconnect()

async def reddit_link(message):
  await client.send_message(message.channel, "http://www.reddit.com"+message.content)
  await client.delete_message(message)

async def clean_command(message):
  await client.delete_message(message)
  amount = message.content[7:]
  try:
    amount = int(amount)
  except:
    amount = 5
  channel = message.channel
  options = [channel, 50000, delete_message, message, None, None]
  await client.purge_from(channel, limit = amount, check=lambda m: m.author.id == '335445369930514433' or m.content.startswith('!'))

def delete_message(message):
  return False
  #if(message.author.id == '335445369930514433' or message.content.startswith('!')):
   # return True

async def vote_command(message, vote):
  content = ''
  if(vote != 'display' and vote == 'down'):
    content = message.content[10:]
  elif(vote != 'display' and vote == 'up'):
    content = message.content[8:]
  votesFile = ''
  rows = []
  foundName = False
  displayString = 'Name, Upvotes, Downvotes, Net score\n'
  if (not content.startswith('<@') or not content.endswith('>')) and vote != 'display':
    return 0
  if not (Path('votes.csv').is_file()):
    votesFile = open('votes.csv', "x")
    votesFile.write("name,upvotes,downvotes,net")
    votesFile.close()
  with open('votes.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
      if(vote == 'display'):
        foundName = True
        newStringLine = row['name']+': '+row['upvotes'] + ", " + row['downvotes'] + ", " + row['net']
        displayString = displayString + newStringLine + "\n"
      elif row['name'] == content:
        foundName = True
        if(vote == 'down' and row['name'] != message.author.mention):
          row['downvotes'] = str(int(row['downvotes']) - 1)
          row['net'] = str(int(row['net']) - 1)
        elif(vote == 'up' and row['name'] != message.author.mention):
          row['upvotes'] = str(int(row['upvotes']) + 1)
          row['net'] = str(int(row['net']) + 1)
        else:
          await client.send_message(message.author, "Stop trying to " + vote + "vote yourself you goddamn hooligan!")
          print("Someone tried to upvote themselves")
      rows.append(row)
    if not foundName:
      if(vote == 'down' and content != message.author.mention):
        newRow = OrderedDict([('name', content), ('upvotes', '0'), ('downvotes', '-1'), ('net', '-1')])
      elif(vote == 'up' and content != message.author.mention):
        newRow = OrderedDict([('name', content), ('upvotes', '1'), ('downvotes', '0'), ('net', '1')])
      rows.append(newRow)
  with open('votes.csv', mode='w') as csv_file:
    fieldnames=['name','upvotes','downvotes','net']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for row in rows:
      writer.writerow(row)
  if(message.content == '!upvote <@!335445369930514433>'):
    thankList = ["🇹", "🇭", "🇦", "🇳", "🇰"]
    youList = ["🇾", "🇴", "🇺"]
    for emoji in thankList:
      await client.add_reaction(message, emoji)
    await client.add_reaction(message, "⬛")
    for emoji in youList:
      await client.add_reaction(message, emoji)
  elif(message.content == '!downvote <@!335445369930514433>'):
    thankList = ["🇸", "🇨", "🇷", "🇪", "🇼"]
    youList = ["🇾", "🇴", "🇺"]
    for emoji in thankList:
      await client.add_reaction(message, emoji)
    await client.add_reaction(message,  "⬛")
    for emoji in youList:
      await client.add_reaction(message, emoji)
  #await client.send_message(message.channel, displayString)
  if(vote == 'display'):
    await client.send_message(message.channel, displayString)
    await client.delete_message(message)


async def mark_command(message):
  now = datetime.datetime.now()
  then = datetime.datetime(2019,2,18,8,30,0)
  timeString = str(now-then)
  timeDelta = (now-then)
  reply = ''
  FORMATCASE = "ALL"
  months, days = divmod(timeDelta.days, 31)
  hours, remainder = divmod(timeDelta.seconds, 3600)
  minutes, seconds = divmod(remainder, 60)
  if(months and days):
    reply = "There has been %d months, %d days, %d hours, %d minutes, and %d seconds since <@!547509875308232745> got rekt at foosball" % (months, days, hours, minutes, seconds)
  elif(months and not days):
    reply = "There has been %d months, %d hours, %d minutes, and %d seconds since <@!547509875308232745> got rekt at foosball" % (months, hours, minutes, seconds)
  elif(not months and days):
    reply = "There has been %d days, %d hours, %d minutes, and %d seconds since <@!547509875308232745> got rekt at foosball" % (days, hours, minutes, seconds)
  elif(not months and not days):
    reply = "There has been %d hours, %d minutes, and %d seconds since <@!547509875308232745> got rekt at foosball" % (hours, minutes, seconds)
  await client.send_message(message.channel, reply)
  await client.delete_message(message)

async def pre_add_reaction(message):
  users = { 'Branden': '<@!159785058381725696>', 'Harold': '<@!451156129830141975>', 'Grant': '<@!314454492756180994>', 'Kevin': '<@!122149736659681282>', 'Mark': '<@!547509875308232745>'}
  if(users['Branden'] in message.content):
    emoji = get(client.get_all_emojis(), name='Branden')
    await client.add_reaction(message, emoji)
  if(users['Harold'] in message.content):
    emoji = get(client.get_all_emojis(), name='Harold')
    await client.add_reaction(message, emoji)
  if(users['Grant'] in message.content):
    emoji = get(client.get_all_emojis(), name='Grant')
    await client.add_reaction(message, emoji)
  if(users['Kevin'] in message.content):
    emoji = get(client.get_all_emojis(), name='Kevin')
    await client.add_reaction(message, emoji)
  if(users['Mark'] in message.content):
    emoji = get(client.get_all_emojis(), name='Mark')
    await client.add_reaction(message, emoji)
  
async def lunch_command(message):
  global lunch_hour
  global lunch_minute
  gifSearches = ['/excited', '/hell yes', '/I\'m ready', '/Let\'s do this', '/Leggo', '/Lunch time']
  now = datetime.datetime.now()
  lunch_time = datetime.datetime(now.year, now.month, now.day, lunch_hour, lunch_minute)
  tdelta = lunch_time - now
  delta_seconds = tdelta.seconds
  if(now.hour == lunch_hour and now.minute == lunch_minute):
    await client.send_message(message.channel, 'You bet! It\'s lunch time!')
  elif(0 > tdelta.days):
    await client.send_message(message.channel, 'You\'ve already had lunch today. Calm down.')
  elif(now.hour == lunch_hour):
    if(10 * 60 > delta_seconds):
      await client.send_message(message.channel, 'Almost lunch time. I\'m so excited. Are you excited?')
      randomInt = random.randint(0, len(gifSearches)-1)
      await client.send_message(message.channel, gifSearches[randomInt])
    elif(30 * 60 > delta_seconds):
      await client.send_message(message.channel, 'Almost there! Less than thirty minutes.')
  else:
    minutes = str(now.minute)
    if( len(str(now.minute)) == 1 ):
      minutes = "0" + str(now.minute)
    await client.send_message(message.channel, 'Not lunch time yet. Lunch is at ' + datetime.datetime(now.year, now.month, now.day, lunch_hour, lunch_minute).strftime("%H:%M"))
  await client.delete_message(message)

async def friday_command(message):
  weekday = datetime.datetime.today().weekday()
  calendarList = list(calendar.day_name)

  if(calendarList[weekday] != 'Friday'):
    await client.send_message(message.channel if message.channel.name else message.author, "Lol sucks you to be sucka, It\'s only " + calendarList[weekday] + '.')
  else:
    await client.send_message(message.channel if message.channel.name else message.author, "Friday!")
    await client.send_message(message.channel if message.channel.name else message.author, "/friday")

def emojify(string):
  emojiMessage = ''
  for c in string:
    if not c.isalpha():
      emojiMessage += c
      continue
    emojiMessage += ':regional_indicator_' + c + ':'
  return emojiMessage

async def emojify_command(message):
  content = emojify(message.content[9:].lower())
  author = emojify(message.author.name.lower() + ': ')
  if hasattr(message.author, 'nick'):
    author = emojify(message.author.nick.lower() + ': ')
  channel = message.channel if message.channel.name else message.author
  emojiMessage = author + "\n\n" + content
  await client.send_message(channel, emojiMessage)
  await client.delete_message(message)
  
async def timecard_reminder(message):
  global timecard_hour
  global thirtyMinWarning
  now = datetime.datetime.today()
  hour = now.hour
  minute = now.minute
  day = now.weekday()
  if(day != 4):
    return False
  if(day != 4 and not hour >= 13):
    return False
  elif(hour > timecard_hour and not hour >= 17):
    reminderMessage = '@everyone do not forget to submit your time sheets! You only have ' + str(17-hour) + ' hours left!'
    await client.send_message(discord.Object(id='514154258245877764'), reminderMessage)
    timecard_hour = hour
  elif(hour == 16 and minute >= 30 and hour <= timecard_hour and not thirtyMinWarning):
    thirtyMinWarning = True
    reminderMessage = '@everyone do not forget to submit your time sheet before you leave!'
    await client.send_message(discord.Object(id='514154258245877764'), reminderMessage)
    timecard_hour = 17
  else:
    return False

async def set_lunch_command(message):
  global lunch_hour
  global lunch_minute
  global foos_time
  channel = message.channel if message.channel.name else message.author
  content = message.content[10:]
  splitString = content.split(',')
  lunch_hour = int(splitString[0])
  lunch_minute = int(splitString[1])
  now = datetime.datetime.now()
  newLunch = datetime.datetime(now.year, now.month, now.day, lunch_hour, lunch_minute)
  foos_time = newLunch + datetime.timedelta(seconds= 30 * 60)
  await client.send_message(channel, 'Lunch time has been set to ' + newLunch.strftime("%Y-%m-%d %H:%M:%S"))
  await client.delete_message(message)

async def set_foos_command(message):
  global foos_time
  channel = message.channel if message.channel.name else message.author
  content = message.content[9:]
  splitString = content.split(',')
  foos_hour = int(splitString[0])
  foos_minute = int(splitString[1])
  now = datetime.datetime.now()
  foos_time = datetime.datetime(now.year, now.month, now.day, foos_hour, foos_minute)
  await client.send_message(channel, 'Foos time has been set to ' + foos_time.strftime("%Y-%m-%d %H:%M:%S"))
  await client.delete_message(message)

async def foos_command(message):
  global foos_time
  gifSearches = ['/excited', '/hell yes', '/I\'m ready', '/Let\'s do this', '/Leggo', '/Lunch time']
  now = datetime.datetime.now()
  tdelta = foos_time - now
  delta_seconds = tdelta.seconds
  if(now.hour == foos_time.hour and now.minute == foos_time.minute):
    await client.send_message(message.channel, 'You bet! It\'s foos time!')
  elif(0 > tdelta.days):
    await client.send_message(message.channel, 'The last foos time was at ' + foos_time.strftime("%H:%M"))
  elif(now.hour == foos_time.hour):
    if(10 * 60 > delta_seconds):
      await client.send_message(message.channel, 'Almost foos time. I\'m so excited. Are you excited?')
      randomInt = random.randint(0, len(gifSearches)-1)
      await client.send_message(message.channel, gifSearches[randomInt])
    elif(30 * 60 > delta_seconds):
      await client.send_message(message.channel, 'Almost there! Less than thirty minutes.')
  else:
    minutes = str(now.minute)
    if( len(str(now.minute)) == 1 ):
      minutes = "0" + str(now.minute)
    await client.send_message(message.channel, 'Not foos time yet. Foos is at ' + datetime.datetime(now.year, now.month, now.day, foos_time.hour, foos_time.minute).strftime("%H:%M"))
  await client.delete_message(message)

async def count_audit(message):
  try:
    oldCount = -1
    newCount = -1
    first = True
    async for serverMessage in client.logs_from(message.channel, limit=2):
      if(first):
        newCount = int(serverMessage.content)
        first = False
        continue
      oldCount = int(serverMessage.content)
      if(newCount != oldCount + 1):
        await client.delete_message(message)
  except:
    await client.delete_message(message)

async def google_command(message):
  search = message.content[7:]
  modifiedSearchString = ''
  lmgtfyPrefix = 'https://lmgtfy.com/?q='
  for c in search:
    if c == ' ':
      modifiedSearchString += '+'
    else:
      modifiedSearchString += c
  try:
    shortener = Shortener('Tinyurl')
    await client.send_message(message.channel if message.channel.name else message.author, shortener.short(lmgtfyPrefix + modifiedSearchString))
  except:
    await client.send_message(message.author, 'Something went wrong shortening the URL. Here is the raw link: ' + lmgtfyPrefix + modifiedSearchString)
  await client.delete_message(message)
  
    
    
    

@client.event
async def on_ready():
    #info
    global timecard_hour
    global lunch_hour
    global lunch_minute
    global foos_time
    global mess_with_kevin
    global thirtyMinWarning
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print(len(client.messages))
    now = datetime.datetime.now()
    timecard_hour = 12
    lunch_hour = 11
    lunch_minute = 30
    lunch_time = datetime.datetime(now.year, now.month, now.day, lunch_hour, lunch_minute)
    foos_time = lunch_time + datetime.timedelta(seconds=30*60)
    mess_with_kevin = False
    thirtyMinWarning = False





@client.event
async def on_message(message):
  global mess_with_kevin
  if(message.author != client.user and message.channel.name):
    message_string = (message.author.name + " said : \"" + message.content + "\" in #" + message.channel.name + " @ " + time.ctime())
    print(message_string)
    await client.send_message(discord.Object(id='549667908884889602'), message_string)
  elif(message.author != client.user and not message.channel.name):
    print(message.author.name + " said: \"" + message.content + "\" privately")
  await pre_add_reaction(message)
  if(mess_with_kevin and message.author.id == '122149736659681282' and (message.content.startswith('!') or message.content.startswith('/'))):
    await client.send_message(message.author, 'Command not recognized. Please try again.')
    await client.send_message(message.author, '!downvote <@!122149736659681282>')
    await client.delete_message(message)
    return 0
  if(message.author != client.user and message.channel.name):
    await timecard_reminder(message)
  if(message.channel.id == '540194885865832518'):
    await count_audit(message)
  elif(message.content.startswith('!voice')):
    if(message.author.id == '159785058381725696' or message.author.id == '328175857707253760' or message.author.id == '314840626820677643' or message.author.id == '209415024354000897'): #These are user IDs and the logic only allows the players with this user ID to use this command
      if(len(message.content) < len('!voice ')):
        await client.send_message(message.channel, 'Please provide a voice channel id')
        return
      channelId = message.content[len('!voice '):]
      await client.send_message(message.channel, 'Joining voice channel with\nID: ' + channelId +'\nName: ' + client.get_channel(channelId).name)
      await join_voice(channelId)
      print("Joined voice channel with Id")
    else:
      count = 0
      await client.send_message(message.channel, "Sorry, you do not have permission to use this command. Please contact Nibikk if you have any questions.") #Change this line to yourself or simply "Bot Admin"
  elif(message.content.startswith('!status')):
    await client.send_message(message.channel, 'I am here')
  elif(message.content.startswith('!help')):
    await help_command(message)
  elif(message.content.startswith('!ping')):
    await ping_command(message)
  elif(message.content.startswith('!stopvoice')):
    if(message.author.id == '159785058381725696' or message.author.id == '328175857707253760'):
      await stop_voice(message)
  elif(message.content.startswith('/r/')):
    await reddit_link(message)
  elif(message.content.startswith('!clean')):
    await clean_command(message)
  elif(message.content.startswith('!pizza')):
    await client.send_message(message.channel, 'Pizza? Who\'s paying for this? Not me.')
  elif(message.content.startswith('!Mugglewump')):
    if(message.author.id == '159785058381725696' or message.author.id == '83809782691004416'):
      await client.send_message(message.channel, '<@328175857707253760> is a dope Templar!')
  elif(message.content.startswith('!downvote')):
    await vote_command(message, 'down')
  elif(message.content.startswith('!upvote')):
    await vote_command(message, 'up')
  elif(message.content.startswith('!votes')):
    await vote_command(message, 'display')
  elif(message.content.lower() == '!lunchtime' or message.content.lower() == '!lunch'):
    await lunch_command(message)
  elif(message.content.startswith('!Mark')):
    await mark_command(message)
  elif(message.content.startswith('!sendMessage')):
    await client.send_message(discord.Object(id='514154258245877764'), message.content[12:])
  elif(message.content.lower().startswith('i\'m')):
    if(' ' not in message.content[4:]):
      await client.send_message(message.channel if message.channel.name else message.author, "Hi " + message.content[4:] + ", I\'m Roboto.")
  elif(message.content.lower().startswith('!friday')):
    await friday_command(message)
  elif(message.content.lower().startswith('!emojify')):
    await emojify_command(message)
  elif(message.content.lower().startswith('!setlunch')):
    await set_lunch_command(message)
  elif(message.content.lower().startswith('!setfoos')):
    await set_foos_command(message)
  elif(message.content.lower().startswith('!foos')):
    await foos_command(message)
  elif(message.content.lower().startswith('!google')):
    await google_command(message)
  elif(message.content.lower() == 'lol'):
    await client.send_message(message.channel if message.channel.name else message.author, 'lo\nlo\nlol')
  elif(message.content.lower() == ('!messwithkevin')):
    if (message.author.id == '159785058381725696'):
      mess_with_kevin = not mess_with_kevin
      await client.send_message(message.channel if message.channel.name else message.author, 'Mess with kevin = ' + str(mess_with_kevin))
  elif(message.content.lower() == ('!version')):
    await client.send_message(message.channel if message.channel.name else message.author, 'Version: 02252019-2')
  elif(message.content.startswith('/')):
    await giphy_command(message.content, message.author, message)

client.run(discordApiKey)
