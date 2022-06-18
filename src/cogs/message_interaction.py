import discord

from discord.ext import commands

from src.cogs.emulator import Emulator
from src.modules.gif_exporter import GifExporter
from src.modules.message_utils import read_emoji_options


class MessageInteraction(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.gif_path = "output.gif"
        self.gif_exporter = GifExporter()

        self.buttons = {
            "up": "up",
            "down": "down",
            "right": "right",
            "left": "left",
            "a": "a",
            "b": "b",
            "start": "start",
            "select": "select"
        }
    
        self.button_map_words = {
            **self.buttons,
            "A": self.buttons["a"],
            "B": self.buttons["b"],
            "🅰": self.buttons["a"],
            "🅱": self.buttons["b"],
            "Start": self.buttons["start"],
            "Select": self.buttons["select"],
            "⏸": self.buttons["start"],
            "🈂": self.buttons["select"],
            "Up": self.buttons["up"],
            "Down": self.buttons["down"],
            "Right": self.buttons["right"],
            "Left": self.buttons["left"],
            "u": self.buttons["up"],
            "d": self.buttons["down"],
            "r": self.buttons["right"],
            "l": self.buttons["left"],
            "U": self.buttons["up"],
            "D": self.buttons["down"],
            "R": self.buttons["right"],
            "L": self.buttons["left"],
            "⬆": self.buttons["up"],
            "⬇": self.buttons["down"],
            "⬅": self.buttons["right"],
            "➡": self.buttons["left"]
        }

    @commands.Command
    async def start_game(self, ctx):
        self.send_game_message(ctx)

        # Ronan take input stuff here

    def send_game_message(self, ctx):
        self.create_output_gif()
        await ctx.send(file=discord.File(self.gif_path))

    def create_output_gif(self):
        emulator: Emulator = self.client.get_cog("Emulator")
        images = emulator.get_image_buffer()
        self.gif_exporter.create_gif(images, self.gif_path)


def setup(client: commands.Bot):
    client.add_cog(MessageInteraction(client))
