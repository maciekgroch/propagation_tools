import astropy.units as u
import numpy as np
import poppy


@poppy.utils.quantity_input(delta_z=u.meter, wave_lengths=u.meter)
def propagate_incoherent(
        delta_z, wave_lengths, weights, aperture, beam_waist, oversample, npix
):
    """
    A method for computing intensity of light after propagating incoherent
    wave front. The idea is based on [1]. An incoherent wavefront is
    procured as a sum of intensities of wave fronts of different wave lengths
    multiplied by corresponding weights.

    Parameters
    ------------
    :param delta_z: float or astropy.Quantity of type length
        Distnce of propagation
    :param wave_lengths: an iterable of astropy.Quantity of type length
        Wave lengths of composing the incoherent wave front
    :param weights: an iterable
        Weights corresponding to the wave lengths
    :param aperture: poppy.AnalyticOpticalElement
        The wave front is confined by the aperture
    :param beam_waist: astropy.Quantity of type length
        Radius of the illuminated beam at the initial optical plane.
    :param oversample: float
        Padding factor to apply to the wavefront array, multiplying on top of
        the beam radius.
    :param npix: int
        Size of the resulting array (npix * oversample, npix * oversample)

    Returns
    -------
    :return: numpy.array
        Resulting intensity distribution

    References
    ----------
    [1] David G. Voelz, Computational Fourier Optics: A MATLAB Tutorial,
        SPIE Press, 2011

    """

    if len(wave_lengths) != len(weights):
        raise RuntimeError(
            "Each wave length has to have a corresponding weight"
        )

    final_intensity = np.zeros(shape=(npix * oversample, npix * oversample))

    wavelengths_weight = zip(wave_lengths, weights)
    for wave_len, weight in wavelengths_weight:
        wave_front = poppy.FresnelWavefront(
            beam_waist, wavelength=wave_len, npix=npix, oversample=oversample
        )
        wave_front *= aperture
        wave_front.propagate_fresnel(delta_z)
        final_intensity += wave_front.intensity * weight

    return final_intensity
