import logging

import discord

from discord.ext import commands

from src.cogs.emulator import Emulator
from src.modules.gif_exporter import GifExporter
from src.modules.message_utils import read_emoji_options


class MessageInteraction(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.current_game_message = None
        self.input_options= ["⬅", "⬆", "⬇", "➡", "🅰", "🅱", "⏸", "⏸"]

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
    async def start_game(self, ctx) -> None:
        await self.update_message(ctx)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, member) -> None:
        if not self.current_game_message or not reaction.message.id == self.current_game_message.id:
            # This is not a message we are watching reactions for
            return

        if member.bot:
            # Reaction is from a bot, nothing should be done
            return

        await self.process_input(reaction.emoji, reaction.message.channel)

    async def process_input(self, button_input: str, ctx) -> None:
        if button_input not in self.button_map_words.keys():
            logging.warning(f"There is no input for this reaction: {button_input}")
            return

        emulator: Emulator = self.client.get_cog("Emulator")
        await emulator.send_game_input(self.button_map_words[button_input], 1)

        await self.update_message(ctx)

    async def update_message(self, ctx) -> None:
        if self.current_game_message:
            await self.current_game_message.delete()

        emulator: Emulator = self.client.get_cog("Emulator")
        gif_path = emulator.create_gif()

        self.current_game_message = await ctx.send(file=discord.File(gif_path))

        for option in self.input_options:
            await self.current_game_message.add_reaction(option)


def setup(client: commands.Bot):
    client.add_cog(MessageInteraction(client))