from logging import Logger
from typing import List
from PIL.Image import Image
from pyboy import PyBoy

from pyboy.utils import WindowEvent
from discord.ext import commands

from game_library_seacher import GameLibrarySearcher

""" Manages emulator state and returns gifs """
class Emulator(commands.Cog):
    def __init__(self, client):
        
        self.buffer_seconds = 4 # buffer size in seconds
        self.rom_path='roms/pokemon-red.gb'
        self.client = client

        # Initialize emulator screenshot buffer, each second is 60 frames
        self.image_buffer = ImageBuffer(self.buffer_seconds * 60)
        
        self.gif_exporter = GifExporter()
        
        self.libary_searcher = GameLibrarySearcher("roms")

        # Saving init
        self.save_slot = 0
        self.save_prefix = "state_file_"
        self.save_postfix = ".state" 
        
    def tick(self, tick_count: int) -> None:
        for t in range(tick_count):
            self.pyboy.tick()
            self.image_buffer.push(self.pyboy.screen_image())
            
    def export_buffer_as_gif(self):
        self.gif_exporter.create_gif(self.image_buffer.get_all())
        
    def save_state(self):
        save_name = self.save_prefix + str(self.save_slot) + self.save_postfix
        with open(save_name, "wb") as save_file:
            self.pyboy.save_state(save_file)

    def load_state(self):
        save_name = self.save_prefix + str(self.save_slot) + self.save_postfix
        with open(save_name, "rb") as save_file:
            self.pyboy.load_state(save_file)

    def initialize_game(self, rom: str):
        self.pyboy = PyBoy(rom)
        self.rom_path = self.libary_searcher.library_path + rom

    def input(self, event: WindowEvent):
        # Pass event to pyboy emulator
        self.pyboy.send_input(event)
    
    def move(self, move):
        if move == 'up':
            self.pyboy.send_input(WindowEvent.PRESS_ARROW_UP)
            self.tick(2)
            self.pyboy.send_input(WindowEvent.RELEASE_ARROW_UP)      
        elif move == 'down':
            self.pyboy.send_input(WindowEvent.PRESS_ARROW_DOWN)
            self.tick(2)
            self.pyboy.send_input(WindowEvent.RELEASE_ARROW_DOWN)      
        elif move == 'right':     
            self.pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
            self.tick(2)
            self.pyboy.send_input(WindowEvent.RELEASE_ARROW_RIGHT)
        elif move == 'left':
            self.pyboy.send_input(WindowEvent.PRESS_ARROW_LEFT)
            self.tick(2)
            self.pyboy.send_input(WindowEvent.RELEASE_ARROW_LEFT)
        elif move == 'a':
            self.pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
            self.tick(2)
            self.pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)        
        elif move == 'b':
            self.pyboy.send_input(WindowEvent.PRESS_BUTTON_B)
            self.tick(2)
            self.pyboy.send_input(WindowEvent.RELEASE_BUTTON_B)      
        elif move == 'start':
            self.pyboy.send_input(WindowEvent.PRESS_BUTTON_START)
            self.tick(2)
            self.pyboy.send_input(WindowEvent.RELEASE_BUTTON_START)       
        elif move == 'select':
            self.pyboy.send_input(WindowEvent.PRESS_BUTTON_SELECT)
            self.tick(2)
            self.pyboy.send_input(WindowEvent.RELEASE_BUTTON_SELECT)

    @commands.Command
    async def newgame(self, ctx):
        self.pyboy = PyBoy(self.rom_path)

        # This will try to emulate as fast as possible
        self.pyboy.set_emulation_speed(0)

        self.tick(self.buffer_seconds * 60)
        self.export_buffer_as_gif()
        self.save_state()
        return


    @commands.Command(
        brief="Will load the game if there is only one result for the search.",
        usage="load [game title]"
    )
    async def load(self, ctx, query: str):
        search_results = self.libary_searcher.search_text(query)
        if len(search_results) == 1:
            self.initialize_game(search_results[0])
        else:
            #print some search options in chat
            pass



    @commands.Command
    async def poke(self, ctx, move, amount):
        self.pyboy = PyBoy(self.rom_path)

        # This will try to emulate as fast as possible
        self.pyboy.set_emulation_speed(0)
        self.load_state()
        self.tick(2)
        i = 0
        while i < amount:
            self.move(move)
        self.tick(self.buffer_seconds * 60)
        self.export_buffer_as_gif()
        self.save_state()
        return             

class GifExporter():
    def __init__(self):
        pass
    
    def create_gif(self, images: List[Image]) -> None:
        if not images:
            Logger.error("No images to export as gif")
            return
        frame_one = images[0]
        frame_one.save("output.gif", format="GIF", append_images=images, save_all=True, duration=16, loop=0)


class ImageBuffer(): 
    """ A circular buffer that stores [size] items """
    def __init__(self, size: int):
        self.size = size
        self.index = 0
    
        # Fill the buffer to avoid assigning extra memory
        self.buffer = [None] * size
    
    def push(self, item) -> None:
        self.buffer[self.index] = item
        # Increase the index by 1, wrap back to 0 when index > buffer size
        self.index = (self.index + 1) % self.size
        
    def get_all(self) -> List:
        # Return everything in buffer in order starting with item at buffer_index
        all = self.buffer[self.index:] + self.buffer[0:self.index]
        all = [frame for frame in all if frame is not None]
        return all
    

def setup(client: commands.Bot):
    client.add_cog(Emulator(client))