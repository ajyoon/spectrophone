import math

from PIL import ImageColor
import numpy as np


_MAX_24_BIT_DISTANCE = math.sqrt((255**2) * 3)



def color_similarity_map(image, color, threshold=0):
    """Extract a color similarity channel from an RGB image.

    Computes the euclidian distance of each pixel's RGB color to a given
    color, and returns a numpy array of dimensions height x width and
    dtype 'f2', where 0.0 is the furthest and 1.0 is the closest.

    Args:
        image (Image):
        color (tuple or str): A 0-255 RGB 3-tuple or a hex color string.
        threshold (float): An optional 0-1 threshold value. If provided,
            all similarities below this threshold will be clipped, and values
            above the threshold will be scaled such that values at the
            threshold have similarity of 0 and values at the map's max
            retain their max.
    """

    if isinstance(color, str):
        if not color.startswith('#'):
            color = '#' + color
        color = ImageColor.getcolor(color, 'RGB')

    array = np.array(image)
    subtracted = array - np.array([[[*color]]])
    norm = np.linalg.norm(subtracted, axis=2)
    scaled = (((norm - _MAX_24_BIT_DISTANCE) / (-_MAX_24_BIT_DISTANCE)))
    if threshold != 0:
        offset = np.clip(scaled - threshold, 0, 1)
        return offset * (scaled.max() / offset.max()).astype('f2')
    else:
        return scaled.astype('f2')


def multi_color_similarity_map(image, channel_params):
    """Extract a similarity map using multiple colors and thresholds

    Args:
        image (Image):
        channel_params (list[tuple]): A list of 3-tuples where the first
            value is a color, the second is a threshold, and the third is
            a 0-1 weight multiplier. See `color_similarity_map` for more
            on the color and threshold values.

    Returns: numpy.ndarray
    """
    return np.maximum.reduce([
        color_similarity_map(image, *params[:2]) * params[2]
        for params in channel_params
    ])


def split_into_color_maps(image, colors, threshold):
    return [
        get_color_similarity_map(image, c, threshold)
        for c in colors
    ]
