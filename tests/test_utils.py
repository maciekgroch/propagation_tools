from PIL import Image
import os
import unittest

import numpy as np

from propagation_tools.utils import (
    create_amp_normalized_entire_wavefront,
    save_as_image,
    MAX_VALUE_FOR_IMAGES
)


class SaveAsImageTest(unittest.TestCase):
    def test_save(self):
        img_path = os.path.abspath('img.bmp')
        self.addCleanup(os.remove, img_path)

        wavefront = np.ones((1024, 1024))
        save_as_image(wavefront, img_path)
        img = Image.open(img_path)
        img = img.convert("L")
        reloaded_wavefront = np.asarray(img).copy()
        reloaded_wavefront *= MAX_VALUE_FOR_IMAGES
        np.testing.assert_almost_equal(reloaded_wavefront, wavefront)

    def test_save_max_zero(self):
        img_path = os.path.abspath('img_0.bmp')
        self.addCleanup(os.remove, img_path)

        wavefront = np.zeros((1024, 1024))
        save_as_image(wavefront, img_path)
        img = Image.open(img_path)
        img = img.convert("L")
        reloaded_wavefront = np.asarray(img)
        np.testing.assert_almost_equal(reloaded_wavefront, wavefront)


class NormalizeAmplitudeTest(unittest.TestCase):
    def test_normalize_entire_wavefront(self):
        shape = (100, 100)
        wf = np.zeros(shape, dtype=complex)
        wf += 10. + 12.j
        wf[10, :] = 0. + 0.j
        wf = create_amp_normalized_entire_wavefront(wf)
        amplitude = np.abs(wf)
        right_answer = np.ones(shape, dtype=float)
        np.testing.assert_almost_equal(amplitude, right_answer)

    def test_normalize_phase_unchanged(self):
        shape = (100, 100)
        wf = np.zeros(shape, dtype=complex)
        wf += 10. + 12.j
        wf[10, :] = 0. + 0.j
        wf_normalized = create_amp_normalized_entire_wavefront(wf)
        correct_phase = np.angle(wf)
        phase_after_normalizaiation = np.angle(wf_normalized)
        np.testing.assert_almost_equal(
            phase_after_normalizaiation, correct_phase
        )

