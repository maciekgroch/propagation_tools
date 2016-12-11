import unittest

import astropy.units as u
import numpy as np
import poppy

from propagation_tools.incoherent import propagate_incoherent


class IncoherentPropagationTest(unittest.TestCase):
    def test_propagate_just_one_wavelen(self):
        aperture = poppy.CircularAperture(radius=800 * u.nm)
        npix = 1024
        oversample = 4
        beam_waist = 5 * u.um
        z = 12 * u.um
        wl = [632.8] * u.nm
        weight = [1.]
        intensity = propagate_incoherent(
            z, wl, weight, aperture, beam_waist, oversample, npix
        )
        wave_front = poppy.FresnelWavefront(
            beam_waist, wavelength=wl[0], npix=npix, oversample=oversample
        )
        wave_front *= aperture
        wave_front.propagate_fresnel(z)

        np.testing.assert_almost_equal(intensity, wave_front.intensity)

    def test_raises_when_invalid_shapes(self):
        aperture = poppy.CircularAperture(radius=800 * u.nm)
        npix = 1024
        oversample = 4
        beam_waist = 5 * u.um
        z = 12 * u.um
        wl = [632.8] * u.nm
        weight = [.5, .5]
        with self.assertRaises(RuntimeError):
            intensity = propagate_incoherent(
                z, wl, weight, aperture, beam_waist, oversample, npix
            )

    def test_assert_proper_value(self):
        aperture = poppy.CircularAperture(radius=800 * u.nm)
        npix = 4
        oversample = 16
        beam_waist = 5 * u.um
        z = 12 * u.um
        wl = [632.8] * 4 * u.nm
        weights = [.25] * 4
        intensity = propagate_incoherent(
            z, wl, weights, aperture, beam_waist, oversample, npix
        )
        wave_front = poppy.FresnelWavefront(
            beam_waist, wavelength=wl[0], npix=npix, oversample=oversample
        )
        wave_front *= aperture
        wave_front.propagate_fresnel(z)
        np.testing.assert_almost_equal(intensity, wave_front.intensity)
