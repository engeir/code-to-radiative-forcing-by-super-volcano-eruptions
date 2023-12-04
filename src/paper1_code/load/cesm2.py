"""Load CESM2 data."""

from typing import Literal

import numpy as np
import scipy
import xarray as xr

import paper1_code as core
from paper1_code.utils.find_c2w_files import FindFiles

FINDER = FindFiles()


def get_c2w_aod_rf(
    freq: Literal["y", "ses"] = "y"
) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray]]:
    """Return time, AOD and RF arrays with seasonal or annual means.

    Parameters
    ----------
    freq : Literal["y", "ses"]
        Whether to return annual (`y`) or seasonal (`ses`) means

    Returns
    -------
    tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray]]
        The time, AOD and RF arrays in lists of length four, representing the four
        simulation cases "medium", "medium-plus", "strong" and "strong-highlat"

    Raises
    ------
    ValueError
        If the given frequency is none of "y" or "ses"
    """
    shift = None if freq == "ses" else 0
    aod_m, aod_mp, aod_s, aod_h = get_aod_arrs(shift=shift)
    aod = aod_m + aod_mp + aod_s + aod_h
    rf_m, rf_mp, rf_s, rf_h = get_rf_arrs(shift=shift)
    rf = rf_m + rf_mp + rf_s + rf_h
    # Check that they include the same items
    aod = core.utils.time_series.keep_whole_years(aod, freq="MS")
    rf = core.utils.time_series.keep_whole_years(rf, freq="MS")
    if freq == "y":
        return _c2w_y(aod, rf)
    elif freq == "ses":
        return _c2w_ses(aod, rf)
    raise ValueError("freq must be y or ses")


def get_aod_arrs(
    remove_seasonality: bool = False, shift: int | None = None
) -> tuple[list[xr.DataArray], ...]:
    """Return medium, medium-plus, strong and strong north arrays in lists."""
    control_match = FINDER.find("e_fSST1850", "control", "AODVISstdn", "h0", "ens0")
    control = control_match.load()
    control = core.utils.time_series.mean_flatten(control, dims=["lat", "lon"])

    def remove_control(arrs: list) -> list:
        # The control is so small it hardly has any effect, but we do it still for
        # consistency
        for i, arr in enumerate(arrs):
            arr_, ctrl = xr.align(arr, control[0])
            arr_.data = arr_.data - ctrl.data
            arrs[i] = arr_
        return arrs

    data = FINDER.find(
        "e_fSST1850",
        {f"ens{i+1}" for i in range(4)},
        {"strong", "medium", "medium-plus", "strong-highlat"},
        "AODVISstdn",
        "h0",
    ).sort("attr", "ensemble")
    m = data.copy().keep("medium").load()
    mp = data.copy().keep("medium-plus").load()
    s = data.copy().keep("strong").load()
    h = data.copy().keep("strong-highlat").load()

    s = core.utils.time_series.mean_flatten(s, dims=["lat", "lon"])
    m = core.utils.time_series.mean_flatten(m, dims=["lat", "lon"])
    mp = core.utils.time_series.mean_flatten(mp, dims=["lat", "lon"])
    h = core.utils.time_series.mean_flatten(h, dims=["lat", "lon"])
    s = remove_control(s)
    m = remove_control(m)
    mp = remove_control(mp)
    h = remove_control(h)
    h_shift = 12 if shift is None else 0
    s = core.utils.time_series.shift_arrays(s, daily=False, custom=shift)
    mp = core.utils.time_series.shift_arrays(mp, daily=False, custom=shift)
    m = core.utils.time_series.shift_arrays(m, daily=False, custom=shift)
    h = core.utils.time_series.shift_arrays(h, custom=h_shift)
    h = core.utils.time_series.shift_arrays(h, daily=False, custom=shift)
    for i, arr in enumerate(s):
        s[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(mp):
        mp[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(m):
        m[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(h):
        h[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    m = list(xr.align(*m))
    mp = list(xr.align(*mp))
    s = list(xr.align(*s))
    h = list(xr.align(*h))
    if remove_seasonality:
        m = core.utils.time_series.shift_arrays(m, daily=False)
        mp = core.utils.time_series.shift_arrays(mp, daily=False)
        s = core.utils.time_series.shift_arrays(s, daily=False)
        h = core.utils.time_series.shift_arrays(h, daily=False)
    return m, mp, s, h


def get_rf_arrs(
    remove_seasonality: bool = False, shift: int | None = None
) -> tuple[list[xr.DataArray], ...]:
    """Return medium, medium-plus, strong and strong north arrays in lists."""
    control_data = FINDER.find(
        "e_fSST1850", "ens0", "control", "h0", ["FLNT", "FSNT"]
    ).sort("attr", "ensemble")
    control = control_data.load()
    control = core.utils.time_series.mean_flatten(control, dims=["lat", "lon"])

    def difference_and_remove_control(arrs: list) -> list:
        stop = len(arrs) // 2
        for i, arr in enumerate(arrs):
            if i > stop - 1:
                arrs = arrs[:stop]
                break
            fsnt, flnt, ctrl_fsnt, ctrl_flnt = xr.align(
                arrs[i + stop], arr, control[1], control[0]
            )
            flnt.data = fsnt.data - flnt.data - (ctrl_fsnt.data - ctrl_flnt.data)
            flnt = flnt.assign_attrs(attr="RF")
            arrs[i] = flnt
        return arrs

    data = FINDER.find(
        "e_fSST1850",
        {f"ens{i+1}" for i in range(4)},
        {"strong", "medium", "medium-plus", "strong-highlat"},
        {"FLNT", "FSNT"},
        "h0",
    ).sort("attr", "ensemble")
    m_ = data.copy().keep("medium").load()
    mp_ = data.copy().keep("medium-plus").load()
    s_ = data.copy().keep("strong").load()
    h_ = data.copy().keep("strong-highlat").load()
    s_ = core.utils.time_series.mean_flatten(s_, dims=["lat", "lon"])
    m_ = core.utils.time_series.mean_flatten(m_, dims=["lat", "lon"])
    mp_ = core.utils.time_series.mean_flatten(mp_, dims=["lat", "lon"])
    h_ = core.utils.time_series.mean_flatten(h_, dims=["lat", "lon"])
    # Find difference and subtract control
    s_ = difference_and_remove_control(s_)
    m_ = difference_and_remove_control(m_)
    mp_ = difference_and_remove_control(mp_)
    h_ = difference_and_remove_control(h_)
    h_shift = 12 if shift is None else 0
    s_ = core.utils.time_series.shift_arrays(s_, daily=False, custom=shift)
    mp_ = core.utils.time_series.shift_arrays(mp_, daily=False, custom=shift)
    m_ = core.utils.time_series.shift_arrays(m_, daily=False, custom=shift)
    h_ = core.utils.time_series.shift_arrays(h_, custom=h_shift)
    h_ = core.utils.time_series.shift_arrays(h_, daily=False, custom=shift)
    for i, arr in enumerate(s_):
        s_[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(mp_):
        mp_[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(m_):
        m_[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(h_):
        h_[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    if remove_seasonality:
        for i, a in enumerate(m_):
            a.data = (a) * (-1)
            m_[i] = a.compute()
        for i, a in enumerate(mp_):
            a.data = (a) * (-1)
            mp_[i] = a.compute()
        for i, a in enumerate(s_):
            a.data = (a) * (-1)
            s_[i] = a.compute()
        for i, a in enumerate(h_):
            a.data = (a) * (-1)
            h_[i] = a.compute()
        m_ = core.utils.time_series.shift_arrays(m_, daily=False)
        mp_ = core.utils.time_series.shift_arrays(mp_, daily=False)
        s_ = core.utils.time_series.shift_arrays(s_, daily=False)
        h_ = core.utils.time_series.shift_arrays(h_, daily=False)
    return m_, mp_, s_, h_


def get_trefht_arrs(
    remove_seasonality: bool = False
) -> tuple[
    list[xr.DataArray], list[xr.DataArray], list[xr.DataArray], list[xr.DataArray]
]:
    """Return medium, medium-plus, strong and strong north arrays in lists."""
    data = FINDER.find(
        "e_BWma1850",
        {f"ens{i+1}" for i in range(4)},
        {"strong", "medium", "medium-plus", "strong-highlat"},
        "TREFHT",
        "h0",
    ).sort("sim", "attr", "ensemble")
    s = data.copy().keep("strong").load()
    m = data.copy().keep("medium").load()
    mp = data.copy().keep("medium-plus").load()
    h = data.copy().keep("strong-highlat").load()
    s = core.utils.time_series.mean_flatten(s, dims=["lat", "lon"])
    m = core.utils.time_series.mean_flatten(m, dims=["lat", "lon"])
    mp = core.utils.time_series.mean_flatten(mp, dims=["lat", "lon"])
    h = core.utils.time_series.mean_flatten(h, dims=["lat", "lon"])
    for i, arr in enumerate(s):
        s[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    s = list(xr.align(*s))
    for i, arr in enumerate(mp):
        mp[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    mp = list(xr.align(*mp))
    for i, arr in enumerate(m):
        m[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    m = list(xr.align(*m))
    for i, arr in enumerate(h):
        h[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    h = list(xr.align(*h))
    if remove_seasonality:
        for i, a in enumerate(m):
            a.data = (a - core.config.MEANS["TREFHT"]) * (-1)
            m[i] = a.compute()
        for i, a in enumerate(mp):
            a.data = (a - core.config.MEANS["TREFHT"]) * (-1)
            mp[i] = a.compute()
        for i, a in enumerate(s):
            a.data = (a - core.config.MEANS["TREFHT"]) * (-1)
            s[i] = a.compute()
        for i, a in enumerate(h):
            a.data = (a - core.config.MEANS["TREFHT"]) * (-1)
            h[i] = a.compute()
        m = core.utils.time_series.remove_seasonality(m, radius=0.1)
        mp = core.utils.time_series.remove_seasonality(mp, radius=0.1)
        s = core.utils.time_series.remove_seasonality(s, radius=0.1)
        h = core.utils.time_series.remove_seasonality(h, radius=0.1)
    m = core.utils.time_series.shift_arrays(m, daily=False)
    mp = core.utils.time_series.shift_arrays(mp, daily=False)
    s = core.utils.time_series.shift_arrays(s, daily=False)
    h = core.utils.time_series.shift_arrays(h, daily=False)
    return m, mp, s, h


def _c2w_ses(aod, rf) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray]]:
    aod = core.utils.time_series.shift_arrays(aod, custom=1)
    rf = core.utils.time_series.shift_arrays(rf, custom=1)
    for i, (arr1, arr2) in enumerate(zip(aod, rf, strict=True)):
        aod[i] = arr1[: int(4 * 12)]
        rf[i] = arr2[: int(4 * 12)]
    simulations_num = 4
    time_ar = [np.array([])] * simulations_num
    aod_ar = [np.array([])] * simulations_num
    rf_ar = [np.array([])] * simulations_num
    weighter_ses = core.utils.time_series.weighted_season_avg
    for a, c in zip(aod, rf, strict=True):
        # Place the arrays in lists based on eruption strength
        a_, c_ = xr.align(a, c)
        match a.sim:
            case str(x) if "medium-plus" in x:
                i = 1
            case str(x) if "medium" in x:
                i = 0
            case str(x) if "strong-highlat" in x:
                i = 3
            case str(x) if "strong" in x:
                i = 2
            case _:
                raise ValueError(f"There is no simulation with {a.sim}")
        aod_ar[i] = np.r_[aod_ar[i], weighter_ses(a_).data]
        time_ar[i] = np.r_[time_ar[i], weighter_ses(a_).time.data]
        rf_ar[i] = np.r_[rf_ar[i], weighter_ses(c_).data]
    for i, arrs in enumerate(time_ar):
        # t.month = 1, 4, 7, 10 -> 0, 0.25, 0.5, 0.75
        time_ar[i] = np.asarray([str(t.year + (t.month - 1) / 12) for t in arrs])
    return time_ar, aod_ar, rf_ar


def _c2w_y(aod, rf) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray]]:
    time_ar = [np.array([])] * 6
    aod_ar = [np.array([])] * 6
    rf_ar = [np.array([])] * 6
    weighter = core.utils.time_series.weighted_year_avg
    for a, c in zip(aod, rf, strict=True):
        # Place the arrays in lists based on eruption strength
        a_, c_ = xr.align(a, c)
        match a.sim:
            case str(x) if "medium-plus" in x:
                i = 1
            case str(x) if "medium" in x:
                i = 0
            case str(x) if "strong-highlat" in x:
                i = 5
            case str(x) if "strong" in x:
                i = 2
            case str(x) if "double-overlap" in x:
                i = 3
            case _:
                raise ValueError(f"There is no simulation with {a.sim}")
        aod_ar[i] = np.r_[aod_ar[i], weighter(a_).data]
        time_ar[i] = np.r_[time_ar[i], weighter(a_).time.data]
        rf_ar[i] = np.r_[rf_ar[i], weighter(c_).data]
    return time_ar, aod_ar, rf_ar


def get_so2_c2w_peaks() -> tuple[float, float, float]:
    """Return the amount of injected SO2 for the three different eruption magnitudes."""
    return 26, 400, 1629


def get_aod_c2w_peaks() -> tuple[float, float, float, float]:
    """Get the AOD peak from the CESM2 simulations."""
    m_, mp_, s_, h_ = get_aod_arrs(shift=0)
    s = core.utils.time_series.get_median(s_, xarray=True)
    mp = core.utils.time_series.get_median(mp_, xarray=True)
    m = core.utils.time_series.get_median(m_, xarray=True)
    h = core.utils.time_series.get_median(h_, xarray=True)
    return (
        scipy.signal.savgol_filter(m.data, 12, 3).max(),
        scipy.signal.savgol_filter(mp.data, 12, 3).max(),
        scipy.signal.savgol_filter(s.data, 12, 3).max(),
        scipy.signal.savgol_filter(h.data, 12, 3).max(),
    )


def get_rf_c2w_peaks() -> tuple[float, float, float, float]:
    """Get the radiative forcing peak from the CESM2 simulations."""
    m_, mp_, s_, h_ = get_rf_arrs(shift=0)
    s = core.utils.time_series.get_median(s_, xarray=True)
    mp = core.utils.time_series.get_median(mp_, xarray=True)
    m = core.utils.time_series.get_median(m_, xarray=True)
    h = core.utils.time_series.get_median(h_, xarray=True)
    s.data *= -1
    mp.data *= -1
    m.data *= -1
    h.data *= -1
    return (
        scipy.signal.savgol_filter(m.data, 12, 3).max(),
        scipy.signal.savgol_filter(mp.data, 12, 3).max(),
        scipy.signal.savgol_filter(s.data, 12, 3).max(),
        scipy.signal.savgol_filter(h.data, 12, 3).max(),
    )


def get_trefht_c2w_peaks() -> tuple[float, float, float, float]:
    """Get the temperature peak from the CESM2 simulations."""
    m_, mp_, s_, h_ = get_trefht_arrs()
    s = core.utils.time_series.get_median(s_, xarray=True)
    mp = core.utils.time_series.get_median(mp_, xarray=True)
    m = core.utils.time_series.get_median(m_, xarray=True)
    h = core.utils.time_series.get_median(h_, xarray=True)
    s.data = (s - core.config.MEANS["TREFHT"]) * (-1)
    mp.data = (mp - core.config.MEANS["TREFHT"]) * (-1)
    m.data = (m - core.config.MEANS["TREFHT"]) * (-1)
    h.data = (h - core.config.MEANS["TREFHT"]) * (-1)
    return (
        scipy.signal.savgol_filter(m.data, 12, 3).max(),
        scipy.signal.savgol_filter(mp.data, 12, 3).max(),
        scipy.signal.savgol_filter(s.data, 12, 3).max(),
        scipy.signal.savgol_filter(h.data, 12, 3).max(),
    )
