import os

BOT_ID = str(os.environ.get('BOT_ID'))
SLACK_BOT_TOKEN = str(os.environ.get('SLACK_BOT_TOKEN'))
SLACK_BOT_ACCESS_TOKEN = str(os.environ.get('SLACK_BOT_ACCESS_TOKEN'))
AT_BOT = "<@" + BOT_ID + ">"

# Commands
TOGGLE_ATTACK_COMMAND = 'destroy'
HELP_COMMAND = 'commands'
STATS_COMMAND = 'stats'
TELEPORT_COMMAND = 'teleport'

# Teleport Command Videos
TELEPORT_VIDEOS = [
  'https://www.youtube.com/watch?v=2IPAOxrH7Ro',
  'https://www.youtube.com/watch?v=MEb2CecR11I',
  'https://www.youtube.com/watch?v=68ugkg9RePc'
]