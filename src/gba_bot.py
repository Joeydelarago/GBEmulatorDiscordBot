import discord
import os

from discord import emoji
from dotenv import load_dotenv
from discord.ext import commands
from pathlib import Path

load_dotenv()
os.chdir(Path(__file__).parent.parent)

TOKEN = os.getenv('DISCORD_TOKEN')
ABS_PATH = Path(os.getcwd())
COG_FOLDER = os.path.join(ABS_PATH, 'src\cogs')

client = commands.Bot(
    command_prefix=">",
    intents=discord.Intents.all()
)

#loads all cogs in cog folder
for filename in os.listdir(COG_FOLDER):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

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
