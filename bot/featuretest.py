import modules.channelconfig as config
import modules.gpt as gpt
import os

text_channels = config.load_config()

def listen_input(username, channel):
    message = input(f'{username} {channel}: ')
    if message.startswith("/"):
        print(slash_command(username, channel, message))
    elif message.startswith("$") and channel in text_channels:
        ask_gpt(username, channel, message)
    else:
        print(log_message(username, channel, message))


def log_message(user, channel, message):
    return f'User {user} sent "{message}" in {channel}'

# Slash Command Wrapper
def slash_command(user, channel, message):
    message = message.split("/")[1].split(" ")
    # Add Channels to Config
    if message[0] == "add":
        pass
    if message[1] == "text":
        config.add_channel("text", message[2])
        print("Added Channel to Config")

    # Remove Channels from Config
    elif message[0] == "remove":
        if message[1] == "text":
            return config.remove_channel("text", message[2])
    # Reload Config
    elif message[0] == "reload":
        text_channels = config.load_config()
        return text_channels
    else:
        return "Invalid Command"

def ask_gpt(user, id, message):
    message = message.split('$')[1]
    answer = gpt.get_answer(id, user, message)
    print(answer)

username = "XYZ"
channel = "112233445566"

while True:
    text_channels = config.load_config()
    listen_input(username, channel)
