#weather.py

import requests
import json
import discord
import datetime
from uszipcode import SearchEngine
import pytz
import calendar

from custom_exceptions import zipcode_invalid_exception

def weather_help():
  weather_help_message="""
  Available Options:
    `!weather zip=#####`
    `!weather forecast zip=64063`"""
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

def create_forecast_embeded(title, description, first_day_times, first_day_temps, first_day_conditions, first_day_humidity, average_temps, weather_conditions, average_humidity):
  calendarList = list(calendar.day_name)
  next_days = []
  first_day = datetime.datetime.fromtimestamp(first_day_times[0])
  for i in range(0, 4):
    first_day = first_day + datetime.timedelta(days=1)
    next_days.append(first_day)
  embed=discord.Embed(title="%s's Weather" % title, description="%s" % description, color=0x00f900)
  for i in range(0, len(first_day_times)):
      date = datetime.datetime.fromtimestamp(first_day_times[i])
      embed.add_field(name="%s, %s" % (date, calendarList[date.weekday()]), value="%s | %s | %s%% humidity" % (first_day_conditions[i], kelvin_to_C_and_F_string(first_day_temps[i]), first_day_humidity[i]), inline=False)
  embed.add_field(name="%s, %s" % (next_days[0].strftime("%Y-%m-%d"), calendarList[next_days[0].weekday()]), value="%s | %s | %s%% humidity" % (weather_conditions[0], kelvin_to_C_and_F_string(average_temps[0]), round(average_humidity[0], 2)), inline=False)
  embed.add_field(name="%s, %s" % (next_days[1].strftime("%Y-%m-%d"), calendarList[next_days[1].weekday()]), value="%s | %s | %s%% humidity" % (weather_conditions[1], kelvin_to_C_and_F_string(average_temps[1]), round(average_humidity[1], 2)), inline=False)
  embed.add_field(name="%s, %s" % (next_days[2].strftime("%Y-%m-%d"), calendarList[next_days[2].weekday()]), value="%s | %s | %s%% humidity" % (weather_conditions[2], kelvin_to_C_and_F_string(average_temps[2]), round(average_humidity[2], 2)), inline=False)
  embed.add_field(name="%s, %s" % (next_days[3].strftime("%Y-%m-%d"), calendarList[next_days[3].weekday()]), value="%s | %s | %s%% humidity" % (weather_conditions[3], kelvin_to_C_and_F_string(average_temps[3]), round(average_humidity[3], 2)), inline=False)
  return embed

def find_zip_info(zipcode):
  search = SearchEngine(simple_zipcode=True)
  zipcode_info = search.by_zipcode(zipcode)
  if(zipcode_info.zipcode == None):
    raise zipcode_invalid_exception
  return zipcode_info.major_city, zipcode_info.state, zipcode_info.timezone

def update_cache(option, zipcode, item, weather_cache):
  if(option == 'forecast'):
    if(not 'forecast' in weather_cache):
      weather_cache['forecast'] = json.loads('{}')
    now = datetime.datetime.now().timestamp()
    item['cached_time'] = now
    weather_cache['forecast'][zipcode] = item
    return weather_cache

  if(option == ''):
    now = datetime.datetime.now().timestamp()
    item['cached_time'] = now
    weather_cache[zipcode] = item
    return weather_cache

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
  arguments = message_content.split(' ')
  if(arguments[0].strip().lower() == 'forecast'): #check if user wants 5 day forecast
    weather_options = message.content[18:]
    equals_index = weather_options.find('=')
    if(equals_index < 0): #check if user provided zipcode
      if(message_content.strip() == 'help'): #check if user is invoking weather help
        await client.send_message(message.author, "%s" % weather_help())
        return weather_cache
      await client.send_message(message.author, "Please ensure you're using one of the following options:\n%s" % weather_help())
      return weather_cache
    if(weather_options[:equals_index].strip().lower() == 'zip'): #check if user provided zip
      zipcode = weather_options[equals_index+1:].strip()
      city, state, time = None, None, None
      try:
        city, state, timezone = find_zip_info(zipcode)
      except zipcode_invalid_exception: #Catch invalid zip code errors
        await client.send_message(message.author, "Zipcode (%s) invalid. Only US zip codes are supported." % zipcode)
        return weather_cache
      try:
        timezone = pytz.timezone('US/%s' % timezone)
      except pytz.exceptions.UnknownTimeZoneError: #unknown timezone error
        await client.send_message(message.author, "Zipcode (%s) is in timezone %s and is not supported or invalid. Contact bot developer if you think this is in error." % zipcode, timezone)
        return weather_cache

      await client.send_message(message.channel, "%s %s %s" % (city, state, timezone))

      now = datetime.datetime.now().timestamp()
      weather_data = None
      if('forecast' in weather_cache and zipcode in weather_cache['forecast'] and now - weather_cache['forecast'][zipcode]['cached_time'] < 600): #check if forecast exists in cache and is still valid
        weather_data = weather_cache['forecast'][zipcode]
      else:
        url = "http://api.openweathermap.org/data/2.5/forecast?zip=%s&APPID=%s" % (zipcode, weather_api_key)
        response = requests.get(url).text
        weather_data = json.loads(response)
        weather_cache = update_cache('forecast', zipcode, weather_data, weather_cache)
      
      first_forecast_time = None
      average_temps = [0, 0, 0, 0]
      weather_condition = ['', '', '', '']
      humidity_average = [0, 0, 0, 0]
      first_day_times = []
      first_day_temps = []
      first_day_conditions = []
      first_day_humidity = []
      if('cod' in weather_data and weather_data['cod'] == '200'):
        now = datetime.datetime.now().timestamp()
        if('list' in weather_data):
          if(len(weather_data['list']) > 0):
            first_forecast_time = weather_data['list'][0]['dt']
          else:
            await client.send_message(message.author, "Something went wrong gathering data. Please try again later.")
            return weather_cache
          for forecast in weather_data['list']:
            if('dt' in forecast):
              if(forecast['dt'] < first_forecast_time + ( 60*60*24)): # first 24 hours of forecast
                first_day_times.append(forecast['dt'])
                first_day_temps.append(forecast['main']['temp'])
                first_day_conditions.append(forecast['weather'][0]['description'])
                first_day_humidity.append(forecast['main']['humidity'])
              elif(forecast['dt'] < first_forecast_time + (60 * 60 * 24 * 2)): #second 24 hours of forecast
                average_temps[0] = (average_temps[0] + forecast['main']['temp']) / 2 if average_temps[0] != 0 else forecast['main']['temp']
                if(forecast['weather'][0]['main'] == 'Rain' or forecast['weather'][0]['main'] == 'Snow'):
                  weather_condition[0] = forecast['weather'][0]['description']
                elif(weather_condition[0] == ''):
                  weather_condition[0] = forecast['weather'][0]['description']
                humidity_average[0] = (humidity_average[0] + forecast['main']['humidity']) / 2 if humidity_average[0] != 0 else forecast['main']['humidity']
              elif(forecast['dt'] < first_forecast_time + (60 * 60 * 24 * 3)): #third 24 hours of forecast
                average_temps[1] = (average_temps[1] + forecast['main']['temp']) / 2 if average_temps[1] != 0 else forecast['main']['temp']
                if(forecast['weather'][0]['main'] == 'Rain' or forecast['weather'][0]['main'] == 'Snow'):
                  weather_condition[1] = forecast['weather'][0]['description']
                elif(weather_condition[1] == ''):
                  weather_condition[1] = forecast['weather'][0]['description']
                humidity_average[1] = (humidity_average[1] + forecast['main']['humidity']) / 2 if humidity_average[1] != 0 else forecast['main']['humidity']
              elif(forecast['dt'] < first_forecast_time + (60 * 60 * 24 * 4)): #fourth 24 hour of forecast
                average_temps[2] = (average_temps[2] + forecast['main']['temp']) / 2 if average_temps[2] != 0 else forecast['main']['temp']
                if(forecast['weather'][0]['main'] == 'Rain' or forecast['weather'][0]['main'] == 'Snow'):
                  weather_condition[2] = forecast['weather'][0]['description']
                elif(weather_condition[2] == ''):
                  weather_condition[2] = forecast['weather'][0]['description']
                humidity_average[2] = (humidity_average[2] + forecast['main']['humidity']) / 2 if humidity_average[2] != 0 else forecast['main']['humidity']
              elif(forecast['dt'] < first_forecast_time + (60 * 60 * 24 * 5)): #fifth 24 hour of forecast
                average_temps[3] = (average_temps[3] + forecast['main']['temp']) / 2 if average_temps[3] != 0 else forecast['main']['temp']
                if(forecast['weather'][0]['main'] == 'Rain' or forecast['weather'][0]['main'] == 'Snow'):
                  weather_condition[3] = forecast['weather'][0]['description']
                elif(weather_condition[3] == ''):
                  weather_condition[3] = forecast['weather'][0]['description']
                humidity_average[3] = (humidity_average[3] + forecast['main']['humidity']) / 2 if humidity_average[3] != 0 else forecast['main']['humidity']

            else:
              await client.send_message(message.author, 'Something went wrong. Sorry about that. Please try again later.')
              return weather_cache
          #create embeded
          embeded = create_forecast_embeded(zipcode,\
                                  "All times in zipcode's local time zone", \
                                  first_day_times, \
                                  first_day_temps, \
                                  first_day_conditions, \
                                  first_day_humidity, \
                                  average_temps, \
                                  weather_condition, \
                                  humidity_average, \
                                  )
          await client.send_message(channel, embed=embeded)
          return weather_cache
        else:
          await client.send_message(message.author, 'Something went wrong. Sorry about that. Please try again later.')
          return weather_cache
      else:
        await client.send_message(message.author, weather_data['message'])
        return weather_cache

  
  elif( 'zip' in arguments[0].strip().lower()):
    equals_index = message_content.find('=')
    if(equals_index < 0): #option not provided
      if(message_content.strip() == 'help'): #weather help command invoked
        await client.send_message(message.author, "%s" % weather_help())
        return weather_cache
      await client.send_message(message.author, "Please ensure you're using one of the following options:\n%s" % weather_help())
      return weather_cache
      
    if(message_content[:equals_index].strip().lower() == 'zip'):
      zipcode = message_content[equals_index+1:].strip()
      now = datetime.datetime.now().timestamp()
      weather_data = None
      if(zipcode in weather_cache and now - weather_cache[zipcode]['cached_time'] < 600):
        weather_data = weather_cache[zipcode]
      else:
        url = "http://api.openweathermap.org/data/2.5/weather?zip=%s&APPID=%s" % (zipcode, weather_api_key)
        response = requests.get(url).text
        weather_data = json.loads(response)
        weather_cache = update_cache('', zipcode, weather_data, weather_cache)
      if('cod' in weather_data and weather_data['cod'] == 200):
        weather = weather_data["weather"][0] if 'weather' in weather_data else []
        main = weather_data["main"] if 'main' in weather_data else []
        wind = weather_data["wind"] if 'wind' in weather_data else []
        rain = weather_data["rain"] if 'rain' in weather_data else []
        snow = weather_data["snow"] if 'snow' in weather_data else []
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
        return weather_cache
      else:
        await client.send_message(message.author, weather_data['message'])
  else:
    await client.send_message(message.author, "%s" % weather_help())

TRIGGER = '!weather'