import logging
import os
from pyboy import PyBoy
from pyboy.utils import WindowEvent
from discord.ext import commands

import discord.embeds
from src.gif_exporter import GifExporter
from src.image_buffer import ImageBuffer


class Emulator(commands.Cog):
    """ Manages emulator state and returns gifs """
    def __init__(self, client):
        self.client = client
        self.pyboy = None

        self.saves_path = os.getcwd() + "/saves"
        self.current_rom_name = ""
        self.save_slot = 0
        #  0 is fast as possible
        self.emulation_speed = 0

        # Initialize emulator screenshot buffer, each second is 60 frames
        self.buffer_seconds = 6  # Buffer size in seconds
        self.image_buffer = ImageBuffer(self.buffer_seconds * 60)
        
        self.gif_exporter = GifExporter()

        self.initialize_game("pokemon-red", os.getcwd() + "/roms/" + "pokemon-red.gb")
        
    def tick(self, tick_count: int) -> None:
        for t in range(tick_count):
            self.pyboy.tick()
            self.image_buffer.push(self.pyboy.screen_image())

    def initialize_game(self, rom_name: str, rom_path: str, save_slot: int = 0) -> None:
        """ Load up new rom and load state """
        self.current_rom_name = rom_name
        self.pyboy = PyBoy(rom_path)
        self.pyboy.set_emulation_speed(self.emulation_speed)
        self.save_slot = save_slot
        self.load_state()

    def close_game(self):
        """ Shutdown pyboy and save game state """
        if self.pyboy:
            self.save_state()
            self.pyboy.stop()

            #  This will remove the pyboy from memory
            self.pyboy = None

    def export_buffer_as_gif(self):
        self.gif_exporter.create_gif(self.image_buffer.get_all())

    def save_state(self) -> None:
        save_name = f"{self.current_rom_name}_{self.save_slot}.state"
        with open(self.saves_path + "/" + save_name, "wb") as save_file:
            self.pyboy.save_state(save_file)

    def load_state(self) -> None:
        save_name = f"{self.current_rom_name}_{self.save_slot}.state"
        save_path = self.saves_path + "/" + save_name

        if not os.path.exists(save_path):
            logging.warning("There is no save file to load at path: " + save_path)
            return

        with open(self.saves_path + "/" + save_name, "rb") as save_file:
            self.pyboy.load_state(save_file)

    def move(self, move):
        if move == 'up':
            self.pyboy.send_input(WindowEvent.PRESS_ARROW_UP)
            self.tick(25)
            self.pyboy.send_input(WindowEvent.RELEASE_ARROW_UP)      
        elif move == 'down':
            self.pyboy.send_input(WindowEvent.PRESS_ARROW_DOWN)
            self.tick(25)
            self.pyboy.send_input(WindowEvent.RELEASE_ARROW_DOWN)      
        elif move == 'right':     
            self.pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
            self.tick(25)
            self.pyboy.send_input(WindowEvent.RELEASE_ARROW_RIGHT)
        elif move == 'left':
            self.pyboy.send_input(WindowEvent.PRESS_ARROW_LEFT)
            self.tick(25)
            self.pyboy.send_input(WindowEvent.RELEASE_ARROW_LEFT)
        elif move == 'a':
            self.pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
            self.tick(25)
            self.pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)        
        elif move == 'b':
            self.pyboy.send_input(WindowEvent.PRESS_BUTTON_B)
            self.tick(25)
            self.pyboy.send_input(WindowEvent.RELEASE_BUTTON_B)      
        elif move == 'start':
            self.pyboy.send_input(WindowEvent.PRESS_BUTTON_START)
            self.tick(25)
            self.pyboy.send_input(WindowEvent.RELEASE_BUTTON_START)       
        elif move == 'select':
            self.pyboy.send_input(WindowEvent.PRESS_BUTTON_SELECT)
            self.tick(25)
            self.pyboy.send_input(WindowEvent.RELEASE_BUTTON_SELECT)

    @commands.Command
    async def tick_test(self, ctx, tick_count: int = 60):
        self.tick(tick_count)

    @commands.Command
    async def newgame(self, ctx):
        self.initialize_game("pokemon-red", self.roms_path + "/" + "pokemon-red.gb")
        self.tick(self.buffer_seconds * 60)
        self.export_buffer_as_gif()
        self.save_state()
        return

    @commands.Command
    async def gba(self, ctx, move, amount: int = 1):
        self.initialize_game("pokemon-red", self.roms_path + "/" + "pokemon-red.gb")
        self.tick(20)
        for i in range(amount):
            self.move(move)
        self.tick(self.buffer_seconds * 60)
        self.export_buffer_as_gif()
        self.save_state()
        await ctx.send(file=discord.File('output.gif'))
        self.pyboy.stop()


def setup(client: commands.Bot):
    client.add_cog(Emulator(client))
