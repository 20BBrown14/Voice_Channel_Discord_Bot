import requests
import json

from client_interactions import send_message, delete_message

"""
Ping Command
Returns covid information
ex: !covid

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@result: Send a message always
"""
async def command(client, message):
  await delete_message(message)
  argument = message.content[7:]
  if(argument == 'help'):
    message_to_send = "'!covid' prints World and US information. '!covid [country]' prints country specific information"
    await send_message(message, message_to_send, True)
  else:
    if(argument == ''):
      try:
        url = 'https://coronavirus-19-api.herokuapp.com/countries'
        data = json.loads(requests.get(url).text)
      except:
        message_to_send = "Something went wrong pulling data. Please try again later"
        await send_message(message, message_to_send, True)
        return 0
      world_cases = world_active = world_deaths = us_cases = us_active = us_deaths = 0
      if(data[0]['country'] == 'World'):
        world_cases = '{:,}'.format(data[0]['cases'] if data[0]['cases'] else 0)
        world_active = '{:,}'.format(data[0]['active'] if data[0]['active'] else 0)
        world_deaths = '{:,}'.format(data[0]['deaths'] if data[0]['deaths'] else 0)
      else:
        for country in data:
          if(country['country'] == 'World'):
            world_cases = '{:,}'.format(country['cases'] if country['cases'] else 0)
            world_active = '{:,}'.format(country['active'] if country['active'] else 0)
            world_deaths = '{:,}'.format(country['deaths'] if country['deaths'] else 0)
            break
      if(data[1]['country'] == 'USA'):
        us_cases = '{:,}'.format(data[1]['cases'] if data[1]['cases'] else 0)
        us_active = '{:,}'.format(data[1]['active'] if data[1]['active'] else 0)
        us_deaths = '{:,}'.format(data[1]['deaths'] if data[1]['deaths'] else 0)
      else:
        for country in data:
          us_cases = '{:,}'.format(country['cases'] if country['cases'] else 0)
          us_active = '{:,}'.format(country['active'] if country['active'] else 0)
          us_deaths = '{:,}'.format(country['deaths'] if country['deaths'] else 0)
          break
      message_to_send = "World Cases: %s\nWorld Active: %s\nWorld Deaths: %s\nUS Cases: %s\nUS Active: %s\nUS Deaths: %s" % (world_cases, world_active, world_deaths, us_cases, us_active, us_deaths)
      await send_message(message, message_to_send)
    else:
      try:
        url = 'https://coronavirus-19-api.herokuapp.com/countries/%s' % argument
        data = json.loads(requests.get(url).text)
      except:
        message_to_send = "Something went wrong pulling data. Please try again later."
        await send_message(message, message_to_send, True)
      country = data['country']
      cases = '{:,}'.format(data['cases'] if data['cases'] else 0)
      active = '{:,}'.format(data['active'] if data['active'] else 0)
      deaths = '{:,}'.format(data['deaths'] if data['deaths'] else 0)
      message_to_send = "Information for %s\nCases: %s\nActives: %s\nDeaths: %s" % (country, cases, active, deaths)
      await send_message(message, message_to_send)
    


# String that triggers this command
TRIGGER = '!covid'

def is_triggered(message_content):
  return message_content.lower().startswith(TRIGGER)