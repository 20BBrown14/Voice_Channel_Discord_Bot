#harry_potter.py

import discord
from pathlib import Path
import os

"""
Harry Potter command

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@param channel: The channel to send the command response to
@result: sends a message always
@result: joins voice channel and plays harry potter audio books
"""
async def command(client, message, channel, delete_message):

  channel_id = message.content[len('!harrypotter '):]
  print(channel_id)

  if not discord.opus.is_loaded():
    print("Not loaded!")
    discord.opus.load_opus("opuslib")
  else:
    print("Loaded apparently?")
  voice_channel = client.get_channel(channel_id)
  voice = await client.join_voice_channel(voice_channel)
  print("about to start playing")
  voice_client = voice


  file_name = "Harry_Potter/Harry_Potter_and_the_Sorcerers_Stone/05 Chapter 1.3 HP1.wma"
  print((os.path.exists("Harry_Potter/Harry_Potter_and_the_Sorcerers_Stone/01 Intro.1 HP1.wma")))
  print(file_name)
  print(os.getcwd())
  if os.path.exists(file_name):
    print('found file')
    player = voice_client.create_ffmpeg_player(file_name)
    player.volume= 100/100 #Change the left number to adjust over all volume
    player.start()
  else:
    print('file not found')

TRIGGER = '!harrypotter'