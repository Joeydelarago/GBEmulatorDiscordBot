import logging
from typing import List

from PIL import Image

class GifExporter:
    """Exports list of Pillow Images to gif"""
    def __init__(self):
        pass
    
    def add_facade(self, frame):
        facade = Image.open('resources/Gameboy.png')

        # Resize frame by 2
        (width, height) = (frame.width * 2, frame.height * 2)
        frame = frame.resize((width, height), Image.ANTIALIAS)

        # Join frame and facade to the buffer
        gameboy = Image.new('RGBA', (512, 700), (0, 0, 0, 0))
        gameboy.paste(facade, (0,0), mask=facade)
        gameboy.paste(frame, (66,69))
        return gameboy

    @staticmethod
    def create_gif(images, path: str = "output.gif") -> None:
        if not images:
            logging.error("No images to export as gif")
            return
            
        frame_one = images[0]
        frame_one.save(path, format="GIF", append_images=images, save_all=True, duration=16, loop=0)