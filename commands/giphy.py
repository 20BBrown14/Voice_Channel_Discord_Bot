import os
import random
import urllib.request
from urllib.request import urlopen
import json

import globals_file
from client_interactions import send_message, delete_message

"""
Giphy Command
Handles searching for a gif from giphy
ex: /some search term

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@param giphy_api_key: api key to use for the giphy request
@result: Sends a message always unless no results are returned
@result: Deletes triggering message always
"""
async def command(client, message, giphy_api_key):
  giphy_cache = globals_file.giphy_file_cache
  await delete_message(message)
  message_content = message.content
  message_author = message.author
  
  search_params = message_content[1:].split(' ')
  search_params_joined = '+'.join(search_params)
  giphy_url = 'http://api.giphy.com/v1/gifs/search?q=%s&api_key=%s&limit=100' % (search_params_joined, str(giphy_api_key))
  data = json.loads((urlopen(giphy_url).read()).decode('utf-8'))
  new_result = False
  if(len(data["data"]) == 1):
    new_result = write_to_file(message_content[1:], data, giphy_cache)
  if(len(data["data"]) > 0):
    gif_url = json.dumps(data["data"][random.randint(0, len(data["data"])-1)]["url"], sort_keys = True, indent = 4)
    display_name = message_author.nick if hasattr(message_author, 'nick') else message_author.name
    result_count = len(data["data"])
    response_string = '%s \'%s\' by %s with %s %s. %s' % (gif_url[1:len(gif_url)-1], message_content[1:], display_name, str(result_count), 'results' if result_count > 1 else 'result', 'Single result %sadded.' % ('not ' if not new_result else '') if len(data["data"]) == 1 else '')
    await send_message(message, response_string)

def write_to_file(search_string, data, giphy_cache):
  new_result = True
  if(len(data["data"]) == 1):
    single_result = search_string.lower()
    if(os.path.isfile('single_giphy_results.txt')):
      if(giphy_cache == None):
        f = open('single_giphy_results.txt', 'r')
        giphy_cache = f.read().split('\n')
        
        f.close()
        del giphy_cache[-1]
        with open('single_giphy_results.txt') as f:
          for line in f:
            if(single_result == line.rstrip().lower()):
              new_result = False
              break
        if(new_result):
          f = open('single_giphy_results.txt', 'a')
          f.write(search_string + '\n')
          f.close()
          giphy_cache.append(search_string)
      else:
        for search in giphy_cache:
          if(single_result == search.rstrip().lower()):
            new_result = False
            break
        if(new_result):
          f = open('single_giphy_results.txt', 'a')
          f.write(search_string + '\n')
          f.close()
          giphy_cache.append(search_string)
    else:
      f = open('single_giphy_results.txt', 'w')
      f.write(search_string + '\n')
      f.close()
    globals_file.giphy_file_cache = giphy_cache
    return new_result
  else:
    return False

# String that triggers this command
TRIGGER = '/'

def is_triggered(message_content):
  return message_content.startswith(TRIGGER)
