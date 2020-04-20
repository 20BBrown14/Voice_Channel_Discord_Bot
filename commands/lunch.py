from datetime import datetime, timedelta
import random

import globals_file
from client_interactions import send_message, delete_message


"""
Lunch Command
Lets the users know when lunch is and how close it is to the set lunch time

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@result: Sends a message always
@result: Deletes the triggering message always
"""
async def command(client, message):
  await delete_message(message)
  gif_searches = ['/excited', '/hell yes', '/I\'m ready', '/Let\'s do this', '/Leggo', '/Lunch time']
  now = datetime.now()

  if(globals_file.lunch_time['today'].day != now.day):
    globals_file.lunch_time = datetime(now.year, now.month, now.day, int(globals_file.lunch_time['default'].split(':')[0]), int(globals_file.lunch_time['default'].split(':')[1]))

  thirty_minutes_before = globals_file.lunch_time['today'] - timedelta(minutes=30)
  ten_minutes_before = globals_file.lunch_time['today'] - timedelta(minutes=10)
  lunch_time_grace = timedelta(seconds=45)
  
  
  if((now == globals_file.lunch_time['today']) or (now > globals_file.lunch_time['today'] and now < globals_file.lunch_time['today'] + lunch_time_grace)):
    response_message = 'You bet! It\'s lunch time!'
    await send_message(message, response_message)
  elif(now < thirty_minutes_before):
    response_message = 'Not lunch time yet. Lunch is at %s' % globals_file.lunch_time['today'].strftime("%H:%M")
    await send_message(message, response_message)
  elif(now > thirty_minutes_before and now < ten_minutes_before):
    response_message = 'Almost there! Only %s to go!' % ':'.join(str(globals_file.lunch_time['today'] - now).split('.')[0].split(':')[1:])
    await send_message(message, response_message)
  elif((now > ten_minutes_before and now < globals_file.lunch_time['today'])):
    response_message = 'Woot woot! Basically there! I\'m so excited, how about you?'
    response_gif = gif_searches[random.randint(0, len(gif_searches)-1)]
    await send_message(message, response_message)
    await send_message(message, response_gif)
  elif(now > globals_file.lunch_time['today'] + lunch_time_grace):
    response_message = 'Whoa there buckaroo. You\'ve already had lunch today. Step off.'
    await send_message(message, response_message)

# String that triggers this command
TRIGGER_MESSAGES = ['!lunch', '!lunchtime']

def is_triggered(message_content):
  return message_content.lower() in TRIGGER_MESSAGES