import typing
import discord
from discord.ext import commands
import aiohttp


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


@DerbyBot.command()
async def cat(ctx: commands.Context):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://aws.random.cat/meow') as r:
            if r.status == 200:
                js = await r.json()
                await ctx.send(js['file'])
