# single_giphy_results_display.py

import os

from client_interactions import delete_message, send_message
import globals_file

async def print_results(client, message, single_results, count):
  await send_message(client, message, "Number of results = %d" % (count))
  for string in single_results:
    if len(string) > 0:
      await send_message(client, message, "```\n%s```" % string[:-2])

async def command(client, message):
  await delete_message(client, message)
  single_results_array = []
  single_results_string = ''
  single_results_count = 0
  giphy_file_contents = globals_file.giphy_file_cache
  if(giphy_file_contents == None and os.path.isfile('single_giphy_results.txt')):
    f = open('single_giphy_results.txt', 'r')
    giphy_file_contents = f.read().split('\n')
    f.close()
    del giphy_file_contents[-1]
    globals_file.giphy_file_cache = giphy_file_contents
  elif(giphy_file_contents == None and not os.path.isfile('single_giphy_results.txt')):
    f = open('single_giphy_results.txt', 'w')
    f.write(search_string + '\n')
    f.close()

  if(message.content.lower() == '!singleresults' and giphy_file_contents == []):
    if(os.path.isfile('single_giphy_results.txt')):
      with open('single_giphy_results.txt') as f:
        for line in f:
          if(len(single_results_string) + len(line.rstrip() + ', ') < 1950):
            single_results_string = single_results_string + line.rstrip() + ', '
            single_results_count += 1
          else:
            single_results_array.append(single_results_string)
            single_results_string = '' + line.rstrip() + ', '
            single_results_count += 1
        single_results_array.append(single_results_string)
      await print_results(client, message, single_results_array, single_results_count)
    else:
      await send_message(client, message, "There are no single results yet")
  elif(message.content.lower() == '!singleresults' and giphy_file_contents != []):
    for result in giphy_file_contents:
      if(len(single_results_string) + len(result.rstrip() + ', ') < 1950):
        single_results_string = single_results_string + result.rstrip() + ', '
        single_results_count += 1
      else:
        single_results_array.append(single_results_string)
        single_results_string = '' + result.rstrip() + ', '
        single_results_count += 1
    single_results_array.append(single_results_string)
    await print_results(client, message, single_results_array, single_results_count)
  elif(message.content.lower() == '!singleresults count' and giphy_file_contents != ''):
    await send_message(client, message, "There have been %d single results so far" % len(giphy_file_contents))
  elif(message.content.lower() == '!singleresults count' and giphy_file_contents == ''):
    if(os.path.isfile('single_giphy_results.txt')):
      with open('single_giphy_results.txt') as f:
        for line in f:
          single_results_count += 1
      await send_message(client, message, "There have been %d single results so far" % single_results_count)
    else:
      await send_message(client, message, "There are no single results yet")
  else:
    print('oops')

TRIGGER = '!singleresults'