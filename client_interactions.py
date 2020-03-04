from discord.utils import get

async def send_message(client, message, message_to_send, force_author = False):
  try:
    message_destination = determine_destination(message, force_author)
    await client.send_message(message_destination, message_to_send)
  except:
    print('Failed to send message')

async def delete_message(client, message):
  try:
    await client.get_message(message.channel, message.id)
    if(message.channel.name):
      if(not message.channel.name.lower() == 'bot_commands'):
        await client.delete_message(message)
  except:
    print('Message DNE')

async def purge_from(client, message, amount, check, force_author = False):
  message_destination = determine_destination(message, force_author)
  await client.purge_from(message_destination, limit = amount, check=check)

async def send_typing(client, message, force_author = False):
  message_destination = determine_destination(message, force_author)
  await client.send_typing(message_destination)

async def add_reaction(client, message, emoji):
  try:
    await client.add_reaction(message, emoji)
  except:
    print('Message DNE')

def get_emoji(client, message, emoji_name):
  return get(client.get_all_emojis(), name=emoji_name)

def determine_destination(message, force_author):
  return message.channel if message.channel.name and not force_author else message.author
  