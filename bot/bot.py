import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import modules.gpt as gpt
import modules.dbmanagement as dbm
import modules.summarize as summarize

description = "ChatGPT Bot for Discord"
configfolder = "config"

load_dotenv(dotenv_path=os.path.join(configfolder, ".env"))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = discord.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description=description,
    intents=intents,
)

### \/ Events Area \/ ###

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await dbm.init_db()

### Message Listener
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    ### Check if Channel is Configured
    if await dbm.get_channel_by_id(message.guild.id, message.channel.id) is not None:
        config = await dbm.get_config_by_id(message.guild.id, message.channel.id)
        if message.content.startswith(config[2]):
            ### Count Messages for Summary
            counter = 0
            if await dbm.get_last_chat(message.guild.id, message.channel.id) is not None:
                counter = await dbm.get_last_chat(message.guild.id, message.channel.id)
                counter = counter[8]
                counter = counter + 1
            else:
                await dbm.add_summary_zero(message.guild.id, message.channel.id)

            ### Read and Send Message/Answer
            await message.channel.trigger_typing()
            msg = message.content.replace(config[2], "", 1)
            await dbm.add_chat(message.guild.id, message.channel.id, message.author.id, message.author.name, "user", message.id, f'{message.author}: {msg}', counter)
            answer = await gpt.get_answer(message.guild.id, message.channel.id)
            sendmsg = await message.channel.send(answer)
            await dbm.add_chat(message.guild.id, message.channel.id, bot.user.id, bot.user.name, "assistant", sendmsg.id, answer, counter+1)

            ### Check if Summary is needed
            last_summary = await dbm.get_latest_summary(message.guild.id, message.channel.id)
            last_summary = last_summary[4]
            last_message = await dbm.get_last_chat(message.guild.id, message.channel.id)
            last_message = last_message[8]

            ### Check if Last Summary is older than 20 Messages
            if last_message - last_summary >= 30:
                await summarize.new_summarize(message.guild.id, message.channel.id)

### /\ End Events Area /\ ###

### \/ Modal Area \/ ###

### Modal Class for Setup
class SetupModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(discord.ui.InputText(label="Channel-ID", placeholder="Channel-ID", required=True))
        self.add_item(discord.ui.InputText(label="Prefix", placeholder="!", required=False))
        self.add_item(discord.ui.InputText(label="GPT", placeholder="3", required=True))
        self.add_item(discord.ui.InputText(label="System Message", placeholder="System Message", required=False, style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Setup Vals")
        embed.add_field(name="Channel-ID", value=self.children[0].value)
        embed.add_field(name="Prefix", value=self.children[1].value)
        embed.add_field(name="GPT", value=self.children[2].value)
        embed.add_field(name="System Message", value=self.children[3].value)

        await interaction.response.send_message(embeds=[embed], ephemeral=True)

        if await dbm.get_server_by_id(interaction.guild.id) is None:
            print("Server not in DB")
            await dbm.add_server(interaction.guild.id)
            await dbm.add_channel(interaction.guild.id, self.children[0].value)
            if dbm.is_premium(interaction.guild.id):
                await dbm.add_config(interaction.guild.id, self.children[0].value, self.children[1].value, self.children[2].value, self.children[3].value)
            else:
                await dbm.add_config(interaction.guild.id, self.children[0].value, 3, self.children[2].value, self.children[3].value)
            await dbm.add_summary_zero(interaction.guild.id, self.children[0].value)
            await dbm.default_premium(interaction.guild.id)
            print("Setup: Server")

        elif await dbm.get_server_by_id(interaction.guild.id) is not None and await dbm.get_channel_by_id(interaction.guild.id, self.children[0].value) is None:
            print("Server in DB, but Channel not")
            await dbm.add_channel(interaction.guild.id, self.children[0].value)
            if dbm.is_premium(interaction.guild.id):
                await dbm.add_config(interaction.guild.id, self.children[0].value, self.children[1].value, self.children[2].value, self.children[3].value)
            else:
                await dbm.add_config(interaction.guild.id, self.children[0].value, 3, self.children[2].value, self.children[3].value)

            await dbm.add_summary_zero(interaction.guild.id, self.children[0].value)
            print("Setup: Channel, Config")

        elif await dbm.get_server_by_id(interaction.guild.id) is not None and await dbm.get_channel_by_id(interaction.guild.id, self.children[0].value) is not None:
            print("Server and Channel in DB, rerun Setup")
            await dbm.remove_channel(interaction.guild.id, self.children[0].value)
            await dbm.remove_config(interaction.guild.id, self.children[0].value)
            await dbm.add_channel(interaction.guild.id, self.children[0].value)
            if dbm.is_premium(interaction.guild.id):
                await dbm.add_config(interaction.guild.id, self.children[0].value, self.children[1].value, self.children[2].value, self.children[3].value)
            else:
                await dbm.add_config(interaction.guild.id, self.children[0].value, 3, self.children[2].value, self.children[3].value)
            await dbm.add_summary_zero(interaction.guild.id, self.children[0].value)
            print("Setup: Channel, Config")

### Add Modal
class AddModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(discord.ui.InputText(label="Prefix (Leave empty for no Prefix)", placeholder="!", required=False))
        self.add_item(discord.ui.InputText(label="GPT (3 - GPT-3.5-Turbo; 4- GPT-4)", placeholder="3", required=True))
        self.add_item(discord.ui.InputText(label="System Message", placeholder="System Message", required=False, style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        if await dbm.get_server_by_id(interaction.guild.id) is None:
            print("Server not in DB")
            await dbm.add_server(interaction.guild.id)
            await dbm.add_channel(interaction.guild.id, interaction.channel.id)
            if dbm.is_premium(interaction.guild.id):
                await dbm.add_config(interaction.guild.id, interaction.channel.id, self.children[0].value, self.children[1].value, self.children[2].value)
            else:
                await dbm.add_config(interaction.guild.id, interaction.channel.id, self.children[0].value, 3, self.children[2].value)
            await dbm.add_summary_zero(interaction.guild.id, interaction.channel.id)
            print("Setup: Channel, Server, Config")
        elif await dbm.get_server_by_id(interaction.guild.id) is not None and await dbm.get_channel_by_id(interaction.guild.id, interaction.channel.id) is None:
            await dbm.add_channel(interaction.guild.id, interaction.channel.id)
            if dbm.is_premium(interaction.guild.id):
                await dbm.add_config(interaction.guild.id, interaction.channel.id, self.children[0].value,
                                     self.children[1].value, self.children[2].value)
            else:
                await dbm.add_config(interaction.guild.id, interaction.channel.id, self.children[0].value, 3,
                                     self.children[2].value)
            await dbm.add_summary_zero(interaction.guild.id, interaction.channel.id)
            print("Setup: Channel, Config")
        elif await dbm.get_server_by_id(interaction.guild.id) is not None and await dbm.get_channel_by_id(interaction.guild.id, interaction.channel.id) is not None:
            await dbm.remove_channel(interaction.guild.id, interaction.channel.id)
            await dbm.remove_config(interaction.guild.id, interaction.channel.id)
            if dbm.is_premium(interaction.guild.id):
                await dbm.add_config(interaction.guild.id, interaction.channel.id, self.children[0].value,
                                     self.children[1].value, self.children[2].value)
            else:
                await dbm.add_config(interaction.guild.id, interaction.channel.id, self.children[0].value, 3,
                                     self.children[2].value)
            await dbm.add_config(interaction.guild.id, interaction.channel.id, self.children[0].value, self.children[1].value, self.children[2].value)
            await dbm.add_summary_zero(interaction.guild.id, interaction.channel.id)
            print("Setup: Channel, Config")

        if dbm.is_premium(interaction.guild.id):
            await interaction.response.send_message('Setup Channel', ephemeral=True)
        else:
            await interaction.response.send_message('Setup Channel (Using GPT-3.5)', ephemeral=True)

### Edit Modal
class EditSystemModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(discord.ui.InputText(label="System Message", placeholder="System Message", required=False, style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        server, channel, prefix, gptver, systemmsg  = await dbm.get_config_by_id(interaction.guild.id, interaction.channel.id)
        await dbm.remove_config(interaction.guild.id, interaction.channel.id)
        await dbm.add_config(interaction.guild.id, interaction.channel.id, prefix, gptver, self.children[0].value)
        await interaction.response.send_message("System Message changed", ephemeral=True)

### /\ End Modal Area /\ ###

### \/ Commands Area \/ ###

### Setup Command
@bot.command(name="setup", description="Used to setup the Bot")
@commands.has_permissions(administrator=True)
async def setup(ctx: discord.ApplicationContext):
    modal = SetupModal(title="Setup ChatGPT")
    await ctx.send_modal(modal)


@bot.command(name="add", description="Used to add Bot answering to specific Channels")
@commands.has_permissions(administrator=True)
async def add(ctx: discord.ApplicationContext):
    if await dbm.get_channel_by_id(ctx.guild.id, ctx.channel.id) is None:
        modal = AddModal(title="Add Channel")
        await ctx.send_modal(modal)
    else:
        await ctx.respond("Channel has already been added. Use /setup", ephemeral=True)


@bot.command(name="remove", description="Used to remove Bot answering to specific Channels")
@commands.has_permissions(administrator=True)
async def remove(ctx: discord.ApplicationContext):
    if await dbm.get_channel_by_id(ctx.guild.id, ctx.channel.id) is not None:
        await dbm.remove_channel(ctx.guild.id, ctx.channel.id)
        await ctx.respond("Channel removed", ephemeral=True)
    else:
        await ctx.respond("Channel not active. Nothing Done", ephemeral=True)


@bot.command(name="list", description="Used to list all Channels in the Server")
@commands.has_permissions(administrator=True)
async def list(ctx: discord.ApplicationContext):

        await ctx.respond("This command is WIP")


@bot.command(name="clear", description="Used to clear chat history of specific Channels/Users")
@commands.has_permissions(administrator=True)
async def clear(ctx: discord.ApplicationContext):
    await dbm.add_summary_zero(ctx.guild.id, ctx.channel.id)
    await ctx.respond("Bot got Amnesia", ephemeral=True)

# Old System, Rewrite needed
@bot.command(name="help", description="Used to get help")
async def help(ctx: discord.ApplicationContext):
    await ctx.respond(f'Here is a list of all commands:\n'
                        'Needs Rewrite\n', ephemeral=True)

@bot.command(name="ping", description="Used to check if the bot is alive")
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond(f'pong', ephemeral=True)

# Old System, Rewrite needed
@bot.command(name="system", description="Used to setup the bot with a custom system message")
@commands.has_permissions(administrator=True)
async def system(ctx: discord.ApplicationContext):
    try:
        modal = EditSystemModal(title="Change System Message")
        await ctx.send_modal(modal)
    except:
        await ctx.respond("No Config found for this Channel", ephemeral=True)

### /\ End Commands Area /\ ###




bot.run(str(os.environ.get('DISCORD_TOKEN')))
