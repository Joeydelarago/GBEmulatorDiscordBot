import logging
from typing import List

from PIL import Image

class GifExporter:
    """Exports list of Pillow Images to gif"""
    def __init__(self):
        pass

    @staticmethod
    def create_gif(images, path: str = "output.gif") -> None:
        if not images:
            logging.error("No images to export as gif")
            return
            
        frame_one = images[0]
        frame_one.save(path, format="GIF", append_images=images, save_all=True, duration=16, loop=0)

        screen = Image.open('output.gif', 'r')
        facade = Image.open('gb_facade.png')

        if screen.is_animated:

            frames = []

            for num in range(screen.n_frames):
                screen.seek(num)
                gameboy = Image.new('RGBA', (512,512), (0, 0, 0, 0))
                gameboy.paste(facade, (0,0), mask=facade)
                gameboy.paste(screen, (67,64))
                frames.append(gameboy)

            frames[0].save('gameboy.gif',
                            save_all=True,
                            append_images=frames[1:],
                            duration=100,
                            loop=0)  
