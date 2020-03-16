
# library imports
from discord import Client #you'll need this install
import discord
import time

# local file imports
import config
import globals_file
from commands import help, weather, single_giphy_results_display, harry_potter, define, giphy, ping, clean, Mark, lunch, set_lunch, emojify, friday, vote
from rules import reddit_link, pre_add_reaction, auto_triggered_messages, timecard_reminder, count_audit

#from config.py file
discordApiKey = config.bot_token 
giphyApiKey = config.giphy_api_key
weather_api_key = config.weather_api_key
dictionary_api = config.dictionary_api
spanish_english_dictionary_api = config.spanish_english_api

# Channel IDs
id_logs            = '549667908884889602'

# Update for each revision using format yyyy-mm-dd_#
# where '#' is the release number for that day.
# e.g. 2019-03-31_1 is the first release of March 31st, 2019
version = '2020-03-06_2'

client = Client()

@client.event
async def on_ready():
    #info
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    client_game = discord.Game(name='Animal Crossing: New Horizons')
    await client.change_status(game = client_game)
    globals_file.init()

@client.event
async def on_message(message):
  if(message.channel.name == 'logs'):
    return 0

  if(message.author != client.user and message.channel.name):
    message_string = (message.author.name + " said : \"`" + message.content + "`\" in #" + message.channel.name + " @ " + time.ctime())
    print(message_string)
    await client.send_message(discord.Object(id=id_logs), message_string)

  elif(message.author != client.user and not message.channel.name):
    print(message.author.name + " said: \"" + message.content + "\" privately")

  await pre_add_reaction.apply(client, message)

  if(message.author != client.user and message.channel.name):
    await timecard_reminder.apply(client, message)

  if(count_audit.is_triggered(message)):
    await count_audit.apply(client, message)

  elif(auto_triggered_messages.is_triggered(message.content)):
    await auto_triggered_messages.apply(client, message)

  elif(message.content.lower() == ('!version')):
    await client.send_message(message.channel if message.channel.name else message.author, 'Version: ' + version)

  elif(message.content.startswith('!status')):
    await client.send_message(message.channel, 'I am here')

  elif(message.content.startswith(help.TRIGGER)):
    await help.command(client, message)

  elif(ping.is_triggered(message.content)):
    await ping.command(client, message)

  elif(reddit_link.is_triggered(message.content)):
    await reddit_link.apply(client, message)

  elif(giphy.is_triggered(message.content)):
    await giphy.command(client, message, giphyApiKey)

  elif(clean.is_triggered(message.content)):
    await clean.command(client, message)

  elif(message.content.lower() == '!pizza'):
    send_message(client, message, 'Pizza? Who\'s paying for this? Definitely not me.')

  elif(vote.is_downvote(message.content)):
    await vote.command(client, message, 'down')

  elif(vote.is_upvote(message.content)):
    await vote.command(client, message, 'up')

  elif(vote.is_display(message.content)):
    await vote.command(client, message, 'display')

  elif(lunch.is_triggered(message.content)):
    await lunch.command(client, message)

  elif(Mark.is_triggered(message.content)):
    await Mark.command(client, message, id_mark)

  elif(friday.is_triggered(message.content)):
    await friday.command(client, message)

  elif(emojify.is_triggered(message.content)):
    await emojify.command(client, message)

  elif(set_lunch.is_triggered(message.content)):
    await set_lunch.command(client, message)

  elif(message.content.startswith(single_giphy_results_display.TRIGGER)):
    await single_giphy_results_display.command(client, message)

  elif(message.content.lower().startswith(weather.TRIGGER)):
    await weather.command(client, message, weather_api_key)

  elif(message.content.lower().startswith(harry_potter.TRIGGER_PAUSE)):
    await harry_potter.command(client, message, 'pause')

  elif(message.content.lower().startswith(harry_potter.TRIGGER_STOP)):
    await harry_potter.command(client, message, 'stop')

  elif(message.content.lower().startswith(harry_potter.TRIGGER_RESUME)):
    await harry_potter.command(client, message, 'resume')

  elif(message.content.lower().startswith(harry_potter.TRIGGER_BEGIN)):
    await harry_potter.command(client, message, 'begin')

  elif(message.content.lower().startswith(define.TRIGGER)):
    await define.command(client, message, dictionary_api)

client.run(discordApiKey)
