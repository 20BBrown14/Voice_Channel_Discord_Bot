import globals_file
from client_interactions import add_reaction, get_emoji

"""
Pre add Reaction
Adds reactions to messages if certain conditions are met

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@result: Adds reactions to messages
"""


async def apply(client, message):
  mentions = message.mentions
  for i in mentions:
    if(i.id in globals_file.user_ids):
      emoji = get_emoji(client, message, globals_file.user_ids[i.id])
      await add_reaction(client, message, emoji)