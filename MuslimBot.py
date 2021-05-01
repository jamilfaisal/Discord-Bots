import asyncio
import aiohttp
import discord
import geopy.exc
from discord.ext import commands
from datetime import datetime
from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import Nominatim
from countryinfo import CountryInfo


bot_description = ""
intents = discord.Intents.default()
MuslimBot = commands.Bot(command_prefix='!', description=bot_description, intents=intents)


@MuslimBot.event
async def on_ready():
    print("Logged on as {}".format(MuslimBot.user))


@MuslimBot.command()
async def athan(ctx: commands.Context, address: str):
    try:
        city, country = await get_location(address)
    except ValueError as e:
        await ctx.send(str(e))
        return
    url = "http://api.aladhan.com/v1/timingsByCity?city={}&country={}&method=2".format(city, country)
    session = aiohttp.ClientSession()
    while True:
        try:
            async with session.get(url) as r:
                if r.status == 200:
                    js = await r.json()
                    await ctx.send(format_athan(js, city, country))
        except aiohttp.ServerDisconnectedError as e:
            print(e)
            continue
        except aiohttp.ClientOSError as e:
            print(e)
            continue
        break
    await session.close()


async def get_location(addr: str):
    async with Nominatim(
            user_agent="MuslimBot",
            adapter_factory=AioHTTPAdapter,
    ) as geolocator:
        try:
            location = await geolocator.geocode(addr, addressdetails=True)
        except geopy.exc.GeocoderTimedOut:
            raise ValueError("Could not find location!")
        if location is None:
            raise ValueError("Invalid address!")
        location = location.raw["address"]
        country = location.get("country")
        if country is None:
            raise ValueError("Country not found!")
        city = location.get("city")
        village = location.get("village")
        if city is not None:
            return city, country
        elif village is not None:
            return village, country
        else:
            c = CountryInfo(addr)
            return c.capital(), addr


def format_athan(json, city, country):
    date_format = datetime.today().strftime('%d-%m-%Y')
    timings = json["data"]["timings"]
    result = """Athan for {}, {} on {}:
    Fajr: {}
    Sunrise: {}
    Dhuhr: {}
    Asr: {}
    Maghrib: {}
    Isha: {}
    """.format(city, country,
               date_format,
               timings["Fajr"],
               timings["Sunrise"],
               timings["Dhuhr"],
               timings["Asr"],
               timings["Maghrib"],
               timings["Isha"])
    return result
