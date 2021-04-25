import asyncio

import aiohttp
import discord
from discord.ext import commands
import requests
from datetime import datetime

bot_description = ""
intents = discord.Intents.default()
MuslimBot = commands.Bot(command_prefix='!', description = bot_description, intents=intents)


@MuslimBot.event
async def on_ready():
    print("Logged on as {}".format(MuslimBot.user))


@MuslimBot.command()
async def athan(ctx: commands.Context, city: str="Toronto", country: str="Canada"):
    url = "http://api.aladhan.com/v1/timingsByCity?city={}&country={}&method=2".format(city, country)
    session = aiohttp.ClientSession()
    while True:
        try:
            async with session.get(url) as r:
                if r.status == 200:
                    js = await r.json()
                    await ctx.send(format_athan(js))
        except Exception as e:
            print(e)
            continue
        break
    await session.close()


def format_athan(json):
    date_format = datetime.today().strftime('%d-%m-%Y')
    timings = json["data"]["timings"]
    result = """Athan for {}
                        Fajr: {}
                        Sunrise: {}
                        Dhuhr: {}
                        Asr: {}
                        Maghrib: {}
                        Isha: {}
                        """.format(date_format,
                                   timings["Fajr"],
                                   timings["Sunrise"],
                                   timings["Dhuhr"],
                                   timings["Asr"],
                                   timings["Maghrib"],
                                   timings["Isha"])
    return result
