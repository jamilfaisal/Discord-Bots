import typing
import discord
from discord.ext import commands


bot_description = ""
intents = discord.Intents.default()
MuslimBot = commands.Bot(command_prefix='!', description = bot_description, intents=intents)


@MuslimBot.event
async def on_ready():
    print("Logged on as {}".format(MuslimBot.user))


