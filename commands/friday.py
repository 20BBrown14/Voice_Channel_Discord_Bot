import calendar
from datetime import datetime

from client_interactions import delete_message, send_message

"""
Friday command
Lets the user know if it's Friday or not

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@result: Sends a message always
@result: Deletes triggering message always
"""
async def command(client, message):
  await delete_message(client, message)
  weekday = datetime.today().weekday()
  calendarList = list(calendar.day_name)

  if(calendarList[weekday] != 'Friday'):
    response_message = "Lol sucks to be you sucka, It\'s only %s." % calendarList[weekday]
    await send_message(client, message, response_message)
  else:
    await send_message('Friday!')
    await send_message("/friday")


# String that triggers this command
TRIGGER = '!friday'

def is_triggered(message_content):
  return message_content.lower() == TRIGGER