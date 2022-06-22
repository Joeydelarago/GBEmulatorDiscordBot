import logging
from typing import List

from PIL import Image

class GifExporter:
    """Exports list of Pillow Images to gif"""
    def __init__(self):
        pass
    
    def add_facade(self, frame):
        facade = Image.open('gb_facade.png')
        gameboy = Image.new('RGBA', (512,512), (0, 0, 0, 0))
        gameboy.paste(facade, (0,0), mask=facade)
        gameboy.paste(frame, (69,66))
        return gameboy
          
    @staticmethod
    def create_gif(images, path: str = "output.gif") -> None:
        if not images:
            logging.error("No images to export as gif")
            return
            
        frame_one = images[0]
        frame_one.save(path, format="GIF", append_images=images, save_all=True, duration=16, loop=0)