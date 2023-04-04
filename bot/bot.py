import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import modules.gpt as gpt
import modules.tts as tts
import modules.summarize as summarize
import modules.channelconfig as config

description = "ChatGPT Bot for Discord"
configfolder = "configs"
audiofolder = "audio"

load_dotenv(dotenv_path=os.path.join(configfolder, ".env"))

text_channels, prefix_channels = config.load_config()
tts_language = "de-DE"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = discord.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description=description,
    intents=intents,
)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if str(message.channel.id) in text_channels and not message.content.startswith("$"):
        await message.channel.trigger_typing()
        print(f'{message.author} asked: {message.content}')
        answer = await gpt.get_answer(message.channel.id, message.author, message.content)
        print(f'Answer: {answer}')
        await message.channel.send(answer)

    if str(message.channel.id) in prefix_channels:
        if message.content.startswith("!"):
            msg_split = message.content.split("!")[1]
            await message.channel.trigger_typing()
            print(f'{message.author} asked: {message.content}')
            answer = await gpt.get_answer(message.channel.id, message.author, msg_split)
            print(f'Answer: {answer}')
            await message.channel.send(answer)


@bot.command(name="add", description="Used to add Bot answering to specific Channels")
async def add(
        ctx: discord.ApplicationContext,
        option: discord.Option(str, choices=["text","prefix"], description="Type of Channel to Add"),
        id: discord.Option(str, description="Channel-ID -> Activate Developer-Options to Copy")):

    if ctx.author.guild_permissions.administrator:
        try:
            config.add_channel(option, id)

            if option == "text":
                text_channels.append(id)

            elif option == "prefix":
                prefix_channels.append(id)

            await ctx.respond(f'{option} channel {id} added', ephemeral=True)
        except ValueError as e:
            await ctx.respond(f'Error: {e}', ephemeral=True)
    else:
        await ctx.respond(f'Error: You need to be an Administrator to use this command', ephemeral=True)

@bot.command(name="remove", description="Used to remove Bot answering to specific Channels")
async def remove(
        ctx: discord.ApplicationContext,
        option: discord.Option(str, choices=["text", "prefix"], description="Type of Channel to Add"),
        id: discord.Option(str, description="Channel-ID -> Activate Developer-Options to Copy")):
    if ctx.author.guild_permissions.administrator:
        try:
            config.remove_channel(option, id)

            if option == "text":
                text_channels.remove(id)

            elif option == "prefix":
                prefix_channels.remove(id)

            await ctx.respond(f'{option} channel {id} removed', ephemeral=True)
        except ValueError as e:
            await ctx.respond(f'Error: {e}', ephemeral=True)
    else:
        await ctx.respond(f'Error: You need to be an Administrator to use this command', ephemeral=True)

@bot.command(name="list", description="Used to list all Channels the Bot is answering to")
async def list(
        ctx: discord.ApplicationContext,
        option: discord.Option(str, choices=["text", "prefix"], description="Type of Channels to List")):

        if ctx.author.guild_permissions.administrator:
            if option == "text":
                await ctx.respond(f'{option} channels: {str(text_channels)}', ephemeral=True)
            elif option == "prefix":
                await ctx.respond(f'{option} channels: {str(prefix_channels)}', ephemeral=True)
        else:
            await ctx.respond(f'Error: You need to be an Administrator to use this command', ephemeral=True)

@bot.command(name="delete", description="Used to delete chat history of specific Channels/Users")
async def delete(
        ctx: discord.ApplicationContext,
        option: discord.Option(str, choices=["text", "prefix"], description="Type of Channel to Delete"),
        id: discord.Option(str, description="Channel-ID -> Activate Developer-Options to Copy")):

    if ctx.author.guild_permissions.administrator:
        try:
            gpt.delete_history(id)
            await ctx.respond(f'{option} channel {id} history deleted', ephemeral=True)
        except Exception as e:
            await ctx.respond(f'Error: {e}', ephemeral=True)
    else:
        await ctx.respond(f'Error: You need to be an Administrator to use this command', ephemeral=True)

@bot.command(name="help", description="Used to get help")
async def help(ctx: discord.ApplicationContext):
    await ctx.respond(f'Here is a list of all commands:\n'
                        f'/ping\n'
                        f'/setup <channel-id> <system-message>\n'
                        f'/add <text/prefix> <channel-id>\n'        
                        f'/remove <text/prefix> <channel-id>\n'
                        f'/list <text/prefix>\n'    
                        f'/delete <text/prefix> <channel-id>\n'        
                        f'/help', ephemeral=True)

@bot.command(name="ping", description="Used to check if the bot is alive")
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond(f'pong', ephemeral=True)

@bot.command(name="setup", description="Used to setup the bot with a custom system message")
async def setup(ctx: discord.ApplicationContext,
                id: discord.Option(str, description="Channel-ID -> Activate Developer-Options to Copy"),
                message: discord.Option(str, description="System Message")):
    if ctx.author.guild_permissions.administrator:
        try:
            gpt.setup_history(id, message)
            await ctx.respond(f'Setup successful', ephemeral=True)
        except Exception as e:
            await ctx.respond(f'Error: {e}', ephemeral=True)
    else:
        await ctx.respond(f'Error: You need to be an Administrator to use this command', ephemeral=True)

bot.run(str(os.environ.get('DISCORD_TOKEN')))
