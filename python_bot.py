
# library imports
import calendar
from collections import OrderedDict
import csv
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import datetime
from discord import Client #you'll need this install
from discord.utils import get
import discord
import json
import os
from pathlib import Path
from pyshorteners import Shortener
import random
import subprocess #You'll need to install this and also download espeak and put in the same directory as this source code.
import threading
from threading import Timer
import time
import urllib.request
import globals_file

# local file imports
import config
from commands import help, weather, single_giphy_results_display, harry_potter, define

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
global weather_cache
global last_giphy_search
global limit_giphy_searches
global giphy_file_contents

#from config.py file
discordApiKey = config.bot_token 
giphyApiKey = config.giphy_api_key
weather_api_key = config.weather_api_key
dictionary_api = config.dictionary_api
spanish_english_dictionary_api = config.spanish_english_api

# User IDs
id_branden = '159785058381725696'
id_grant   = '314454492756180994'
id_kevin   = '122149736659681282'
id_mark    = '547509875308232745'
id_harold  = '451156129830141975'

# Channel IDs
id_general         = '514154258245877764'
id_new_bot_testing = '548166917987500053'
id_count           = '540194885865832518'

# Update for each revision using format yyyy-mm-dd_#
# where '#' is the release number for that day.
# e.g. 2019-03-31_1 is the first release of March 31st, 2019
version = '2019-10_28_1'


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
  global last_giphy_search
  global limit_giphy_searches
  global giphy_file_contents
  now = datetime.datetime.now().timestamp()
  if(limit_giphy_searches and now - last_giphy_search < 10):
    await client.delete_message(message)
    await client.send_message(message.author, 'Too many giphy searches server wide. You can search again in %d seconds' % int(10-(now-last_giphy_search)))
    return
  last_giphy_search = now
  forbidden_gifs = ['/gamerescape', '/xivdb', '/giphy', '/tts', '/tenor', '/me', '/tableflip', '/unflip', '/shrug', '/nick']
  spaceIndex = messageContent.find(' ')
  if spaceIndex != -1 and messageContent[:spaceIndex] in forbidden_gifs:
    return
  elif spaceIndex == -1 and messageContent in forbidden_gifs:
    print("Returning due to forbidden gif search")
    return
  if('\n' in message.content):
    await client.send_message(message.author, "Forbidden search string used")
    return
  search_params = messageContent[1:]
  search_params_sb = ""
  first = True
  for i in range(0,len(search_params)):
    if search_params[i] == ' ':
      search_params_sb = search_params_sb + search_params[len(search_params_sb):i] + '+'
  search_params_sb = search_params_sb + search_params[len(search_params_sb):]
  data = json.loads((urllib.request.urlopen('http://api.giphy.com/v1/gifs/search?q='+search_params_sb+'&api_key=' + str(giphyApiKey) + '&limit=100').read()).decode('utf-8'))
  new_result = True
  if(len(data["data"]) == 1):
    single_result = messageContent[1:].lower()
    if(os.path.isfile('single_giphy_results.txt')):
      if(giphy_file_contents == ''):
        f = open('single_giphy_results.txt', 'r')
        giphy_file_contents = f.read().split('\n')
        f.close()
        del giphy_file_contents[-1]
        with open('single_giphy_results.txt') as f:
          for line in f:
            if(single_result == line.rstrip().lower()):
              new_result = False
              break
        if(new_result):
          f = open("single_giphy_results.txt", "a")
          f.write(messageContent[1:] + '\n')
          f.close()
          giphy_file_contents.append(messageContent[1:])
      else:
        for search in giphy_file_contents:
          if(single_result == search.rstrip().lower()):
            new_result = False
            break
        if(new_result):
          f = open('single_giphy_results.txt', 'a')
          f.write(messageContent[1:] + '\n')
          f.close()
          giphy_file_contents.append(messageContent[1:])
    else:
      f = open("single_giphy_results.txt", 'w')
      f.write(messageContent[1:] + '\n')
      f.close()
  if(len(data["data"]) <= 0 ):
    await client.send_message(author, "Sorry, but '"+messageContent[1:] + "' returned no results from Giphy.")
  else:
    url = json.dumps(data["data"][random.randint(0,len(data["data"])-1)]["url"], sort_keys = True, indent = 4)
    displayName = ''
    if(hasattr(author, 'nick')):
      displayName = author.nick
    else:
      displayName = author.name
    if(len(data["data"]) == 1):
      if(new_result):
        await client.send_message(message.channel, "%s \'%s\' by %s with %s result. Single result added." % (url[1:len(url)-1], messageContent[1:], displayName, str(len(data["data"]))))
      else:
        await client.send_message(message.channel, "%s \'%s\' by %s with %s result. Single result not added." % (url[1:len(url)-1], messageContent[1:], displayName, str(len(data["data"]))))
    else:
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
    reply = "There has been %d months, %d days, %d hours, %d minutes, and %d seconds since <@!%s> got rekt at foosball" % (months, days, hours, minutes, seconds, id_mark)
  elif(months and not days):
    reply = "There has been %d months, %d hours, %d minutes, and %d seconds since <@!%s> got rekt at foosball" % (months, hours, minutes, seconds, id_mark)
  elif(not months and days):
    reply = "There has been %d days, %d hours, %d minutes, and %d seconds since <@!%s> got rekt at foosball" % (days, hours, minutes, seconds, id_mark)
  elif(not months and not days):
    reply = "There has been %d hours, %d minutes, and %d seconds since <@!%s> got rekt at foosball" % (hours, minutes, seconds, id_mark)
  await client.send_message(message.channel, reply)
  await client.delete_message(message)

async def pre_add_reaction(message):
  users = { 'Branden': '<@!' + id_branden + '>', 'Harold': '<@!' + id_harold + '>', 'Grant': '<@!' + id_grant + '>', 'Kevin': '<@!' + id_kevin + '>', 'Mark': '<@!' + id_mark + '>'}
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
    timecard_hour = 12
    return False
  if(day != 4 and not hour >= 13):
    return False
  elif(hour > timecard_hour and not hour >= 17):
    reminderMessage = '@everyone do not forget to submit your time sheets! You only have ' + str(17-hour) + ' hours left!'
    await client.send_message(discord.Object(id=id_general), reminderMessage)
    timecard_hour = hour
  elif(hour == 16 and minute >= 30 and hour <= timecard_hour and not thirtyMinWarning):
    thirtyMinWarning = True
    reminderMessage = '@everyone do not forget to submit your time sheet before you leave!'
    await client.send_message(discord.Object(id=id_general), reminderMessage)
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
    await client.send_message(message.channel if message.channel.name else message.author, '<%s>' % shortener.short(lmgtfyPrefix + modifiedSearchString))
  except:
    await client.send_message(message.author, 'Something went wrong shortening the URL. Here is the raw link: ' + lmgtfyPrefix + modifiedSearchString)
  await client.delete_message(message)

async def delete_message(client, message):
  try:
    client.get_message(message.channel, message.id)
    if(message.channel.name):
      if(not message.channel.name.lower() == 'bot_commands'):
        await client.delete_message(message)
  except:
    print('Message DNE')

@client.event
async def on_ready():
    #info
    global timecard_hour
    global lunch_hour
    global lunch_minute
    global foos_time
    global mess_with_kevin
    global thirtyMinWarning
    global weather_cache
    global last_giphy_search
    global limit_giphy_searches
    global giphy_file_contents
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
    client_game = discord.Game(name='Goosball v%s' % version)
    weather_cache = json.loads('{}')
    last_giphy_search = 0
    limit_giphy_searches = True
    await client.change_status(game = client_game)
    globals_file.init()
    giphy_file_contents = ''

@client.event
async def on_message(message):
  if(message.channel.name == 'logs'):
    return 0
  global mess_with_kevin
  global limit_giphy_searches
  global giphy_file_contents
  global lunch_hour
  global lunch_minute
  if(message.author != client.user and message.channel.name):
    message_string = (message.author.name + " said : \"" + message.content + "\" in #" + message.channel.name + " @ " + time.ctime())
    print(message_string)
    await client.send_message(discord.Object(id='549667908884889602'), message_string)
  elif(message.author != client.user and not message.channel.name):
    print(message.author.name + " said: \"" + message.content + "\" privately")
  await pre_add_reaction(message)
  if(mess_with_kevin and message.author.id == id_kevin and (message.content.startswith('!') or message.content.startswith('/'))):
    await client.send_message(message.author, 'Command not recognized. Please try again.')
    await client.send_message(message.author, '!downvote <@!' + id_kevin + '>')
    await client.delete_message(message)
    return 0
  if(message.content.lower() == 'foos?'):
    foos_response_array = ['when?', 'omw'];
    await client.send_message(message.channel if message.channel.name else message.author, foos_response_array[random.randint(0,len(foos_response_array)-1)])
  if(message.content.lower() == 'ope'):
    gottem_array = ['gottem', 'gotem', 'gotm', 'gottum', 'gottm', 'gotm', 'gotim', 'gottim', 'oof', 'gotus', 'gottus', '**OOF**', '***OOF***']
    await client.send_message(message.channel if message.channel.name else message.author, gottem_array[random.randint(0,len(gottem_array)-1)])
  if(message.content.lower() == 'oof'):
    oof_array = ['**BIG OOF**','you dun goofed', 'Pay some respect, send an F', 'oh snap','_nice job_','Can we get an F in chat?', 'Press F'];
    await client.send_message(message.channel if message.channel.name else message.author, oof_array[random.randint(0,len(oof_array)-1)])
  if(message.author != client.user and message.channel.name):
    await timecard_reminder(message)
    now = datetime.datetime.now()
    if(now.hour > lunch_hour + 1):
      lunch_hour = 11
      lunch_minute = 30
      lunch_time = datetime.datetime(now.year, now.month, now.day + 1, lunch_hour, lunch_minute)
  if(message.channel.id == id_count):
    await count_audit(message)
  elif(message.content.lower() == ('!version')):
    await client.send_message(message.channel if message.channel.name else message.author, 'Version: ' + version)
  elif(message.content.startswith('!status')):
    await client.send_message(message.channel, 'I am here')
  elif(message.content.startswith(help.TRIGGER)):
    await help.command(client, message)
  elif(message.content.startswith('!ping')):
    await ping_command(message)
  elif(message.content.startswith('!stopvoice')):
    if(message.author.id == id_branden):
      await stop_voice(message)
  elif(message.content.startswith('/r/')):
    await reddit_link(message)
  elif(message.content.startswith('/')):
    await giphy_command(message.content, message.author, message)
  elif(message.content.startswith('!clean')):
    await clean_command(message)
  elif(message.content.startswith('!pizza')):
    await client.send_message(message.channel, 'Pizza? Who\'s paying for this? Not me.')
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
    await client.send_message(discord.Object(id=id_general), message.content[12:])
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
  elif(message.content.startswith(single_giphy_results_display.TRIGGER)):
    await single_giphy_results_display.command(client, message, message.channel if message.channel.name else message.author, delete_message, giphy_file_contents)
  elif(message.content.lower() == 'lol'):
    await client.send_message(message.channel if message.channel.name else message.author, 'lo\nlo\nlol')
  elif(message.content.lower() == ('!messwithkevin')):
    if (message.author.id == id_branden):
      mess_with_kevin = not mess_with_kevin
      await client.send_message(message.channel if message.channel.name else message.author, 'Mess with kevin = ' + str(mess_with_kevin))
  elif(message.content.lower() == '!limitsearchestoggle'):
    limit_giphy_searches = not limit_giphy_searches
    await client.send_message(message.author, 'Search limit has been toggled %s' % str(limit_giphy_searches))
  elif(message.content.lower().startswith(weather.TRIGGER)):
    await weather.command(client, message, message.channel if message.channel.name else message.author, delete_message, weather_cache, weather_api_key)
  elif(message.content.lower().startswith(harry_potter.TRIGGER_PAUSE)):
    await harry_potter.command(client, message, message.channel if message.channel.name else message.author, delete_message, 'pause')
  elif(message.content.lower().startswith(harry_potter.TRIGGER_STOP)):
    await harry_potter.command(client, message, message.channel if message.channel.name else message.author, delete_message, 'stop')
  elif(message.content.lower().startswith(harry_potter.TRIGGER_RESUME)):
    await harry_potter.command(client, message, message.channel if message.channel.name else message.author, delete_message, 'resume')
  elif(message.content.lower().startswith(harry_potter.TRIGGER_BEGIN)):
    await harry_potter.command(client, message, message.channel if message.channel.name else message.author, delete_message, 'begin')
  elif(message.content.lower().startswith(define.TRIGGER)):
    await define.command(client, message, message.channel if message.channel.name else message.author, delete_message, dictionary_api)
  elif(message.content.startswith('!voice')):
    if(message.author.id == id_branden): # only users in this if can use this command
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
client.run(discordApiKey)
