from logging import Logger
from typing import List
from PIL.Image import Image
from pyboy import PyBoy

from pyboy.utils import WindowEvent
from discord.ext import commands

""" Manages emulator state and returns gifs """
class emulator(commands.Cog):
    def __init__(self, client):
        ROM_PATH='roms/pokemon-red.gb'
        BUFFER_SECONDS=3 # buffer size in seconds

        self.client = client
        self.pyboy = PyBoy(ROM_PATH)
        
        # This will try to emulate as fast as possible
        self.pyboy.set_emulation_speed(0)
        
        # Initialize emulator screenshot buffer, each second is 60 frames
        self.image_buffer = ImageBuffer(BUFFER_SECONDS * 60)
        
        self.gif_exporter = GifExporter()
        
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
        
    def input(self, event: WindowEvent):
        # Pass event to pyboy emulator
        self.pyboy.send_input(event)
                

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
    return 
    
            
    @commands.Command
    async def newgame(ctx):
        emulation_stream = EmulationStreamer(ROM_PATH)
        emulation_stream.tick(1800)
        emulation_stream.export_buffer_as_gif()
        emulation_stream.save_state()
        emulation_stream.tick(100)
        emulation_stream.load_state()

    @commands.Command
    async def poke(ctx):
        pass

def setup(client: commands.Bot):
    client.add_cog(emulator(client))