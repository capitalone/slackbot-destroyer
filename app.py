#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from slackclient import SlackClient
from constants import *
from util import *

slack_client = SlackClient(SLACK_BOT_TOKEN)

def handle_command(command, channel):
    """
        Handles any generic command that is pointed
        towards the bot.
    """
    if command.startswith(SLACKBOT_SILENCE_COMMAND):
        # Returns a message if we ask Slackbot to silence
        send_basic_message('no', channel)

    if command.startswith(TOGGLE_ATTACK_COMMAND):
        global_settings['attack'] = not global_settings['attack']
        
        if global_settings['attack'] == True:
            send_basic_message('DESTROY', channel)

        if global_settings['attack'] == False:
            send_basic_message('DEACTIVATE', channel)

def delete_message(timestamp, channel):
    slack_client.api_call("chat.delete", channel=channel,
                          ts=timestamp, as_user=True)

def send_basic_message(message, channel):
    """ Sends a basic message with the Slack API """
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=message, as_user=True)

def parse_slack_output(slack_rtm_output):
    """
        Returns None unless a message is directed at the bot
        based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
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
