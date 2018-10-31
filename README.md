# Slackbot Destroyer :mega: :x: 

This bot deletes auto responses from Slack's very own Slackbot. If you'd like to be rid of the responses in certain channels in your organization, you can employ the `Slackbot Destroyer` to fight on your behalf.

## Installation

1. Go to your [organization's Slack integration page](https://api.slack.com/apps) and create a **new application**. An organization admin will need to do this as this bot requires permissions to delete messages using the credentials of an admin user.
2. Add a [Bot user](https://api.slack.com/bot-users) to the app you created and give it a name. 
3. Click the button below and enter the required settings.

[![Deploy](assets/heroku_button.png)](https://heroku.com/deploy?template=https://github.com/UnitedIncome/slackbot-destroyer/master)

If you'd like to run the application manually you can add the required secrets within [constants.py](constants.py) as environment variables and then run `$ python app.py`.

### Configuration

The installation button will require you to enter a number of API keys. Below you'll find an explanation 

| Key  | Value Information | Required |
| ------------- | ------------- | ------------- |
| `BOT_ID`  | The ID of your Slack bot user, this is required so the bot knows when a command is directed at it. If you're unsure what your bot ID is you can run `id.py` which will print the ID, you'll need to make sure that the `BOT_NAME` environment variable corresponds with the one you setup in the Slack interface.  | **Yes** |
| `SLACK_BOT_TOKEN`  | The bot token found within the [Slack API settings](https://api.slack.com/bot-users).  | **Yes** |
| `SLACK_USER_TOKEN`  | The user token found within the [Slack API settings](https://api.slack.com/bot-users). This must be the user token of an admin.  | **Yes** |
| `AWS_ACCESS_KEY_ID`  | Your AWS access key id, only required if you'd like to persist the bot settings.  | **No** |
| `AWS_SECRET_ACCESS_KEY`  | Your AWS access key id, only required if you'd like to persist the bot settings.  | **No** |
| `CHANNEL_WHITELIST`  | A comma seperated list of channels you'd like the bot to operate in, if this is left blank the bot will be allowed to join any channel. Requires `channels:write` and `channels:read` permissions. For example `general, random`.  | **No** |

## Commands

The following commands are available.

```
# Displays a list of available commands.
@slackbot-destroyer commands

# Activate Slackbot Destroyer in a channel.
@slackbot-destroyer destroy

# Deactivate Slackbot Destroyer in a channel.
@slackbot-destroyer deactivate

# Show how many times Slackbot Destroyer has destroyed Slackbot responses.
@slackbot-destroyer stats

# Teleport to the future
@slackbot-destroyer teleport
```
