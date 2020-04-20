from datetime import datetime

import globals_file
from client_interactions import send_message

"""
Timecard Reminder
Reminds people in the chat to submit their time cards on Fridays
Config should be set in config.py

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@result: Sends a message if a reminder is needed to be sent
"""

async def apply(client, message):
  now = datetime.now()
  current_hour = now.hour
  today_day = now.strftime("%A").lower()
  remind_time = globals_file.timecard_reminder_config['time_due'].split(':')
  remind_time = datetime(now.year, now.month, now.day, int(remind_time[0]), int(remind_time[1]))
  if(today_day != globals_file.timecard_reminder_config['remind_day'].lower()):
    globals_file.timecard_reminder_config['next_hour_reminder'] = remind_time.hour - 5
    return
  else:
    response_message = '@everyone do not forget to submit your time sheets! Only %s until %s today.' % (str(remind_time - now).split('.')[0], globals_file.timecard_reminder_config['time_due'])
    if(globals_file.timecard_reminder_config['next_hour_reminder'] < current_hour and current_hour < remind_time.hour):
      await send_message(message, response_message)
      globals_file.timecard_reminder_config['next_hour_reminder'] = current_hour
    elif(globals_file.timecard_reminder_config['next_hour_reminder'] == remind_time.hour - 1 and globals_file.timecard_reminder_config['next_hour_reminder'] < remind_time.hour and now.hour == remind_time.hour - 1 and now.minute > 30):
      await send_message(message, response_message)
      globals_file.timecard_reminder_config['next_hour_reminder'] = remind_time.hour
      


