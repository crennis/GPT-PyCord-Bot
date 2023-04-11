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
6. Go to the `config`-folder and create a file called `.env` in the config folder and add the following:

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
5. Make a folder called `config` and create a file called `.env` in the configs folder and add the following:

```shell
DISCORD_TOKEN=Your_Bot_Token
OPENAI_API_KEY=Your_OpenAI_API_Key
```

7. Run the bot using `docker run -v /path/to/config:/usr/share/dcbot/config -d --name discord-bot discord-bot`
8. To stop the Bot use `docker stop discord-bot`

## How to use the Bot

Once the Bot is running and you have invited it to your Server, you can use the following commands:

- /add - Opens a Dialog to add a new Server to the Bot
- /setup - Same as Add, but you can change the Channel ID
- /remove - Removes the current Channel from the Bot
- /clear - Clears the Message History used by the Bot. Does not remove Messages from Discord, only from the Bot
- /system - Opens a Dialog to change the System-Messege set to the Bot. More in OpenAI's Docs
- /ping - Checks if the Bot is responding

### How to Contribute

If you want to contribute to this project, feel free to open a PR or Issue.

### Credits

- [OpenAI](https://openai.com/) for the GPT API
- [PyCord](https://pycord.dev/) for the Discord API Wrapper
