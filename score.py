from PIL import Image, ImageOps

import numpy
from tqdm import tqdm


class Score:

    __slots__ = (
        '_image',
        'data',
        'amplitude_map'
    )

    def __init__(self, image_path):
        self._image = Image.open(image_path)
        self.data = numpy.asarray(self._image, dtype=numpy.uint16)
        self.amplitude_map = Score.create_amplitude_map(self._image)

    @staticmethod
    def create_amplitude_map(image):
        out_data = numpy.ndarray((image.size[1], image.size[0]), dtype='f2')
        inverted_greyscale = ImageOps.invert(image.convert('L'))

        for y in tqdm(range(len(out_data)), 'preparing amplitude map'):
            for x in range(len(out_data[0])):
                out_data[y][x] = inverted_greyscale.getpixel((x, y)) / 255
        return out_data
