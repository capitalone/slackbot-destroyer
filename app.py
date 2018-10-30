#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import requests
import random
from slackclient import SlackClient
from constants import *
from util import *

slack_client = SlackClient(SLACK_BOT_TOKEN)

def handle_command(command, channel):
    """
        Handles any generic command that is pointed
        towards the bot.
    """
    if command.startswith(HELP_COMMAND):
        # Displays a list of available commands.
        send_attachment_message(
        {
            'fallback': 'Available Commands',
            'color': '#150650',
            'title': 'A v a i l a b l e  C o m m a n d s',
            'title_link': 'http://unitedincome.com',
            'text': '',
            "fields": [
                {
                    "title": "`destroy`",
                    "value": "`Deletes all incoming messages from Slackbot.`",
                    "short": True
                },
                {
                    "title": "`stats`",
                    "value": "`Shows how many messages from Slackbot that have been deleted.`",
                    "short": True
                },
                {
                    "title": "`commands`",
                    "value": "`Displays a list of available commands.`",
                    "short": True
                },
                {
                    "title": "`teleport`",
                    "value": "`Teleport to the future.`",
                    "short": True
                }
            ],
        } 
        , channel)

    if command.startswith(TOGGLE_ATTACK_COMMAND):
        global_store['destroy'] = not global_store['destroy']
        
        if global_store['destroy'] == True:
            send_basic_message('`D E S T R O Y` :robot_face:', channel)

        if global_store['destroy'] == False:
            send_basic_message('`D E A C T I V A T E` :robot_face:', channel)

    if command.startswith(TELEPORT_COMMAND):
        # Returns a random robot inspired videos.
        send_basic_message(random.choice(TELEPORT_VIDEOS), channel)

    if command.startswith(STATS_COMMAND):
        send_basic_message('`I  H A V E  D E S T R O Y E D  %s  M E S S A G E  F R O M  S L A C K B O T` :robot_face:' % global_store['deletions'], channel)


def send_basic_message(message, channel):
    """ Sends a basic message with the Slack API """
    slack_client.api_call("chat.postMessage", channel=channel,
                    text=message, as_user=True)


def send_attachment_message(attachment, channel):
    """
        Sends an attachment message to Slack. The payload argument
        should be a JSON object containing the following keys.

        {
            'fallback': 'Fallback text',
            'color': '#fff',
            'title': 'Title text',
            'title_link': 'http://unitedincome.com',
            'text': 'Text',
            'fields': []
        }
    """

    ts = int(time.time())

    payload = [
        {
            'fallback': attachment['fallback'],
            'color': attachment['color'],
            'title': attachment['title'],
            'title_link': "%s" % (attachment['title_link']),
            'text': attachment['text'],
            'ts': ts,
            'fields': attachment['fields'],
            'footer': 'https://github.com/UnitedIncome/slackbot-destroyer',
            'image_url': 'https://i.imgur.com/22XLQna.jpg',
            'footer_icon': 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/google/146/robot-face_1f916.png',
        }
    ]

    slack_client.api_call("chat.postMessage", channel=channel,
                attachments=payload, as_user=True)


def delete_message(timestamp, channel):
    """ Deletes a message using the Slack Web API """
    options = {
        'token': SLACK_BOT_ACCESS_TOKEN,
        'channel': channel,
        'ts': timestamp,
        'as_user': True
    }
    requests.post('https://slack.com/api/chat.delete', params=options)

    global_store['deletions'] += 1


def parse_slack_output(slack_rtm_output):
    """
        Returns None unless a message is directed at the bot
        based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:

            if global_store['destroy'] == True and output and 'subtype' in output.keys():
                if output['subtype'] == 'slackbot_response':
                    delete_message(output['ts'], output['channel'])

            if output and 'text' in output and AT_BOT in output['text']:
                # Return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip(), \
                    output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print('Launch successful, waiting for input...')

        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. This is likely due to an invalid Slack token or Bot ID.")
