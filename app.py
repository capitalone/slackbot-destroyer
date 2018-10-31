#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import requests
import random
import boto3
import json
import io
from slackclient import SlackClient
from constants import *

slack_client = SlackClient(SLACK_BOT_TOKEN)
s3 = boto3.resource('s3')
global_store = None

def handle_command(command, channel):
    """
        Handles any generic command that is pointed
        towards the bot.
    """
    
    if channel not in global_store['destroy'].keys():
        # If the bot is being used in a new channel we store a new dictionary entry for it.
        global_store['destroy'][channel] = False

    if command.startswith(HELP_COMMAND):
        # Displays a list of available commands.
        return send_attachment_message(
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

    if command.startswith(TOGGLE_DESTROY_COMMAND):
        if global_store['destroy'][channel] == True:
            return send_basic_message('`A L R E A D Y  D E S T R O Y I N G` :robot_face:', channel)

        global_store['destroy'][channel] = True
        return send_basic_message('`D E S T R O Y` :robot_face:', channel)

    if command.startswith(TOGGLE_DEACTIVATE_COMMAND):
        if global_store['destroy'][channel] == False:
            return send_basic_message('`S T A N D I N G  B Y` :robot_face:', channel)

        global_store['destroy'][channel] = False
        return send_basic_message('`D E A C T I V A T E` :robot_face:', channel)

    if command.startswith(TELEPORT_COMMAND):
        # Returns a random robot inspired videos.
        return send_basic_message(random.choice(TELEPORT_VIDEOS), channel)

    if command.startswith(STATS_COMMAND):
        return send_basic_message('`I  H A V E  D E S T R O Y E D  %s  M E S S A G E  F R O M  S L A C K B O T` :robot_face:' % global_store['deletions'], channel)

    if command.startswith(S3_COMMAND):
        return handle_s3()


def handle_s3():
    bucket = s3.Bucket(AWS_BUCKET_NAME)
    print(bucket.name)
    for key in bucket.objects.all():
        print(key.key)
    print(AWS_BUCKET_NAME)
    print(CONFIG_FILE)
    to_put = s3.Object(AWS_BUCKET_NAME, CONFIG_FILE)
    to_put.put(Body=json.dumps(global_store))

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
        'token': SLACK_USER_TOKEN,
        'channel': channel,
        'ts': timestamp,
        'as_user': True
    }

    try:
        requests.post('https://slack.com/api/chat.delete', params=options)
    
    except requests.exceptions.RequestException as error:
        print(error)

    global_store['deletions'] += 1


def get_channel_list():
    """ Gets a list of channels using the Slack Web API """

    options = {
        'token': SLACK_USER_TOKEN,
    }

    try:
        request = requests.get('https://slack.com/api/channels.list', params=options)
        request.raise_for_status()
        request_json = request.json()

    except requests.exceptions.RequestException as error:
        request_json = {}
        print(error)

    return request_json


def remove_from_channel(id, channel):
    """ Removes a user from a channel, primarily used to remove the bot from
        non whitelisted channels """

    options = {
        'token': SLACK_USER_TOKEN,
        'user': id,
        'channel': channel
    }

    try:
        requests.post('https://slack.com/api/channels.kick', params=options)
    
    except requests.exceptions.RequestException as error:
        print(error)
    

def parse_slack_output(slack_rtm_output):
    """
        Returns None unless a message is directed at the bot
        based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:

            # If the channel name is not found in the whitelist, the bot removes its self.
            # This functionality requires the channels:read and channels:write permissions.
            if 'type' in output.keys() and output['type'] == 'channel_joined' and CHANNEL_WHITELIST is not None:
                channel_white_list = CHANNEL_WHITELIST.strip().split(',')
                channel_list = get_channel_list()

                if 'channels' in channel_list.keys():
                    for channel in channel_list['channels']:
                        if channel['name'] not in channel_white_list:
                            remove_from_channel(BOT_ID, channel['id'])

            # Handles message types
            if 'type' in output.keys() and output['type'] == 'message':
                if 'channel' in output.keys() and output['channel'] in global_store['destroy'].keys() and global_store['destroy'][output['channel']] == True:
                    if 'subtype' in output.keys() and output['subtype'] == 'slackbot_response':
                        delete_message(output['ts'], output['channel'])

                if output and 'text' in output and AT_BOT in output['text']:
                    # Return text after the @ mention, whitespace removed
                    return output['text'].split(AT_BOT)[1].strip(), \
                        output['channel']
    return None, None


def load_config():
    global global_store
    if len(AWS_ACCESS_KEY_ID) > 0 and len(AWS_SECRET_ACCESS_KEY) > 0:
        bucket = s3.Bucket(AWS_BUCKET_NAME)
        for obj in bucket.objects.all():
            if obj.key == CONFIG_FILE:
                config_bytes = io.BytesIO()
                bucket.download_fileobj(CONFIG_FILE, config_bytes)
                global_store = json.loads(config_bytes.getvalue())
                return
    # If it can't find config file in the bucket OR it doesn't have AWS configured
    with open('config.json') as json_data:
        global_store = json.load(json_data)


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print('Connected to RTM')
        load_config()
        print(global_store)
        print('Launch successful, waiting for input...')

        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. This is likely due to an invalid Slack token or Bot ID.")
