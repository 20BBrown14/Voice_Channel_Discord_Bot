from discord.utils import get

async def send_message(message, message_to_send, force_author = False):
  try:
    message_destination = determine_destination(message, force_author)
    await message_destination.send(message_to_send)
  except:
    print('Failed to send message')

async def delete_message(message):
  try:
    await message.channel.fetch_message(message.id)
    if(message.channel.name):
      if(not message.channel.name.lower() == 'bot_commands'):
        await message.delete()
  except:
    print('Message DNE')

async def purge_from(client, message, amount, check, force_author = False):
  message_destination = determine_destination(message, force_author)
  await message_destination.purge(limit = amount, check=check)

async def add_reaction(client, message, emoji):
  try:
    await message.add_reaction(emoji)
  except:
    return

def get_emoji(client, message, emoji_name):
  return get(client.emojis, name=emoji_name)

def determine_destination(message, force_author):
  return message.channel if message.channel.name and not force_author else message.author
  