import logging
from typing import List

from PIL.Image import Image


class GifExporter:
    """Exports list of Pillow Images to gif"""
    def __init__(self):
        pass

    @staticmethod
    def create_gif(images: List[Image], path: str = "output.gif") -> None:
        if not images:
            logging.error("No images to export as gif")
            return
        frame_one = images[0]
        frame_one.save(path, format="GIF", append_images=images, save_all=True, duration=16, loop=0)