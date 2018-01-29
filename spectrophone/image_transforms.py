from PIL import Image


def get_color_similarity_channel(image, red, green, blue):

    return image.convert(
        mode='L',
        matrix=(
            red / 255,
            green / 255,
            blue / 255,
            0
        ))
