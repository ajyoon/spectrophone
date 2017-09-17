from PIL import Image
import numpy


class Score:

    def __init__(self, image_path):
        self._image = Image.open(image_path)
        self.data = numpy.asarray(self._image, dtype=numpy.uint16)
