from client_interactions import send_message, delete_message

"""
Reddit Link
Sends a reddit link if there is a shortened sub or user link
ex: /r/funny
ex: /u/gallowboob

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@result: Creates a reddit link from the triggering message content
"""

async def apply(client, message):
  await delete_message(message)
  reddit_link = 'https://www.reddit.com%s/' % message.content
  await send_message(message, reddit_link)

def is_triggered(message_content):
  # determine if this command will be triggered
  lowercase_message = message_content.lower()
  return not ' ' in lowercase_message and (lowercase_message.startswith('/r/') or lowercase_message.startswith('/u/'))