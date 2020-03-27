from datetime import datetime
from dateutil.relativedelta import relativedelta

from client_interactions import send_message, delete_message

"""
Mark Command
Determines how long it has been since Mark got first rekt at foosball and displays it

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@result: Send a message always
@result: Deletes the triggering message always
"""
async def command(client, message, mark_id):
  await delete_message(message)
  now = datetime.now()
  then = datetime(2019,2,18,8,30,0)
  rd = relativedelta(now,then)
  years = rd.years
  years = "%d year%s," % (years, '' if years <= 1 else 's') if years > 0 else ''
  months = rd.months
  months = "%d month%s," % (months, '' if months <= 1 else 's') if months > 0 else ''
  days = rd.days
  days = "%d day%s," % (days, '' if days <= 1 else 's') if days > 0 else ''
  hours = rd.hours
  hours = "%d hour%s," % (hours, '' if hours <= 1 else 's') if hours > 0 else ''
  minutes = rd.minutes
  minutes = "%d minute%s," % (minutes, '' if minutes <= 1 else 's') if minutes > 0 else ''
  seconds = rd.seconds
  display_and = 'and' if years or months or days or hours or minutes else ''
  reply = "There has been %s %s %s %s %s %s %d seconds since <@!%s> first got rekt at foosball" % (years, months, days, hours, minutes, display_and, seconds, mark_id)
  await send_message(message, reply)

# String that triggers this command
TRIGGER = '!Mark'

def is_triggered(message_content):
  return message_content == TRIGGER