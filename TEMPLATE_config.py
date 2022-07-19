# config.py
# save a copy of this template file as config.py with your BOT TOKEN from discord app settings 
# and your Giphy api key, both are strings and so need to be in quotes

bot_token = "BOT_TOKEN"
giphy_api_key = "YOUR_GIPHY_API_KEY"
weather_api_key = "" # https://openweathermap.org/api
dictionary_api = "" # https://dictionaryapi.com/

# Set game status in user list
# play_game - Bool: Whether to play a game or not
# game_played - String: The game to play
# use_version - Bool: Whether to use version in place of a game. True overrides the other options.
game_played_config = {
  "play_game": False,
  "game_played": "",
  "use_version": False
}

# Config to log messages this bot sees to a discord channel
# Automatically ignores own messages and logs channel
# use_logs - Bool: Whether to use this config or not
# logs_channel - Int: The channel id to log messages to
# ignored_channels - Array(Int): Channels to ignore for logging
logs_config = {
  "use_logs": False,
  "logs_channel": 0,
  "ignored_channels": []
}

# Config to auto add reactions when a user is mentioned
# Array(Dictionaries)
# user_id - Int: Discord user id that is mentioned to add reaction for
# emoji_name - String: discord emoji name to be added as reaction
mention_reactions_config = [
  {
    "user_id": 0,
    "emoji_name": ""
  },
  {
    "user_id": 0,
    "emoji_name": ""
  }
]

# Config for timecard reminder
# use_reminder - Bool: Whether to use the reminder feature or not
# remind_day - String: Day to send reminder message
# time_due - String: Time the timecard is due. 24 hour format.
timecard_reminder_config = {
  "use_reminder": False,
  "remind_day": "Friday",
  "time_due": "17:00"
}

# Count channel config
# count_channel - Int: Channel id to audit counting
count_config = {
  "count_channel": 0
}

# Default lunch config
# lunch_time - String: Default lunch time in 24 hour format
lunch_config = {
  "lunch_time": "11:30"
}

turn_on_pc_config = {
  "allowed_servers": [123, 456],
  "allowed_channels": [123, 456],
  "allowed_users": [123, 456],
  "mac_to_wake": "FF:FF:FF:FF:FF"
}

finnhub_api_key = "abcdefghijklmnopqrstuvwxyz"
