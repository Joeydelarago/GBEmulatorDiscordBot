import logging
from typing import List, Tuple

from PIL import Image


class GifExporter:
    """Exports list of Pillow Images to gif"""

    @staticmethod
    def create_gif(images, output_path) -> None:
        if not images:
            logging.error("No images to export as gif")
            return
            
        frame_one = images[0]
        frame_one.save(output_path, format="GIF", append_images=images, save_all=True, duration=16, loop=0)

    @staticmethod
    def create_gif_with_facade(images, output_path: str, facade_path: str, image_point: Tuple[int, int]):
        images_with_facade = []

        with Image.open(facade_path) as facade_image:
            for frame in images:

                # Resize Frame to fit facade
                (width, height) = (frame.width * 2, frame.height * 2)
                frame = frame.resize((width, height), Image.ANTIALIAS)

                # Copy facade
                facade_frame = facade_image.copy()

                # Paste frame into facade
                facade_frame.paste(frame, image_point)
                images_with_facade.append(facade_frame)

        GifExporter.create_gif(images_with_facade, output_path)
