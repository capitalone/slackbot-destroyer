import os

BOT_ID = os.environ.get('BOT_ID')
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_USER_TOKEN = os.environ.get('SLACK_USER_TOKEN')
CHANNEL_WHITELIST = os.environ.get('CHANNEL_WHITELIST')
AT_BOT = "<@" + BOT_ID + ">"

# Commands
TOGGLE_DESTROY_COMMAND = 'destroy'
TOGGLE_DEACTIVATE_COMMAND = 'deactivate'
HELP_COMMAND = 'commands'
STATS_COMMAND = 'stats'
TELEPORT_COMMAND = 'teleport'

# Teleport Command Videos
TELEPORT_VIDEOS = [
  'https://www.youtube.com/watch?v=2IPAOxrH7Ro',
  'https://www.youtube.com/watch?v=MEb2CecR11I',
  'https://www.youtube.com/watch?v=68ugkg9RePc'
]