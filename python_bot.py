
# library imports
from discord import Client #you'll need this install
import discord
import time

# local file imports
import config
import globals_file
from commands import help, weather, single_giphy_results_display, harry_potter, define, giphy, ping, clean, Mark, lunch, set_lunch, emojify, friday, vote, discipline, discipline_defs
from rules import reddit_link, pre_add_reaction, auto_triggered_messages, timecard_reminder, count_audit
from client_interactions import send_message

#from config.py file
discordApiKey = config.bot_token 
giphyApiKey = config.giphy_api_key
weather_api_key = config.weather_api_key
dictionary_api = config.dictionary_api

client = discord.Client()

@client.event
async def on_ready():
    #info
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    globals_file.init(client, config)
    if(globals_file.game_played_config):
      client_game = discord.Game(name=globals_file.game_played_config['game_played'])
      await client.change_presence(activity = client_game)

@client.event
async def on_message(message):
  if(globals_file.logs_config and message.channel == globals_file.logs_config['logs_channel']):
    return 0

  if(message.author != client.user and message.channel.name and globals_file.logs_config and message.channel.id not in globals_file.logs_config['ignored_channels']):
    message_string = (message.author.name + " said : \"" + message.clean_content + "\" in #" + message.channel.name + " @ " + time.ctime())
    await globals_file.logs_config['logs_channel'].send(message_string)

  await pre_add_reaction.apply(client, message)

  if(message.author != client.user and message.channel.name and globals_file.timecard_reminder_config):
    await timecard_reminder.apply(client, message)

  if(globals_file.count_config and count_audit.is_triggered(message)):
    await count_audit.apply(client, message)

  elif(auto_triggered_messages.is_triggered(message.content)):
    await auto_triggered_messages.apply(client, message)

  elif(message.content.lower() == ('!version')):
    await send_message(message, 'Version: %s' % globals_file.version)

  elif(message.content.startswith('!status')):
    await send_message(message, 'I am here')

  elif(message.content.startswith(help.TRIGGER)):
    await help.command(client, message)

  elif(ping.is_triggered(message.content)):
    await ping.command(client, message)

  elif(reddit_link.is_triggered(message.content)):
    await reddit_link.apply(client, message)

  elif(config.giphy_api_key and giphy.is_triggered(message.content)):
    await giphy.command(client, message, giphyApiKey)

  elif(clean.is_triggered(message.content)):
    await clean.command(client, message)

  elif(message.content.lower() == '!pizza'):
    await send_message(message, 'Pizza? Who\'s paying for this? Definitely not me.')

  elif(vote.is_downvote(message.content)):
    await send_message(message, 'This command is currently unavailable')
    # await vote.command(client, message, 'down')

  elif(vote.is_upvote(message.content)):
    await send_message(message, 'This command is currently unavailable')
    # await vote.command(client, message, 'up')

  elif(vote.is_display(message.content)):
    await send_message(message, 'This command is currently unavailable')
    #await vote.command(client, message, 'display')

  elif(globals_file.lunch_time and lunch.is_triggered(message.content)):
    await lunch.command(client, message)

  elif(Mark.is_triggered(message.content)):
    await Mark.command(client, message, globals_file.id_mark)

  elif(friday.is_triggered(message.content)):
    await friday.command(client, message)

  elif(emojify.is_triggered(message.content)):
    await emojify.command(client, message)

  elif(globals_file.lunch_time and set_lunch.is_triggered(message.content)):
    await set_lunch.command(client, message)

  elif(message.content.startswith(single_giphy_results_display.TRIGGER)):
    await single_giphy_results_display.command(client, message)

  elif(config.weather_api_key and message.content.lower().startswith(weather.TRIGGER)):
    await weather.command(client, message, weather_api_key)

  elif(message.content.lower().startswith(harry_potter.TRIGGER_PAUSE)):
    await send_message(message, 'This command is currently unavailable')
    # await harry_potter.command(client, message, 'pause')

  elif(message.content.lower().startswith(harry_potter.TRIGGER_STOP)):
    await send_message(message, 'This command is currently unavailable')
    # await harry_potter.command(client, message, 'stop')

  elif(message.content.lower().startswith(harry_potter.TRIGGER_RESUME)):
    await send_message(message, 'This command is currently unavailable')
    # await harry_potter.command(client, message, 'resume')

  elif(message.content.lower().startswith(harry_potter.TRIGGER_BEGIN)):
    await send_message(message, 'This command is currently unavailable')
    # await harry_potter.command(client, message, 'begin')

  elif(config.dictionary_api and message.content.lower().startswith(define.TRIGGER)):
    await define.command(client, message, dictionary_api)
    
  elif(message.content.startswith(discipline.TRIGGER)):
    split_content = message.content.split( ' ' )
    await discipline.command(client, message, split_content[ 1 ])

client.run(discordApiKey)
