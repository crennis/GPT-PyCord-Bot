# GPT-3.5 PyCord Discord Bot



This is a Discord Bot that Uses OpenAI's new Chat API-Endpoint to generate text like ChatGPT

## How to use

This Bot uses the PyCord Library ([PyCord](https://pycord.dev/)) and the OpenAI Python Library ([OpenAI](https://platform.openai.com/docs/libraries))

There are three ways to use this bot:

1. By just inviting [this Bot](https://discord.com/api/oauth2/authorize?client_id=1083786070786850959&permissions=2147486720&scope=bot) to your Server

2. Using Docker
3. Without using Docker

### The No Docker Way

1. Clone the Repo
2. Install the requirements using `pip install -r requirements.txt`. Preferably in a virtual environment like `venv`.
3. Get a Discord Bot Token from the [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new Application
   - Go to the Bot Tab and create a new Bot
   - Copy the Token
   - Also Check under Privileged Gateway Intents the following:
     - Server Members Intent
     - Message Content Intent
4. Get an OpenAI API Key from [OpenAI](https://platform.openai.com/account/api-keys)
6. Go to the `configs`-folder and create a file called `.env` in the config folder and add the following:

```shell
DISCORD_TOKEN=Your_Bot_Token
OPENAI_API_KEY=Your_OpenAI_API_Key
```

6. Run the bot using `python main.py` or `python3 main.py`
    - To keep the Bot running in the background use `nohup python3 main.py &`
    - To stop the Bot use `pkill -f main.py`

### The Docker Way

1. Clone the Repo
2. Get a Discord Bot Token from the [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new Application
   - Go to the Bot Tab and create a new Bot
   - Copy the Token
   - Also Check under Privileged Gateway Intents the following:
     - Server Members Intent
     - Message Content Intent
3. Get an OpenAI API Key from [OpenAI](https://platform.openai.com/account/api-keys)
4. Use `docker build -t discord-bot .` to build the Docker Image
5. Make a folder called `chat`
6. Make a folder called `config` and create a file called `.env` in the configs folder and add the following:

```shell
DISCORD_TOKEN=Your_Bot_Token
OPENAI_API_KEY=Your_OpenAI_API_Key
```

7. Run the bot using `docker run -v /path/to/config:/usr/share/dcbot/configs -v /path/to/chat:/usr/share/dcbot/chats -d --name discord-bot discord-bot`
8. To stop the Bot use `docker stop <container-id>`

## How to use the Bot

Once the Bot is running and you have invited it to your Server, you can use the following commands:

- /add text (channel-id) to Add the Bot to listen in a channel. The Bot will listen to all messages in that channel and answer them using GPT-3.5. The Bot will ignore Messages with a Prefix (Default - $)
- /add prefix (channel-id) to Add the Bot to listen in a channel. The Bot will listen to all messages in that channel that start with the prefix and answer them using GPT-3.5 (Default - !)
- /remove text/prefix (channel-id) to remove the Bot from listening in a channel.
- /list text/prefix to list all channels the Bot is listening in.
- /delete to delete the bots history from specific channels.
- /help to get a list of all commands.
- /ping to check if the Bot is online.
- /setup (channelid) (System-Message) Changes the System-Message. See OenAI's Documentation for more information. [OpenAI Docs](https://platform.openai.com/docs/guides/chat/instructing-chat-models)


### Future Improvements

- Currently I am working on an SQLite DB to store all information needed (eg. Servers, Channels, Configs, etc)
- Also I am working on a way to toggle between GPT 3.5-turbo and GPT-4
- Need to find and fix Bugs

### How to Contribute

If you want to contribute to this project, feel free to open a PR or Issue.

### Credits

- [OpenAI](https://openai.com/) for the GPT API
- [PyCord](https://pycord.dev/) for the Discord API Wrapper
- [Drone](https://drone.io/) for the CI/CD
