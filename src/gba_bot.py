import discord
import os

from discord import emoji
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(
    command_prefix=">",
    intents=discord.Intents.all()
)

client.load_extension("cogs.emulator")
client.load_extension("cogs.game_library")


@client.event
async def on_raw_reaction_add(payload):
    if payload.user_id == "984864873450176602":
        return

    if payload.emoji.name == "arrow_up_small":
        pass
    elif emoji == "emoji 2":
        pass
    elif emoji == "emoji 3":
        pass
    else:
        return

client.run(TOKEN)
