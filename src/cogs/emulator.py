import logging
import os
import asyncio

from pyboy import PyBoy
from pyboy.utils import WindowEvent
from discord.ext import commands

from src.modules.gif_exporter import GifExporter
from src.modules.image_buffer import ImageBuffer


class Emulator(commands.Cog):
    BUTTONS = {
            "up": (WindowEvent.PRESS_ARROW_UP, WindowEvent.RELEASE_ARROW_UP),
            "down": (WindowEvent.PRESS_ARROW_DOWN, WindowEvent.RELEASE_ARROW_DOWN),
            "right": (WindowEvent.PRESS_ARROW_RIGHT, WindowEvent.RELEASE_ARROW_RIGHT),
            "left": (WindowEvent.PRESS_ARROW_LEFT, WindowEvent.RELEASE_ARROW_LEFT),
            "a": (WindowEvent.PRESS_BUTTON_A, WindowEvent.RELEASE_BUTTON_A),
            "b": (WindowEvent.PRESS_BUTTON_B, WindowEvent.RELEASE_BUTTON_B),
            "start": (WindowEvent.PRESS_BUTTON_START, WindowEvent.RELEASE_BUTTON_START),
            "select": (WindowEvent.PRESS_BUTTON_SELECT, WindowEvent.RELEASE_BUTTON_SELECT)
        }
    
    """ Manages emulator state and returns gifs """
    def __init__(self, client):
        self.client = client
        self.pyboy = None

        self.saves_path = os.path.join(os.getcwd(), "saves")
        self.current_rom_name = ""
        self.save_slot = 0
        self.emulation_speed = 0
        self.button_press_ticks = 4
        
        # Initialize emulator screenshot buffer, each second is 60 frames
        self.buffer_size = 6 * 60  # Buffer size in seconds multiplied by frames per second
        self.image_buffer = ImageBuffer(self.buffer_size)

        self.gif_path = "output.gif"
        self.gif_exporter = GifExporter()

        self.initialize_game("pokemon-red", os.path.join(os.getcwd(), "roms", "pokemon-red.gb"))

        self.current_message = None
        
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

        # Fill buffer so we can send initial gif
        self.tick(self.buffer_size)

    def close_game(self):
        """ Shutdown pyboy and save game state """
        if self.pyboy:
            self.save_state()
            self.pyboy.stop()

            #  This will remove the pyboy from memory
            self.pyboy = None

    def save_state(self) -> None:
        save_name = f"{self.current_rom_name}_{self.save_slot}.state"
        with open(os.path.join(self.saves_path, save_name), "wb") as save_file:
            self.pyboy.save_state(save_file)

    def load_state(self) -> None:
        save_name = f"{self.current_rom_name}_{self.save_slot}.state"
        save_path = os.path.join(self.saves_path, save_name)

        if not os.path.exists(save_path):
            logging.warning("There is no save file to load at path: " + save_path)
            return

        with open(os.path.join(self.saves_path, save_name), "rb") as save_file:
            self.pyboy.load_state(save_file)

    async def send_game_input(self, button, amount):
        for i in range(amount):
            self.pyboy.send_input(self.BUTTONS[button][0])
            for i in range(0, self.button_press_ticks):
                self.pyboy.tick()
            self.pyboy.send_input(self.BUTTONS[button][1])
            if amount > 1:
                await asyncio.sleep(0.1)

    def create_gif(self) -> str:
        """ Creates a new gif and returns the path to the gif"""
        self.gif_exporter.create_gif(self.image_buffer.get_all(), self.gif_path)
        return self.gif_path

    @commands.Command
    async def tick_test(self, ctx, tick_count: int = 60):
        self.tick(tick_count)


def setup(client: commands.Bot):
    client.add_cog(Emulator(client))