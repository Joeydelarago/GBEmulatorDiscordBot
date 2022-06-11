import logging
import os
from logging import Logger
from typing import List
from PIL.Image import Image
from pyboy import PyBoy
from pyboy.utils import WindowEvent
from discord.ext import commands

import discord.embeds
from src.game_library_seacher import GameLibrarySearcher
from src.gif_exporter import GifExporter
from src.image_buffer import ImageBuffer


class Emulator(commands.Cog):
    """ Manages emulator state and returns gifs """
    def __init__(self, client):
        self.client = client
        self.pyboy = None

        self.saves_path = os.getcwd() + "/saves"
        self.roms_path = os.getcwd() + "/roms"
        self.current_rom_name = ""
        self.save_slot = 0

        # Initialize emulator screenshot buffer, each second is 60 frames
        self.buffer_seconds = 6  # Buffer size in seconds
        self.image_buffer = ImageBuffer(self.buffer_seconds * 60)
        
        self.gif_exporter = GifExporter()
        
        self.library_searcher = GameLibrarySearcher(self.roms_path)

        self.initialize_game("pokemon-red.gb")
        
    def tick(self, tick_count: int) -> None:
        for t in range(tick_count):
            self.pyboy.tick()
            self.image_buffer.push(self.pyboy.screen_image())
            
    def export_buffer_as_gif(self):
        self.gif_exporter.create_gif(self.image_buffer.get_all())
        
    def save_state(self) -> None:
        save_name = "{rom_name}_{save_slot}.state".format(rom_name=self.current_rom_name, save_slot=self.save_slot)
        with open(self.saves_path + "/" + save_name, "wb") as save_file:
            self.pyboy.save_state(save_file)

    def load_state(self) -> None:
        save_name = "{rom_name}_{save_slot}.state".format(rom_name=self.current_rom_name, save_slot=self.save_slot)
        save_path = self.saves_path + "/" + save_name

        if not os.path.exists(save_path):
            logging.warning("There is no save file to load at path: " + save_path)
            return

        with open(self.save_path + "/" + save_name, "rb") as save_file:
            self.pyboy.load_state(save_file)

    def initialize_game(self, rom_name: str, save_slot: int = 0) -> None:
        self.current_rom_name = rom_name
        self.pyboy = PyBoy(self.roms_path + "/" + rom_name)
        self.save_slot = save_slot
        self.load_state()

    def close_game(self):
        if self.pyboy:
            self.pyboy.save_state()
            self.pyboy.stop()

            #  This will remove the pyboy from memory
            self.pyboy = None
    
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
    async def load(self, ctx, query: str):
        search_results = self.library_searcher.search_text(query)
        if len(search_results) == 1:
            self.close_game()
            self.initialize_game(search_results[0])
        else:
            #print some search options in chat
            pass

    @commands.Command
    async def newgame(self, ctx):
        self.pyboy = PyBoy(self.rom_path)

        # This will try to emulate as fast as possible
        self.pyboy.set_emulation_speed(0)

        self.tick(self.buffer_seconds * 60)
        self.export_buffer_as_gif()
        self.save_state()
        return

    @commands.Command
    async def gba(self, ctx, move, amount: int = 1):
        self.pyboy = PyBoy(self.rom_path)

        # This will try to emulate as fast as possible
        self.pyboy.set_emulation_speed(0)
        self.load_state()
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
