import discord
import os

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(
    command_prefix=">",
    intents=discord.Intents.all()
)

client.load_extension("cogs.emulator")

client.run(TOKEN)