import numpy as np
from PIL import Image


MAX_VALUE_FOR_IMAGES = 255


def save_as_image(array, file_name, file_format='bmp', mode='L'):
    normalized_to_img = array * MAX_VALUE_FOR_IMAGES / array.max()
    img = Image.fromarray(normalized_to_img, mode)
    img.save(file_name, file_format)
