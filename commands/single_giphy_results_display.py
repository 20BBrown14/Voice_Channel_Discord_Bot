# single_giphy_results_display.py

async def command(client, message, channel, delete_message):
  f = open('single_giphy_results.txt', 'r')
  file_contents = f.read()
  f.close()
  if(file_contents != ''):
    print(file_contents)
    await client.send_message(channel, "```\n%s```" % file_contents)
  else:
    await client.send_message(message.author, "There are no single results yet")

TRIGGER = '!singleresults'