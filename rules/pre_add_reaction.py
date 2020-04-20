import globals_file
from client_interactions import add_reaction, get_emoji

"""
Pre add Reaction
Adds reactions to messages if certain conditions are met.
Config should be set in config.py

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@result: Adds reactions to messages
"""


async def apply(client, message):
  mentions = message.mentions
  for i in mentions:
    for options in globals_file.mention_reactions_config:
      if(i.id == options['user_id']):
        emoji = get_emoji(client, message, options['emoji_name'].lower())
        await add_reaction(client, message, emoji)

  