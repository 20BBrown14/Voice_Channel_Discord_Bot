import random

from client_interactions import send_message

"""
Auto triggerd messages without explicit consent of the user
Sends a response message based on the message contents.

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@result: Sends a message if one of the trigger messages is present
"""

async def apply(client, message):
  content = message.content.lower()
  if(content == 'foos?'):
    foos_response_array = ['when?', 'omw', 'Oh, so that\'s why you never have your stuff done.']
    await send_message(message, foos_response_array[random.randint(0,len(foos_response_array)-1)])
  elif(content == 'ope'):
    gottem_array = ['gottem', 'gotem', 'gotm', 'gottum', 'gottm', 'gotm', 'gotim', 'gottim', 'oof', 'gotus', 'gottus', '**OOF**', '***OOF***']
    await send_message(message, gottem_array[random.randint(0,len(gottem_array)-1)])
  elif(content == 'oof'):
    oof_array = ['**BIG OOF**','you dun goofed', 'Pay some respect, send an F', 'oh snap','_nice job_','Can we get an F in chat?', 'Press F'];
    await send_message(message, oof_array[random.randint(0,len(oof_array)-1)])
  elif(content == 'lol'):
    await send_message(message, 'lo\nlo\nlol')
  elif(content.startswith('i\'m ')):
    if(' ' not in message.content[4:]):
      response_message = 'Hi %s, I\'m Roboto.' % (message.content[4:])
      await send_message(message, response_message)

TRIGGER_MESSAGES = ['foos?', 'ope', 'oof', 'lol']
DAD_TRIGGER = 'I\'m '

def is_triggered(message_content):
  # determine if this command will be triggered
  return message_content.lower() in TRIGGER_MESSAGES or message_content.startswith(DAD_TRIGGER)