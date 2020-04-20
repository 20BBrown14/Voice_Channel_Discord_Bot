import globals_file
from client_interactions import delete_message

"""
Count Audit
Audits the count channel so only the next number can be sent otherwise deletes whatever was sent

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@result: Deletes a message if it's not the next number or on error
"""

async def apply(client, message):
  try:
    oldCount = -1
    newCount = -1
    first = True
    async for serverMessage in message.channel.history(limit=2):
      if(first):
        newCount = int(serverMessage.content)
        first = False
        continue
      oldCount = int(serverMessage.content)
      if(newCount != oldCount + 1):
        await delete_message(message)
  except:
    await delete_message(message)

def is_triggered(message):
  return message.channel == globals_file.count_config['count_channel']
  