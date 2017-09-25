import gc

import numpy as np
from PIL import Image, ImageOps


class Score:

    __slots__ = (
        'amplitude_map'
    )

    def __init__(self, image_path):
        image = Image.open(image_path)
        self.amplitude_map = Score.create_amplitude_map(image)
        gc.collect()  # Memory tends to balloon in this init,
                      # so try to get it back under control

    @staticmethod
    def create_amplitude_map(image):
        print('preparing amplitude map')
        inverted_greyscale = ImageOps.invert(image.convert('L'))
        return np.asarray(inverted_greyscale, dtype='f2') / 255
