from datetime import datetime

import globals_file
from client_interactions import delete_message, send_message

"""
Set lunch command
Sets the lunch time for the current day

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@param other_args: Whatever other args that are passed into this template
@result: sends a message on...
@result: deletes a message on...
@result: adds a react on....
"""
async def command(client, message):
  await delete_message(message)
  message_content = message.content
  if(not len(message_content.split(' ')) == 2):
    return await error_response(client, message)
  
  new_time = message_content.split(' ')[1]
  if(not len(new_time.split(':')) == 2):
    return await error_response(client, message)
  
  new_hour = new_time.split(':')[0]
  new_minute = new_time.split(':')[1]
  if(not new_hour.isnumeric() or not new_minute.isnumeric()):
    return await error_response(client, message)
  
  new_hour = int(new_hour)
  new_minute = int(new_minute)
  if(new_hour > 23 or new_hour < 0 or new_minute > 59 or new_minute < 0):
    return await error_response(client, message)
  
  now = datetime.now()
  globals_file.lunch_time['today'] = datetime(now.year, now.month, now.day, new_hour, new_minute)
  response_message = "Lunch time has been set to %s" % globals_file.lunch_time['today'].strftime("%Y-%m-%d %H:%M")
  await send_message(message, response_message)

async def error_response(client, message):
  response_message = 'Format should be `!setlunch HH:MM` where HH is 00-23 and MM is 00-59'
  await send_message(message, response_message, True)
  return
# String that triggers this command
TRIGGER = '!setlunch '

def is_triggered(message_content):
  return message_content.lower().startswith(TRIGGER)