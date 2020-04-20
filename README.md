# Voice_Channel_Discord_Bot
This bot announces who leaves and enters a voice channel it is a part of along with a few other commands.

Be sure to read in-line comments to make everything work. README update to come soon.

## Setup
Python 3.5 or greater required

Install modules as defined in requirements.txt
`pip install -r requirements.txt`

You'll need to create a bot for the discord API. You'll get a secret token. Be sure to add that in [python_bot.py L232](https://github.com/20BBrown14/Voice_Channel_Discord_Bot/blob/master/python_bot.py#L232) in place of `TOKEN`

Follow the discord provided instructions on how to setup a bot on your discord server.

Follow instructions on how to install discord.py for your operating system

Follow instructions on how to install python for your operating system

### Config File

You will need to setup a config.py file. A template is provided: [TEMPLATE_config](#TEMPLATE_config.py)
See TEMPLATE_config.py for more documentation on nested keys for dictionaries.
Each optional config option is required for the corresponding functionality.

| Option | Description | Required |
| ------ | ----------- | -------- |
| bot_token | String the discord bots token | :white_check_mark: |
| giphy_api_key | String the giphy apo key. Required for giphy search functionality | :x: |
| weather_api_key | String the weather api key. Required for weather functionality | :x: |
| dictionary_api | String the dictionary api key. Required for dictionary functionality. | :x: |
| logs_config | Dictionary logs configuration | :x: |
| game_played_config | Dictionary config for game played | :x: |
| mention_reactions_config | Dictionary config for auto add reactions on mentions | :x: |
| timecard_reminder_config | Dictionary config for timecard reminder functionality | :x: |
| count_config | Dictionary config for count channel | :x: |
| lunch_config | Dictionary config for lunch time tracking | :x: |

### Running on Windows
Win + R

type 'cmd'

hit enter

cd into the directory with python_bot.py

run `[Path to python.exe] python_bot.py`

### Running on Mac
Command + Space

type 'terminal'

hit enter

cd into the directory with python_bot.pt

run `python python_bot.py`

## Notes
You will have to keep the terminal/cmd window running while you want the bot running. This bot will not run if your computer is asleep, hibernating, or turned off. You will need to host it on a seperate server with a 100% uptime. It is possible to set the bot to turn on when you turn your computer on. You'll have to look up that information yourself.
