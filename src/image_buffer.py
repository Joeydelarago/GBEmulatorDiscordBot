from typing import List


class ImageBuffer:
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
        ordered_frames = self.buffer[self.index:] + self.buffer[0:self.index]
        return [frame for frame in ordered_frames if frame is not None]