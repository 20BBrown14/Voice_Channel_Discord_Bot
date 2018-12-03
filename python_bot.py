#import discord #You'll need to install this
from discord import Client
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
#from dateutil.parser import parse

global player
global voice_client
global voice_channel
global old_voice_members

client = Client()

def member_change():
  global old_voice_members
  global player
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

async def giphy_command(message):
  forbidden_gifs = ['/gamerescape', '/xivdb', '/giphy', '/tts', '/tenor', '/me', '/tableflip', '/unflip', '/shrug', '/nick']
  spaceIndex = message.content.find(' ')
  if message.content[:spaceIndex] in forbidden_gifs:
    return
  search_params = message.content[1:]
  search_params_sb = ""
  first = True
  for i in range(0,len(search_params)):
    if search_params[i] == ' ':
      search_params_sb = search_params_sb + search_params[len(search_params_sb):i] + '+'
  search_params_sb = search_params_sb + search_params[len(search_params_sb):]
  data = json.loads(urllib.request.urlopen('http://api.giphy.com/v1/gifs/search?q='+search_params_sb+'&api_key=&limit=100').read()) #Add your own giphy API here key
  url = json.dumps(data["data"][random.randint(0,len(data["data"]))]["url"], sort_keys = True, indent = 4)
  await client.send_message(message.channel, url[1:len(url)-1] + ' \'' + message.content[1:] + '\' by ' + message.author.nick + ' with ' + str(len(data["data"])) + ' results')
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
  d = datetime.utcnow() - message.timestamp
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
  Nibikk is the creator of me, contact him if you have any questions.
  Last updated 11/27/2018""" #Change the text here to customize your help message.
  await client.send_message(channel, help_message)
  await client.delete_message(message)

async def stop_voice(message):
  global voice_client
  await voice_client.disconnect()

async def reddit_link(message):
  await client.send_message(message.channel, "http://www.reddit.com"+message.content)
  await client.delete_message(message)

async def clean_command(message):
  channel = message.channel
  options = [channel, 50000, delete_message, message, None, None]
  await client.purge_from(channel, limit = 50000, check=lambda m: m.author.id == '335445369930514433' or m.content.startswith('!'))

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
        if(vote == 'down'):
          row['downvotes'] = str(int(row['downvotes']) - 1)
          row['net'] = str(int(row['net']) - 1)
        elif(vote == 'up'):
          print("changing it up")
          row['upvotes'] = str(int(row['upvotes']) + 1)
          row['net'] = str(int(row['net']) + 1)
      rows.append(row)
    if not foundName:
      if(vote == 'down'):
        newRow = OrderedDict([('name', content), ('upvotes', '0'), ('downvotes', '-1'), ('net', '-1')])
      elif(vote == 'up'):
        newRow = OrderedDict([('name', content), ('upvotes', '1'), ('downvotes', '0'), ('net', '1')])
      rows.append(newRow)
  with open('votes.csv', mode='w') as csv_file:
    fieldnames=['name','upvotes','downvotes','net']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for row in rows:
      writer.writerow(row)
  #await client.send_message(message.channel, displayString)
  if(vote == 'display'):
    await client.send_message(message.channel, displayString)
    await client.delete_message(message)

async def mark_command(message):
  today = datetime.date.today()
  rd = relativedelta(today, datetime.date(2019,2,18))
  reply = "Mark's first day at Cerner is in "
  rd.years = rd.years * -1
  rd.months = rd.months * -1
  rd.days = rd.days * -1
  if(rd.years > 0):
    reply = reply + "%(years)d years " % rd.__dict__
  if(rd.months > 0 and rd.years > 0 and rd.days > 0):
    reply = reply + "and %(months)d months and %(days)d days" % rd.__dict__
  elif(rd.months > 0 and rd.years > 0 and not rd.days > 0):
    reply = reply +"and %(months)d months" % rd.__dict__
  elif(rd.months > 0 and not rd.years > 0 and rd.days > 0):
    reply = reply + "%(months)d months and %(days)d days" % rd.__dict__
  elif(rd.months > 0 and not rd.years > 0 and not rd.days > 0):
    reply = reply + "%(months)d months" % rd.__dict__
  await client.send_message(message.channel, reply)
  await client.delete_message(message)

async def pre_add_reaction(message):
  users = { 'Branden': '<@!159785058381725696>', 'Harold': '<@!451156129830141975>', 'Grant': '<@!314454492756180994>', 'Kevin': '<@!122149736659681282>'}
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
  
async def lunch_command(message):
  now = datetime.now()
  if(now.hour == 11 and now.minute == 30):
    await client.send_message(message.channel, 'You bet! It\'s lunch time!')
  elif(now.hour >= 11 and now.minute > 30):
    await client.send_message(message.channel, 'You\'ve already had lunch today. Calm down.')
  else:
    await client.send_message(message.channel, 'Not lunch time yet. It\'s only '+ str(now.hour) +':' + str(now.minute))
  
@client.event
async def on_ready():
    #info
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    if not os.path.exists("VoiceFiles"):
      os.makedirs("VoiceFiles")
    if( not (Path("VoiceFiles/joined.wav").is_file())):
      textToWav("Has joined the channel", "VoiceFiles/joined.wav")
    if( not (Path("VoiceFiles/left.wav").is_file())):
      textToWav("Has left the channel", "VoiceFiles/left.wav")
    if( not (Path("VoiceFiles/init.wav").is_file())):
      textToWav("init", "VoiceFiles/init.wav")
    print(len(client.messages))

@client.event
async def on_message(message):
  if(message.author != client.user):
    print(message.author.name + " said: \"" + message.content + "\" in #" + message.channel.name + " @ " + time.ctime())
  await pre_add_reaction(message)
  if(message.content.startswith('!voice')):
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
  elif(message.content == '!lunchtime'):
    await lunch_command(message)
  elif(message.content.startswith('!Mark')):
    await mark_command(message)
  elif(message.content.startswith('/')):
    await giphy_command(message)

client.run("") #Add your own bot's token here
