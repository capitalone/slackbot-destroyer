import os
from enum import Enum

BOT_ID = os.environ.get('BOT_ID')
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_USER_TOKEN = os.environ.get('SLACK_USER_TOKEN')
CHANNEL_WHITELIST = os.environ.get('CHANNEL_WHITELIST')
AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
CONFIG_FILE = 'config.json'
AT_BOT = "<@" + BOT_ID + ">"

# Commands
TOGGLE_DESTROY_COMMAND = 'destroy'
TOGGLE_DEACTIVATE_COMMAND = 'deactivate'
HELP_COMMAND = 'commands'
STATS_COMMAND = 'stats'
TELEPORT_COMMAND = 'teleport'
CYBER_COMMAND = 'what do cybermen do better than you'
MODERATE_COMMAND = 'moderate'
SHOW_STATE = 'wassup'
SHOW_RESPONSES = 'track'
CONFIGURE_RESPONSE = 'hunt'

# Teleport Command Videos
TELEPORT_VIDEOS = [
  'https://www.youtube.com/watch?v=2IPAOxrH7Ro',
  'https://www.youtube.com/watch?v=MEb2CecR11I',
  'https://www.youtube.com/watch?v=68ugkg9RePc'
]

State = Enum('State', 'DESTROYING MODERATING DEACTIVATED')
