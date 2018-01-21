import numpy as np
from PIL import Image, ImageOps


class Score:

    __slots__ = (
        'amplitude_map'
    )

    def __init__(self, amplitude_map):
        """Create a Score directly from a 2D amplitude map array.

        To load from an image in memory or from a file, use `Score.from_image`.

        Args:
            amplitude_map (ndarray): A 2D array of 16-bit floats
                where 0 indicates silence and 255 indicates maximum amplitude.
        """
        self.amplitude_map = amplitude_map

    @classmethod
    def from_image(cls, image):
        """
        Args:
            image (Image or str): A PIL Image or a str path to an image file.
        """
        if isinstance(image, Image.Image):
            loaded_image = image
        else:
            loaded_image = Image.open(image)
        return cls(cls.create_amplitude_map(loaded_image))

    @staticmethod
    def create_amplitude_map(image):
        print('preparing amplitude map...')
        inverted_greyscale = ImageOps.invert(image.convert('L'))
        return np.array(inverted_greyscale).astype('f2') / 255
