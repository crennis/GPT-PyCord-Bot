# Rewrite of Channelmgmt
from os import path

folder = "configs"
text_channel_file = "text_channels.txt"
prefix_channel_file = "prefix_channels.txt"

def load_config():
    # Load Text-Channel Config
    try:
        with open(path.join(folder,text_channel_file), "r") as f:
            text_channels = f.read().split("\n")
    except Exception as error:
        print(f'File not Fount, creating new. {error}')
        with open(path.join(folder,text_channel_file), "w") as f:
            f.write('')
        text_channels = []
    # Load Prefix-Channel Config
    try:
        with open(path.join(folder, prefix_channel_file), "r") as f:
            prefix_channels = f.read().split("\n")
    except Exception as error:
        print(f'File not Fount, creating new. {error}')
        with open(path.join(folder, prefix_channel_file), "w") as f:
            f.write('')
        prefix_channels = []

    return text_channels, prefix_channels

# Add Channel to Config
def add_channel(type, id):
    try:
        if type == "text":
            text_channels = load_config()
            if id in text_channels:
                # Throw Error if already in List
                raise ValueError("Channel already in List")
            else:
                with open(path.join(folder, text_channel_file), 'a') as f:
                    f.write(f'{id}\n')
                return True
        elif type == "prefix":
            prefix_channels = load_config()
            if id in prefix_channels:
                # Throw Error if already in List
                raise ValueError("Channel already in List")
            else:
                with open(path.join(folder, prefix_channel_file), 'a') as f:
                    f.write(f'{id}\n')
                return True

    except FileNotFoundError as error:
        load_config()
        add_channel(type, id)

def remove_channel(type, id):
    try:
        if type == "text":
            text_channels = load_config()
            if id in text_channels:
                text_channels.remove(id)
                new_conf = ""
                for x in text_channels:
                    new_conf += f'{x}\n'

                with open(path.join(folder, text_channel_file), 'w') as f:
                    f.write(new_conf)
                return True
            else:
                raise ValueError("Channel not in List")

        elif type == "prefix":
            prefix_channels = load_config()
            if id in prefix_channels:
                prefix_channels.remove(id)
                new_conf = ""
                for x in prefix_channels:
                    new_conf += f'{x}\n'

                with open(path.join(folder, prefix_channel_file), 'w') as f:
                    f.write(new_conf)
                return True
            else:
                raise ValueError("Channel not in List")

    except Exception as error:
        print(error)
        return False