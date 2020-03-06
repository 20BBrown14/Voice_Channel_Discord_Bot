from datetime import datetime

import globals_file
from client_interactions import send_message

"""
Timecard Reminder
Reminds people in the chat to submit their time cards on Fridays

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@result: Sends a message if a reminder is needed to be sent
"""

async def apply(client, message):
  now = datetime.now()
  current_hour = now.hour
  today_day = now.weekday()
  if(today_day != 4):
    globals_file.time_card_reminder = 12
    return
  else:
    fivepm = datetime(now.year, now.month, now.day, 17, 00)
    response_message = '@everyone do not forget to submit your time sheets! Only %s until 5PM today.' % str(fivepm - now).split('.')[0]
    if(globals_file.time_card_reminder < current_hour and current_hour < 17):
      await send_message(client, message, response_message)
      globals_file.time_card_reminder = current_hour
    elif(globals_file.time_card_reminder == 16 and globals_file.time_card_reminder < 17 and now.hour == 16 and now.minute > 30):
      await send_message(client, message, response_message)
      globals_file.time_card_reminder = 17
      


