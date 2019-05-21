# single_giphy_results_display.py

import os

async def print_results(client, message, channel, single_results, count):
  await client.send_message(channel, "Number of results = %d" % (count))
  for string in single_results:
    if len(string) > 0:
      print(len(string))
      print(string)
      await client.send_message(channel, "```\n%s```" % string[:-2])

async def command(client, message, channel, delete_message, giphy_file_contents):
  single_results_array = []
  single_results_string = ''
  single_results_count = 0
  if(message.content.lower() == '!singleresults' and giphy_file_contents == ''):
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
      await print_results(client, message, channel, single_results_array, single_results_count)
    else:
      await client.send_message(message.author, "There are no single results yet")
  elif(message.content.lower() == '!singleresults' and giphy_file_contents != ''):
    for result in giphy_file_contents:
      if(len(single_results_string) + len(result.rstrip() + ', ') < 1950):
        single_results_string = single_results_string + result.rstrip() + ', '
        single_results_count += 1
      else:
        single_results_array.append(single_results_string)
        single_results_string = '' + result.rstrip() + ', '
        single_results_count += 1
    single_results_array.append(single_results_string)
    await print_results(client, message, channel, single_results_array, single_results_count)
  elif(message.content.lower() == '!singleresults count' and giphy_file_contents != ''):
    await client.send_message(channel, "There have been %d single results for far" % len(giphy_file_contents))
  elif(message.content.lower() == '!singleresults count' and giphy_file_contents == ''):
    if(os.path.isfile('single_giphy_results.txt')):
      with open('single_giphy_results.txt') as f:
        for line in f:
          single_results_count += 1
      await client.send_message(channel, "There have been %d single results so far" % single_results_count)
    else:
      await client.send_message(message.author, "There are no single results yet")
  else:
    print('oops')

TRIGGER = '!singleresults'