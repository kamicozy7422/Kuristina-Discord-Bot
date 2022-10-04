import discord
import os
from discord.ext import commands, tasks
from itertools import cycle
from decouple import config

# Initialisation of the bot
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = ['k+', 'K+'], case_insensitive=True, help_command=None, intents=intents)
status = cycle(['Hacking To The Gate', 'I told you before its not Tina'])

# Events
@client.event
async def on_ready():
    change_status.start()
    print("bot is ready")

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(config('SECRET_KEY'))
