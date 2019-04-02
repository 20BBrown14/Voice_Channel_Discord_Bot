# single_giphy_results_display.py

import os

async def command(client, message, channel, delete_message):
  single_results = []
  if(os.path.isfile('single_giphy_results.txt')):
    with open('single_giphy_results.txt') as f:
      for line in f:
        single_results.append(line.rstrip())
  else:
    await client.send_message(message.author, "There are no single results yet")

  if(len(single_results) > 0 ):
    await client.send_message(channel, "```\nNumber of results = %d\n%s```" % (len(single_results), ', '.join(single_results)))
  else:
    await client.send_message(message.author, "There are no single results yet")


TRIGGER = '!singleresults'