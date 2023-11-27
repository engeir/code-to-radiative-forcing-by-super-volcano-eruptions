"""Implement a simple function that removes frequencies from time series."""

import cftime
import matplotlib.pyplot as plt
import numpy as np
import scipy
import xarray as xr


def remove_seasonality(
    arrays: list[xr.DataArray] | xr.DataArray,
    freq: float = 1.0,
    radius: float = 0.01,
    plot: bool = False,
) -> list[xr.DataArray] | xr.DataArray:
    """Remove seasonality from array.

    Parameters
    ----------
    arrays : list[xr.DataArray] | xr.DataArray
        An array or a list of arrays to remove seasonality from
    freq : float
        Gives the frequency that should be removed when using the Fourier method
    radius : float
        Gives the frequency range that should be removed when using the Fourier method
    plot : bool
        Will plot what is removed in the Fourier domain

    Returns
    -------
    list[xr.DataArray] | xr.DataArray
        An object of the same arrays as the input, but modified

    Raises
    ------
    NameError
        If a seasonality removing strategy is not found.
    """
    if isinstance(arrays, xr.DataArray):
        return _remove_seasonality_fourier(arrays.copy(), freq, radius, plot)
    array = arrays[:]
    for i, arr in enumerate(array):
        # Need to re-assign `arr`, otherwise it will be re-used
        array[i] = _remove_seasonality_fourier(arr, freq, radius, plot)
    return array[:]


def _remove_seasonality_fourier(
    arr: xr.DataArray, freq: float, radius: float, plot: bool
) -> xr.DataArray:
    """Remove seasonality via Fourier transform.

    Parameters
    ----------
    arr : xr.DataArray
        An xarray DataArray.
    frequency : float
        Give a custom frequency that should be removed. Default is 1.
    radius : float
        Give a custom radius that should be removed. Default is 0.01.
    plot : bool
        Will plot what is removed in the Fourier domain

    Returns
    -------
    xr.DataArray
        An xarray DataArray.

    Raises
    ------
    TypeError
        If the time axis type is not recognised and we cannot translate to frequency.
    """
    if isinstance(arr.time.data[0], float):
        sample_spacing = arr.time.data[1] - arr.time.data[0]
    elif isinstance(arr.time.data, xr.CFTimeIndex | np.ndarray) and isinstance(
        arr.time.data[0], cftime.datetime
    ):
        sec_in_year = 3600 * 24 * 365
        sample_spacing = (
            arr.time.data[11] - arr.time.data[10]
        ).total_seconds() / sec_in_year
    else:
        raise TypeError(
            f"I cannot handle time arrays where {type(arr.time.data) = } and"
            f" {type(arr.time.data[0]) = }. The array must be a numpy.ndarray or"
            " xr.CFTimeIndex, and the elements must be floats or cftime.datetime."
        )
    n = len(arr.time.data)
    yf = scipy.fft.rfft(arr.data)
    xf = scipy.fft.rfftfreq(n, sample_spacing)
    idx = np.argwhere((xf > freq - radius) & (xf < freq + radius))
    yf_clean = yf.copy()
    if any(idx):
        linear_fill = np.linspace(
            yf_clean[idx[0] - 1], yf_clean[idx[-1] + 1], len(yf_clean[idx])
        )
        yf_clean[idx] = linear_fill
    else:
        print(
            "WARNING: No frequencies were removed! The radius is probably too small,"
            " try with a larger one."
        )
        print(
            "HINT: You can also view the before/after of this function by pasing in"
            " the `plot=True` keyword argument."
        )
    new_f_clean = scipy.fft.irfft(yf_clean)
    if plot:
        plt.semilogy(xf, np.abs(yf))
        plt.semilogy(xf, np.abs(yf_clean))
        plt.xlim([-1, 10])
        plt.show()
    arr.data[: len(new_f_clean)] = new_f_clean

    return arr[:]
