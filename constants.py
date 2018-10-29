import os


BOT_ID = str(os.environ.get('BOT_ID'))
SLACK_BOT_TOKEN = str(os.environ.get('SLACK_BOT_TOKEN'))
AT_BOT = "<@" + BOT_ID + ">"

# Commands
SLACKBOT_SILENCE_COMMAND = 'shh'
