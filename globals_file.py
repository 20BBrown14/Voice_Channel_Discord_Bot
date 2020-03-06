#globals.py
import json
from datetime import datetime

id_branden = '159785058381725696'
id_grant   = '314454492756180994'
id_kevin   = '122149736659681282'
id_mark    = '547509875308232745'
id_harold  = '451156129830141975'
id_dan     = '258024860360507413'

global player
global voice_client
global giphy_file_cache
global user_ids
global lunch_time
global time_card_reminder
global weather_cache

def init():
    global player
    player = None

    global voice_client
    voice_client = None
    
    global giphy_file_cache
    giphy_file_cache = None

    global user_ids
    user_ids = {
      id_branden: 'Branden',
      id_harold: 'Harold',
      id_grant: 'Grant',
      id_kevin: 'Kevin',
      id_mark: 'Mark',
      id_dan: 'Dan'
    }

    global lunch_time
    now = datetime.now()
    lunch_time = datetime(now.year, now.month, now.day, 11, 30)

    global time_card_reminder
    time_card_reminder = 11

    global weather_cache
    weather_cache = json.loads('{}')
