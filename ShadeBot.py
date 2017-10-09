import os
import time
import random
from slackclient import SlackClient

BOT_NAME = 'shadebot'
BOT_ID = os.environ.get('BOT_ID')

#CONSTANTS
AT_BOT = "<@{0}>".format(BOT_ID)
EXAMPLE_COMMAND = "do"
INSULT_COMMAND = "insult"

#instantiate the client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

insults = ["you suck", "grow a pair!", "Your mom!", "Generic insults!", "I love you?"]


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    elif command.startswith(INSULT_COMMAND):
        command_number = random.randint(0, len(insults) - 1)
        response = "{0}".format(insults[command_number])
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print("ShadeBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command,channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection Failed. Invalide slack token or bot id?")





