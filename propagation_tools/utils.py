import numpy as np
from PIL import Image

MAX_VALUE_FOR_IMAGES = 255


def create_amp_normalized_entire_wavefront(wavefront):
    """
    A method for normalizing amplitude of a wavefront. Phase should be
    left unchanged.

    Parameters
    ------------
    :param wavefront: numpy.array
        Complex array (wavefront) to normalize
    Returns
    -------
    :return: numpy.array
        Amplitude-normalized wavefront

    """
    with np.errstate(divide='ignore', invalid='ignore'):
        amplitude = np.abs(wavefront)
        normalized = np.true_divide(wavefront, amplitude)
        normalized[np.isnan(normalized)] = 1. + 0.j  # amp = 1, phase = 0

    return normalized


def save_as_image(array, file_path):
    """
    A method for saving array as bitmap. It is normalized so that the max
    value corresponds to 255 (white) and min to 0 (black).

    Parameters
    ------------
    :param array: numpy.array
        Array to be sized as an image
    :param file_path: string
        Path of the file. Should contain format
    """
    file_format = file_path.split('.')[-1]
    normalized_to_img = array.copy()
    if array.max() != 0:
        normalized_to_img *= MAX_VALUE_FOR_IMAGES / array.max()

    img = Image.fromarray(normalized_to_img)
    img = img.convert("RGB")
    img.save(file_path, file_format)
