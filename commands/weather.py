#weather.py

import requests
import json
import discord

def weather_help():
  weather_help_message="""
  Available Options:
    `!weather zip=#####`
    `!weather city=someCity`
    `!weather lat=###, lon=###`"""
  return weather_help_message

def degree_to_cardinal_direction(degree):
      arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
      val = int((degree/22.5)+.5)
      return arr[(val % 16)]

def meter_per_sec_to_mph(speed):
  mph = str(round(int(speed) * 2.237, 2))
  return ("%s m/s (%s mph)" % (speed, mph))


def kelvin_to_C_and_F_string(kelvin_temp):
  celcius = str(round(int(kelvin_temp) - 273.15, 1))
  fahrenheit = str(round((int(kelvin_temp) - 273.15) * (9/5) + 32, 1))
  return "%s°C (%s°F)" % (celcius, fahrenheit)

def mm_to_inches(rain_mm):
  inches = str(round(int(rain_mm) / 25.4, 5))
  return "%s mm (%s in)" % (rain_mm, inches)

def precip_string(precip):
  if('1h' in precip and '3h' in precip):
    return "%s in last 1 hour and %s in last 3 hour" % (mm_to_inches(precip['1h']), mm_to_inches(precip['3h']))
  elif('1h' in precip and not '3h' in precip):
    return "%s in last 1 hour" % (mm_to_inches(precip['1h']))
  elif('3h' in precip and not '1h' in precip):
    return "%s in last 3 hours" % (mm_to_inches(precip['3h']))
  else:
    return False

def create_embeded(title, description, icon, min_temp, max_temp, current_temp, humidity, wind_speed, wind_degrees, wind_direction, rain, snow):
  print(description)
  embed=discord.Embed(title="%s's Weather" % title, description="%s" % description, color=0x00f900)
  if(icon):
    embed.set_thumbnail(url="http://openweathermap.org/img/w/%s.png" % icon)
  if(min_temp):
    embed.add_field(name="Min Temp", value=min_temp, inline=True)
  if(max_temp):
    embed.add_field(name="Max Temp", value=max_temp, inline=True)
  if(current_temp):
    embed.add_field(name="Current Temp", value=current_temp, inline=True)
  if(humidity):
    embed.add_field(name="Humidity", value="%s%%" % (humidity), inline=True)
  if(wind_speed and wind_degrees and wind_direction):
    embed.add_field(name="Wind Speed", value="%s" % wind_speed, inline=True)
    embed.add_field(name="Wind Direction", value="%s° (%s)" % (wind_degrees, wind_direction), inline=True)
  if(rain):
    embed.add_field(name='Rain', value=rain, inline=True)
  if(snow):
    embed.add_field(name='Snow', value=snow, inline=True)
  return embed

"""
Weather command

@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@param channel: The channel to send the command response to
@param delete_message: Function to try to delete message
@param weather_cache: Cached weather objects
@param weather_api_key: Weather api key to hit weather api endpoint with
@result: Sends a message always
@result: Deletes messages always
@result: Hits weather api when needed to get weather information
"""
async def command(client, message, channel, delete_message, weather_cache, weather_api_key):
  await delete_message(client, message)

  message_content = message.content[9:]
  equals_index = message_content.find('=')

  if(equals_index < 0): #option not provided
    if(message_content.strip() == 'help'): #weather help command invoked
      weather_help(client, message, channel)
      await client.send_message(message.author, "%s" % weather_help())
      return
    await client.send_message(message.author, "Please ensure you're using one of the follow options:\n%s" % weather_help())
    return
    
  if(message_content[:equals_index].strip().lower() == 'zip'):
    zipcode = message_content[equals_index+1:].strip()
    url = "http://api.openweathermap.org/data/2.5/weather?zip=%s&APPID=%s" % (zipcode, weather_api_key)
    response = requests.get(url).text
    JSONResponse = json.loads(response)
    if(JSONResponse['cod'] == 200):
      weather = JSONResponse["weather"][0] if 'weather' in JSONResponse else []
      main = JSONResponse["main"] if 'main' in JSONResponse else []
      wind = JSONResponse["wind"] if 'wind' in JSONResponse else []
      rain = JSONResponse["rain"] if 'rain' in JSONResponse else []
      snow = JSONResponse["snow"] if 'snow' in JSONResponse else []
      weather_embeded = create_embeded(zipcode, \
                                      "%s / %s" % (weather['main'], weather['description']) if 'main' in weather and 'description' in weather else 'Weather', \
                                      weather["icon"] if 'icon' in weather else False, \
                                      kelvin_to_C_and_F_string(main["temp_min"]) if 'temp_min' in main else False, \
                                      kelvin_to_C_and_F_string(main["temp_max"]) if 'temp_max' in main else False, \
                                      kelvin_to_C_and_F_string(main["temp"]) if 'temp' in main else False, \
                                      main["humidity"] if 'humidity' in main else 'N/A', \
                                      meter_per_sec_to_mph(wind['speed']) if 'speed' in wind else False, \
                                      wind['deg'] if 'deg' in wind else False, \
                                      degree_to_cardinal_direction(wind['deg']) if 'deg' in wind else False, \
                                      precip_string(rain), \
                                      precip_string(snow) \
                                    )
      await client.send_message(channel, embed=weather_embeded)
    else:
      await client.send_message(message.author, JSONResponse['message'])

TRIGGER = '!weather'