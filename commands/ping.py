from datetime import datetime

from client_interactions import send_message

"""
Ping Command
Returns the ping between message sent time and message processed time
ex: !ping

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@result: Send a message always
"""
async def command(client, message):
  d = datetime.utcnow() - message.timestamp
  s = d.seconds*1000 + d.microseconds//1000
  response = 'Ping: %sms' % str(s)
  await send_message(client, message, response)


# String that triggers this command
TRIGGER = '!ping'

def is_triggered(message_content):
  return message_content.lower() == TRIGGER