#globals.py
import json
from datetime import datetime

id_mark    = 547509875308232745

global player
global voice_client
global giphy_file_cache
global lunch_time
global timecard_reminder_config
global weather_cache
global logs_config
global game_played_config
global mention_reactions_config
global count_config

def init(client, config):
  # Update for each revision using format yyyy-mm-dd_#
  # where '#' is the release number for that day.
  # e.g. 2019-03-31_1 is the first release of March 31st, 2019
    global version 
    version = '2020-04-30_1'

    global player
    player = None

    global voice_client
    voice_client = None
    
    global giphy_file_cache
    giphy_file_cache = None

    global lunch_time
    if(config.lunch_config):
      now = datetime.now()
      lunch_time_config = config.lunch_config['lunch_time'].split(':')
      lunch_time = {
        "today": datetime(now.year, now.month, now.day, int(lunch_time_config[0]), int(lunch_time_config[1])),
        "default": config.lunch_config['lunch_time']
      }
    else:
      lunch_time = None

    global timecard_reminder_config
    if(config.timecard_reminder_config and config.timecard_reminder_config['use_reminder']):
      timecard_reminder_config = config.timecard_reminder_config
      timecard_reminder_config['next_hour_reminder'] = int(timecard_reminder_config['time_due'].split(':')[0]) - 5
    else:
      timecard_reminder_config = None

    global weather_cache
    weather_cache = json.loads('{}')

    global logs_config
    logs_config = config.logs_config
    if(config.logs_config and config.logs_config['use_logs'] and config.logs_config['logs_channel']):
      for guild in client.guilds:
        for channel in guild.channels:
          if channel.id == logs_config['logs_channel']:
            logs_config['logs_channel'] = channel
    else:
      logs_config = None

    global game_played_config
    game_played_config = config.game_played_config
    if(game_played_config):
      if(game_played_config['use_version']):
        game_played_config['game_played'] = "Version %s" % version
    else:
      game_played_config = None

    global mention_reactions_config
    if(config.mention_reactions_config and len(config.mention_reactions_config) > 0):
      mention_reactions_config = config.mention_reactions_config
    else:
      mention_reactions_config = None

    global count_config
    if(config.count_config):
      count_config = config.count_config
      for guild in client.guilds:
        for channel in guild.channels:
          if channel.id == count_config['count_channel']:
            count_config['count_channel'] = channel
    else:
      count_config = None
    
