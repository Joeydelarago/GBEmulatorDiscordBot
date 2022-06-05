from typing import List
from PIL.Image import Image
from pyboy import PyBoy
from time import time

from pyboy.utils import WindowEvent

ROM_PATH='roms/pokemon-red.gb'
BUFFER_SECONDS=3 # buffer size in seconds


class EmulationStreamer():
    def __init__(self, rom_path: str):
        self.pyboy = PyBoy(rom_path)
        
        # This will try to emulate as fast as possible
        self.pyboy.set_emulation_speed(0)
        
        # Fill the buffer to avoid assigning extra memory, each second is 60 images
        self.image_buffer = ImageBuffer(BUFFER_SECONDS * 60)
        
        self.gif_exporter = GifExporter()
        
        self.tick(1800)
        
        # Saving init
        self.save_slot = 0
        self.save_prefix = "state_file_"
        self.save_postfix = ".state" 
        
    def tick(self, tick_count: int) -> None:
        for t in range(tick_count):
            self.pyboy.tick()
            self.image_buffer.push(self.pyboy.screen_image())
            
    def export_buffer(self):
        # Export buffer as gif
        self.gif_exporter.create_gif(self.image_buffer.get_all())
        
    def save_state(self):
        save_name = self.save_prefix + str(self.save_slot) + self.save_postfix
        with open(save_name, "wb") as save_file:
            self.pyboy.save_state(save_file)

    def load_state(self):
        save_name = self.save_prefix + str(self.save_slot) + self.save_postfix
        with open(save_name, "rb") as save_file:
            self.pyboy.load_state(save_file)
        
    def input(self):
        self.pyboy.send_input(WindowEvent.PRESS_ARROW_DOWN)
            
            

class GifExporter():
    def __init__(self):
        pass
    
    def create_gif(self, images: List[Image]):
        frame_one = images[0]
        frame_one.save("output.gif", format="GIF", append_images=images, save_all=True, duration=16, loop=0)


class ImageBuffer():
    def __init__(self, size: int):
        self.size = size
        self.index = 0
        self.buffer = [None] * size
        
    def push(self, item) -> None:
        self.buffer[self.index] = item
        self.index = (self.index + 1) % self.size
        
    def get_all(self) -> List:
        # Return everything in buffer in order starting with buffer_index
        return self.buffer[self.index:] + self.buffer[0:self.index]
        
        


if __name__ == "__main__":
    emulation_stream = EmulationStreamer(ROM_PATH)
    emulation_stream.export_buffer()
    emulation_stream.save_state()
    emulation_stream.tick(100)
    emulation_stream.load_state()
    emulation_stream.tick(100)