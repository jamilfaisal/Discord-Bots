import typing
import discord
from discord.ext import commands


bot_description = ""
intents = discord.Intents.default()
DerbyBot = commands.Bot(command_prefix='!', description = bot_description, intents=intents)


@DerbyBot.event
async def on_ready():
    print("Logged on as {}".format(DerbyBot.user))


@DerbyBot.command()
async def add(ctx: commands.Context, left: int, right: int):
    await ctx.send(content=(left + right))


@add.error
async def add_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.BadArgument):
        return await ctx.send("Invalid arguments!")