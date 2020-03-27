#harry_potter.py

import discord
from pathlib import Path
import os
import time
from natsort import natsorted, ns
import asyncio
import globals_file
from client_interactions import send_message

"""
Harry Potter command

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@param channel: The channel to send the command response to
@result: sends a message always
@result: joins voice channel and plays harry potter audio books
"""
async def command(client, message, player_change):

  if(player_change == 'pause'):
    if(globals_file.player != None and globals_file.player.is_playing()):
      globals_file.player.pause()
      await send_message(message, "Player has been paused")
    return
  elif(player_change == 'stop'):
    if(globals_file.player != None and globals_file.player.is_playing() or not globals_file.player.is_done()):
      globals_file.player.stop()
      globals_file.player = None
      await globals_file.voice_client.disconnect()
      globals_file.voice_client = None
      await send_message(message, "Player has been stopped")
    return
  elif(player_change == 'resume'):
    if(globals_file.player != None and not globals_file.player.is_playing()):
      globals_file.player.resume()
      await send_message(message, "Player has been resumed")
    return
  elif(player_change == 'begin'):
    if(globals_file.player != None):
      await send_message(message, 'Player already initialized. Try `!harrypotter resume`')
      return
    args = message.content[len('!harrypotter begin '):]
    args = args.split(' ')
    chapter_selection = ''
    channel_id = 0
    if('chapter' in args[0].lower()):
      chapter_selection = args[0].lower()
      channel_id = args[1]
    else:
      channel_id = args[0]
    print(chapter_selection)
    print(channel_id)

    # figure out what chapter to start
    # HP#-Chapter##-Part## 2, 11-12, 18-19 
    book_number = 0
    chapter = 0
    part = 0
    start_file_path = ''
    if(chapter_selection != ''):
      book_number = chapter_selection[2]
      chapter = chapter_selection[11:13]
      part = chapter_selection[18:20]
      try:
        book_number = int(book_number)
        chapter = int(chapter)
        part = int(part)
      except:
        await send_message(message, 'Use format `HP#-Chapter##-Part##` to define a chapter to start at. For one digit numbers for chapter and part use a leading 0.')
        return
      if(book_number > 7 or book_number < 1):
        await send_message(message, 'Book number must be 1-7, inclusive')
        return
      if(chapter < 1):
        await send_message(message, 'Chapter must be greater than 01')
        return
      if(part < 1):
        await send_message(message, 'Part must be greater than 01')
        return
      book_name = ''
      file_name = "Chapter %d.%d HP%d" % (chapter, part, book_number)
      if(book_number == 1):
        book_name = '1Harry_Potter_and_the_sorcerers_Stone/'
      elif(book_number == 2):
        book_name = '2Harry Potter and the Chamber of Secrets/'
      elif(book_number == 3):
        book_name = '3Harry Potter and the Prisoner of Azkaban/'
      elif(book_number == 4):
        book_name = '4Harry Potter and the Goblet of Fire/'
      elif(book_number == 5):
        book_name = '5Harry Potter and the Order of the Phoenix/'
      elif(book_number == 6):
        book_name = '6Harry Potter and the Half-Blood Prince/'
      elif(book_number == 7):
        book_name = '7Harry Potter And The Deathly Hallows/'
      start_file_path = 'Harry_Potter/' + book_name + file_name

# Book 1 - 1Harry_Potter_and_the_Sorcerers_Stone/Chapter #.# HP1.wma
# Book 2 - 2Harry Potter and the Chamber of Secrets/Chapter #.# HP2.wma
# Book 3 - 3Harry Potter and the Prisoner of Azkaban/Chapter #.# HP3.wma
# Book 4 - 4Harry Potter and the Goblet of Fire/Chapter #.# HP4.wma
# Book 5 - 5Harry Potter and the Order of the Phoenix/Chapter #.# HP5
# Book 6 - 6Harry Potter and the Half-Blood Prince/Chapter #.# HP6.wma
# Book 7 - 7Harry Potter And The Deathly Hallows/Chapter #.# HP7.wma


    if not discord.opus.is_loaded():
      discord.opus.load_opus("opuslib")

    HP_Books = []

    for root, dirs, files in os.walk('/mnt/USB/Harry_Potter/Harry_Potter'):
      for folder in dirs:
          HP_Books.append(os.path.join(root, folder))


    voice_channel = client.get_channel(channel_id)
    voice = await client.join_voice_channel(voice_channel)
    globals_file.voice_client = voice
	
    HP_Books.sort()

    for book in HP_Books: #13
      if(start_file_path != '' and int(book[35]) < int(start_file_path[13])):
        continue
      audio_files = []
      for root, dirs, files in os.walk(book):
        for some_file in files:
          if '.wma' in some_file and not 'Intro' in some_file and not 'Epilogue' in some_file:
            chapter_and_part = some_file[7:]
            dot_index = chapter_and_part.find('.')
            chapter_number = chapter_and_part[:dot_index]
            part_number = chapter_and_part[dot_index+1:dot_index+3]
            if(start_file_path != '' and int(book[35]) == int(start_file_path[13])):
              if(int(chapter_number) == int(chapter)):
                if(int(part_number) >= int(part)):
                  audio_files.append(os.path.join(root, some_file))
                else:
                  continue
              elif(int(chapter_number) > int(chapter)):
                audio_files.append(os.path.join(root, some_file))
              else:
                continue
            else:
              audio_files.append(os.path.join(root, some_file))
      await send_message(message, "Playing book: %s" % book)
      audio_files = natsorted(audio_files, key=lambda y: y.lower())
      audio_files = natsorted(audio_files, alg=ns.IGNORECASE)
      for book_part in audio_files:
        globals_file.player = globals_file.voice_client.create_ffmpeg_player(book_part)
        globals_file.player.volume = 100/100
        await send_message(message, "Playing audio file: %s" % book_part)
        globals_file.player.start()
        while(not globals_file.player.is_done()):
          await asyncio.sleep(1)
        globals_file.player.stop()
        await send_message(message, "Finished playing audio file: %s" % book_part)
      await send_message(message, "Finished playing book: %s" % book)

TRIGGER_BEGIN = '!harrypotter begin'
TRIGGER_PAUSE = '!harrypotter pause'
TRIGGER_STOP = '!harrypotter stop'
TRIGGER_RESUME = '!harrypotter resume'