"""Load CESM2 data."""

from typing import Literal

import numpy as np
import xarray as xr
from volcano_base.load import FindFiles

import paper1_code as core

FINDER = FindFiles()


def get_c2w_aod_rf(
    freq: Literal["y", "ses"] = "y",
) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray]]:
    """Return time, SAOD and RF arrays with seasonal or annual means.

    Parameters
    ----------
    freq : Literal["y", "ses"]
        Whether to return annual (`y`) or seasonal (`ses`) means

    Returns
    -------
    tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray]]
        The time, SAOD and RF arrays in lists of length four, representing the four
        simulation cases "medium", "medium-plus", "strong" and "strong-highlat"

    Raises
    ------
    ValueError
        If the given frequency is none of "y" or "ses"
    """
    shift = None if freq == "ses" else 0
    aod_m, aod_mp, aod_s, aod_ss, aod_h = get_aod_arrs(shift=shift)
    aod = aod_m + aod_mp + aod_s + aod_ss + aod_h
    rf_m, rf_mp, rf_s, rf_ss, rf_h = get_rf_arrs(shift=shift)
    rf = rf_m + rf_mp + rf_s + rf_ss + rf_h
    # Check that they include the same items
    aod = core.utils.time_series.keep_whole_years(aod, freq="MS")
    rf = core.utils.time_series.keep_whole_years(rf, freq="MS")
    if freq == "y":
        return _c2w_y(aod, rf)
    elif freq == "ses":
        return _c2w_ses(aod, rf)
    raise ValueError("freq must be y or ses")


def _finalize_arrays(
    sim_lists: tuple[
        list[xr.DataArray],
        list[xr.DataArray],
        list[xr.DataArray],
        list[xr.DataArray],
        list[xr.DataArray],
    ],
    shift: int | None = None,
    remove_seasonality: bool = False,
) -> tuple[
    list[xr.DataArray],
    list[xr.DataArray],
    list[xr.DataArray],
    list[xr.DataArray],
    list[xr.DataArray],
]:
    m, mp, s, ss, h = sim_lists
    h_shift = 12 if shift is None else 0
    s = core.utils.time_series.shift_arrays(s, daily=False, custom=shift)
    ss = core.utils.time_series.shift_arrays(ss, daily=False, custom=shift)
    mp = core.utils.time_series.shift_arrays(mp, daily=False, custom=shift)
    m = core.utils.time_series.shift_arrays(m, daily=False, custom=shift)
    h = core.utils.time_series.shift_arrays(h, custom=h_shift)
    h = core.utils.time_series.shift_arrays(h, daily=False, custom=shift)
    m = list(xr.align(*m))
    mp = list(xr.align(*mp))
    s = list(xr.align(*s))
    ss = list(xr.align(*ss))
    h = list(xr.align(*h))
    if remove_seasonality:
        # Assume time series are centred at zero and all of the same kind.
        sign = 1  # if abs(m[0].data.min()) < abs(m[0].data.max()) else -1
        for i, a in enumerate(m):
            a.data = a * sign
            m[i] = a.compute()
        for i, a in enumerate(mp):
            a.data = a * sign
            mp[i] = a.compute()
        for i, a in enumerate(s):
            a.data = a * sign
            s[i] = a.compute()
        for i, a in enumerate(ss):
            a.data = a * sign
            ss[i] = a.compute()
        for i, a in enumerate(h):
            a.data = a * sign
            h[i] = a.compute()
        m = core.utils.time_series.shift_arrays(m, daily=False)
        mp = core.utils.time_series.shift_arrays(mp, daily=False)
        s = core.utils.time_series.shift_arrays(s, daily=False)
        ss = core.utils.time_series.shift_arrays(ss, daily=False)
        h = core.utils.time_series.shift_arrays(h, daily=False)
    # Finally shift so the eruption day is at time = 0.
    m = core.utils.time_series.shift_arrays(m, custom=1)
    mp = core.utils.time_series.shift_arrays(mp, custom=1)
    s = core.utils.time_series.shift_arrays(s, custom=1)
    ss = core.utils.time_series.shift_arrays(ss, custom=1)
    h = core.utils.time_series.shift_arrays(h, custom=1)
    for i, array in enumerate(m):
        m[i] = array.assign_coords(time=array.time.data - 1850)
    for i, array in enumerate(mp):
        mp[i] = array.assign_coords(time=array.time.data - 1850)
    for i, array in enumerate(s):
        s[i] = array.assign_coords(time=array.time.data - 1850)
    for i, array in enumerate(ss):
        ss[i] = array.assign_coords(time=array.time.data - 1850)
    for i, array in enumerate(h):
        h[i] = array.assign_coords(time=array.time.data - 1850)
    return m, mp, s, ss, h


def get_aod_arrs(
    remove_seasonality: bool = False, shift: int | None = None
) -> tuple[
    list[xr.DataArray],
    list[xr.DataArray],
    list[xr.DataArray],
    list[xr.DataArray],
    list[xr.DataArray],
]:
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

    def subtract_last_decade_mean(arrs: list, custom_decade: int = 120) -> list:
        # Subtract the mean of the last decade
        for i, arr in enumerate(arrs):
            arr_ = arr[-custom_decade:]
            arr.data = arr.data - arr_.mean().data
            arrs[i] = arr
        return arrs

    data = (
        FINDER.find(
            "e_fSST1850",
            {f"ens{i + 1}" for i in range(5)},
            {"strong", "medium", "medium-plus", "strong-highlat", "size5000"},
            "AODVISstdn",
            "h0",
        )
        .sort("attr", "ensemble")
        .keep_most_recent()
    )
    m = data.copy().keep("medium", {f"ens{i + 2}" for i in range(4)}).load()
    mp = data.copy().keep("medium-plus", {f"ens{i + 2}" for i in range(4)}).load()
    s = data.copy().keep("strong", {f"ens{i + 2}" for i in range(4)}).load()
    ss = data.copy().keep("size5000", {"ens2", "ens4"}).load()
    h = data.copy().keep("strong-highlat", {"ens1", "ens3"}).load()
    s = core.utils.time_series.mean_flatten(s, dims=["lat", "lon"])
    ss = core.utils.time_series.mean_flatten(ss, dims=["lat", "lon"])
    m = core.utils.time_series.mean_flatten(m, dims=["lat", "lon"])
    mp = core.utils.time_series.mean_flatten(mp, dims=["lat", "lon"])
    h = core.utils.time_series.mean_flatten(h, dims=["lat", "lon"])
    # Remove control run
    # s = remove_control(s)
    # m = remove_control(m)
    # mp = remove_control(mp)
    # h = remove_control(h)
    s = subtract_last_decade_mean(s)
    ss = subtract_last_decade_mean(ss)
    m = subtract_last_decade_mean(m)
    mp = subtract_last_decade_mean(mp)
    h = subtract_last_decade_mean(h)
    for i, arr in enumerate(s):
        s[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(ss):
        ss[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(mp):
        mp[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(m):
        m[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(h):
        h[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    # import matplotlib.pyplot as plt
    # [plt.plot(arr.time, arr) for arr in m + mp + s + ss + h]
    return _finalize_arrays((m, mp, s, ss, h), shift, remove_seasonality)


def get_rf_arrs(
    remove_seasonality: bool = False, shift: int | None = None
) -> tuple[
    list[xr.DataArray],
    list[xr.DataArray],
    list[xr.DataArray],
    list[xr.DataArray],
    list[xr.DataArray],
]:
    """Return medium, medium-plus, strong and strong north arrays in lists."""
    control_data = (
        FINDER.find("e_fSST1850", "ens1", "control", "h0", ["FLNT", "FSNT"])
        .sort("attr", "ensemble")
        .keep_most_recent()
    )
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

    def subtract_last_decade_mean(arrs: list, custom_decade: int = 120) -> list:
        # Subtract the mean of the last decade
        for i, arr in enumerate(arrs):
            arr_ = arr[-custom_decade:]
            arr.data = arr.data - arr_.mean().data
            arrs[i] = arr
        return arrs

    data = (
        FINDER.find(
            "e_fSST1850",
            {f"ens{i + 1}" for i in range(5)},
            {"strong", "medium", "medium-plus", "strong-highlat", "size5000"},
            {"FLNT", "FSNT"},
            "h0",
        )
        .sort("attr", "ensemble")
        .keep_most_recent()
    )
    m = data.copy().keep("medium", {f"ens{i + 2}" for i in range(4)}).load()
    mp = data.copy().keep("medium-plus", {f"ens{i + 2}" for i in range(4)}).load()
    s = data.copy().keep("strong", {f"ens{i + 2}" for i in range(4)}).load()
    ss = data.copy().keep("size5000", {"ens2", "ens4"}).load()
    h = data.copy().keep("strong-highlat", {"ens1", "ens3"}).load()
    s = core.utils.time_series.mean_flatten(s, dims=["lat", "lon"])
    ss = core.utils.time_series.mean_flatten(ss, dims=["lat", "lon"])
    m = core.utils.time_series.mean_flatten(m, dims=["lat", "lon"])
    mp = core.utils.time_series.mean_flatten(mp, dims=["lat", "lon"])
    h = core.utils.time_series.mean_flatten(h, dims=["lat", "lon"])
    # Remove control run
    s = difference_and_remove_control(s)
    ss = difference_and_remove_control(ss)
    m = difference_and_remove_control(m)
    mp = difference_and_remove_control(mp)
    h = difference_and_remove_control(h)
    s = subtract_last_decade_mean(s)
    ss = subtract_last_decade_mean(ss)
    m = subtract_last_decade_mean(m)
    mp = subtract_last_decade_mean(mp)
    h = subtract_last_decade_mean(h)
    for i, arr in enumerate(s):
        s[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(ss):
        ss[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(mp):
        mp[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(m):
        m[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(h):
        h[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    # import matplotlib.pyplot as plt
    #
    # fig = plt.figure()
    # fig.suptitle("Normal")
    # [plt.plot(arr.time, arr) for arr in m + mp + s + ss + h]
    return _finalize_arrays((m, mp, s, ss, h), shift, remove_seasonality)


def get_rf_coupled_arrs(
    remove_seasonality: bool = False, shift: int | None = None
) -> tuple[
    list[xr.DataArray],
    list[xr.DataArray],
    list[xr.DataArray],
    list[xr.DataArray],
    list[xr.DataArray],
]:
    """Return medium, medium-plus, strong and strong north arrays in lists."""
    control_data = (
        FINDER.find("e_BWma1850", "ens0", "control", "h0", ["FLNT", "FSNT"])
        .sort("attr", "ensemble")
        .keep_most_recent()
    )
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

    def subtract_last_decade_mean(arrs: list, custom_decade: int = 120) -> list:
        # Subtract the mean of the last decade
        for i, arr in enumerate(arrs):
            arr_ = arr[-custom_decade:]
            arr.data = arr.data - arr_.mean().data
            arrs[i] = arr
        return arrs

    data = (
        FINDER.find(
            "e_BWma1850",
            {f"ens{i + 1}" for i in range(5)},
            {"strong", "medium", "medium-plus", "strong-highlat", "size5000"},
            {"FLNT", "FSNT"},
            "h0",
        )
        .sort("attr", "ensemble")
        .keep_most_recent()
    )
    m = data.copy().keep("medium", {f"ens{i + 2}" for i in range(4)}).load()
    mp = data.copy().keep("medium-plus", {f"ens{i + 2}" for i in range(4)}).load()
    s = data.copy().keep("strong", {f"ens{i + 2}" for i in range(4)}).load()
    ss = data.copy().keep("size5000", {"ens2", "ens4"}).load()
    h = data.copy().keep("strong-highlat", {"ens1", "ens3"}).load()
    s = core.utils.time_series.mean_flatten(s, dims=["lat", "lon"])
    ss = core.utils.time_series.mean_flatten(ss, dims=["lat", "lon"])
    m = core.utils.time_series.mean_flatten(m, dims=["lat", "lon"])
    mp = core.utils.time_series.mean_flatten(mp, dims=["lat", "lon"])
    h = core.utils.time_series.mean_flatten(h, dims=["lat", "lon"])
    # Remove control run
    s = difference_and_remove_control(s)
    ss = difference_and_remove_control(ss)
    m = difference_and_remove_control(m)
    mp = difference_and_remove_control(mp)
    h = difference_and_remove_control(h)
    s = subtract_last_decade_mean(s)
    ss = subtract_last_decade_mean(ss)
    m = subtract_last_decade_mean(m)
    mp = subtract_last_decade_mean(mp)
    h = subtract_last_decade_mean(h)
    for i, arr in enumerate(s):
        s[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(ss):
        ss[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(mp):
        mp[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(m):
        m[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(h):
        h[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    # import matplotlib.pyplot as plt
    #
    # fig = plt.figure()
    # fig.suptitle("Coupled")
    # [plt.plot(arr.time, arr) for arr in m + mp + s + ss + h]
    return _finalize_arrays((m, mp, s, ss, h), shift, remove_seasonality)


def get_trefht_arrs(
    remove_seasonality: bool = False,
    shift: int | None = None,
) -> tuple[
    list[xr.DataArray],
    list[xr.DataArray],
    list[xr.DataArray],
    list[xr.DataArray],
    list[xr.DataArray],
]:
    """Return medium, medium-plus, strong and strong north arrays in lists."""
    data = (
        FINDER.find(
            "e_BWma1850",
            {f"ens{i + 1}" for i in range(5)},
            {"strong", "medium", "medium-plus", "strong-highlat", "size5000"},
            "TREFHT",
            "h0",
        )
        .sort("sim", "attr", "ensemble")
        .keep_most_recent()
    )
    s = data.copy().keep("strong", {f"ens{i + 2}" for i in range(4)}).load()
    ss = data.copy().keep("size5000", {"ens2", "ens4"}).load()
    m = data.copy().keep("medium", {f"ens{i + 2}" for i in range(4)}).load()
    mp = data.copy().keep("medium-plus", {f"ens{i + 2}" for i in range(4)}).load()
    h = data.copy().keep("strong-highlat", {"ens1", "ens3"}).load()
    s = core.utils.time_series.mean_flatten(s, dims=["lat", "lon"])
    ss = core.utils.time_series.mean_flatten(ss, dims=["lat", "lon"])
    m = core.utils.time_series.mean_flatten(m, dims=["lat", "lon"])
    mp = core.utils.time_series.mean_flatten(mp, dims=["lat", "lon"])
    h = core.utils.time_series.mean_flatten(h, dims=["lat", "lon"])
    # Remove control run mean and seasonal variability
    for i, arr in enumerate(s):
        arr.data = arr - core.config.MEANS["TREFHT"]
        a = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
        s[i] = a.compute()
    for i, arr in enumerate(ss):
        arr.data = arr - core.config.MEANS["TREFHT"]
        a = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
        ss[i] = a.compute()
    for i, arr in enumerate(mp):
        arr.data = arr - core.config.MEANS["TREFHT"]
        a = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
        mp[i] = a.compute()
    for i, arr in enumerate(m):
        arr.data = arr - core.config.MEANS["TREFHT"]
        a = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
        m[i] = a.compute()
    for i, arr in enumerate(h):
        arr.data = arr - core.config.MEANS["TREFHT"]
        a = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
        h[i] = a.compute()
    m = core.utils.time_series.remove_seasonality(m, radius=0.1)
    mp = core.utils.time_series.remove_seasonality(mp, radius=0.1)
    s = core.utils.time_series.remove_seasonality(s, radius=0.1)
    ss = core.utils.time_series.remove_seasonality(ss, radius=0.1)
    h = core.utils.time_series.remove_seasonality(h, radius=0.1)
    # import matplotlib.pyplot as plt
    # [plt.plot(arr.time, arr) for arr in m + mp + s + ss + h]
    return _finalize_arrays((m, mp, s, ss, h), shift, remove_seasonality)


def _c2w_ses(aod, rf) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray]]:
    aod = core.utils.time_series.shift_arrays(aod, custom=1)
    rf = core.utils.time_series.shift_arrays(rf, custom=1)
    for i, (arr1, arr2) in enumerate(zip(aod, rf, strict=True)):
        aod[i] = arr1[: int(4 * 12)]
        rf[i] = arr2[: int(4 * 12)]
    simulations_num = 5
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
            case str(x) if "size5000" in x:
                i = 4
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
                i = 3
            case str(x) if "strong" in x:
                i = 2
            case str(x) if "size5000" in x:
                i = 4
            case str(x) if "double-overlap" in x:
                i = 5
            case _:
                raise ValueError(f"There is no simulation with {a.sim}")
        aod_ar[i] = np.r_[aod_ar[i], weighter(a_).data]
        time_ar[i] = np.r_[time_ar[i], weighter(a_).time.data]
        rf_ar[i] = np.r_[rf_ar[i], weighter(c_).data]
    return time_ar, aod_ar, rf_ar


def get_so2_c2w_peaks() -> tuple[float, float, float, float, float]:
    """Return the amount of injected SO2 for the three different eruption magnitudes."""
    return 26, 400, 1629, 3000, 1629


def get_aod_c2w_peaks() -> tuple[float, float, float, float, float]:
    """Get the SAOD peak from the CESM2 simulations."""
    m_, mp_, s_, ss_, h_ = get_aod_arrs(shift=0)
    m_ = core.utils.time_series.shift_arrays(m_, daily=False)
    mp_ = core.utils.time_series.shift_arrays(mp_, daily=False)
    s_ = core.utils.time_series.shift_arrays(s_, daily=False)
    ss_ = core.utils.time_series.shift_arrays(ss_, daily=False)
    h_ = core.utils.time_series.shift_arrays(h_, daily=False)
    s = core.utils.time_series.get_median(s_, xarray=True)
    ss = core.utils.time_series.get_median(ss_, xarray=True)
    mp = core.utils.time_series.get_median(mp_, xarray=True)
    m = core.utils.time_series.get_median(m_, xarray=True)
    h = core.utils.time_series.get_median(h_, xarray=True)
    v = "rolling"
    return (
        core.utils.time_series.find_peak(m, version=v),
        core.utils.time_series.find_peak(mp, version=v),
        core.utils.time_series.find_peak(s, version=v),
        core.utils.time_series.find_peak(ss, version=v),
        core.utils.time_series.find_peak(h, version=v),
    )


def get_rf_c2w_peaks() -> tuple[float, float, float, float, float]:
    """Get the radiative forcing peak from the CESM2 simulations."""
    m_, mp_, s_, ss_, h_ = get_rf_arrs(shift=0)
    m_ = core.utils.time_series.shift_arrays(m_, daily=False)
    mp_ = core.utils.time_series.shift_arrays(mp_, daily=False)
    s_ = core.utils.time_series.shift_arrays(s_, daily=False)
    ss_ = core.utils.time_series.shift_arrays(ss_, daily=False)
    h_ = core.utils.time_series.shift_arrays(h_, daily=False)
    s = core.utils.time_series.get_median(s_, xarray=True)
    ss = core.utils.time_series.get_median(ss_, xarray=True)
    mp = core.utils.time_series.get_median(mp_, xarray=True)
    m = core.utils.time_series.get_median(m_, xarray=True)
    h = core.utils.time_series.get_median(h_, xarray=True)
    s.data *= -1
    ss.data *= -1
    mp.data *= -1
    m.data *= -1
    h.data *= -1

    v = "rolling"
    return (
        core.utils.time_series.find_peak(m, version=v),
        core.utils.time_series.find_peak(mp, version=v),
        core.utils.time_series.find_peak(s, version=v),
        core.utils.time_series.find_peak(ss, version=v),
        core.utils.time_series.find_peak(h, version=v),
    )


def get_rf_coupled_c2w_peaks() -> tuple[float, float, float, float, float]:
    """Get the radiative forcing peak from the CESM2 simulations."""
    m_, mp_, s_, ss_, h_ = get_rf_coupled_arrs(shift=0)
    m_ = core.utils.time_series.shift_arrays(m_, daily=False)
    mp_ = core.utils.time_series.shift_arrays(mp_, daily=False)
    s_ = core.utils.time_series.shift_arrays(s_, daily=False)
    ss_ = core.utils.time_series.shift_arrays(ss_, daily=False)
    h_ = core.utils.time_series.shift_arrays(h_, daily=False)
    s = core.utils.time_series.get_median(s_, xarray=True)
    ss = core.utils.time_series.get_median(ss_, xarray=True)
    mp = core.utils.time_series.get_median(mp_, xarray=True)
    m = core.utils.time_series.get_median(m_, xarray=True)
    h = core.utils.time_series.get_median(h_, xarray=True)
    s.data *= -1
    ss.data *= -1
    mp.data *= -1
    m.data *= -1
    h.data *= -1
    v = "rolling"
    return (
        core.utils.time_series.find_peak(m, version=v),
        core.utils.time_series.find_peak(mp, version=v),
        core.utils.time_series.find_peak(s, version=v),
        core.utils.time_series.find_peak(ss, version=v),
        core.utils.time_series.find_peak(h, version=v),
    )


def get_trefht_c2w_peaks() -> tuple[float, float, float, float, float]:
    """Get the temperature peak from the CESM2 simulations."""
    m_, mp_, s_, ss_, h_ = get_trefht_arrs(shift=0)
    m_ = core.utils.time_series.shift_arrays(m_, daily=False)
    mp_ = core.utils.time_series.shift_arrays(mp_, daily=False)
    s_ = core.utils.time_series.shift_arrays(s_, daily=False)
    ss_ = core.utils.time_series.shift_arrays(ss_, daily=False)
    h_ = core.utils.time_series.shift_arrays(h_, daily=False)
    s = core.utils.time_series.get_median(s_, xarray=True)
    ss = core.utils.time_series.get_median(ss_, xarray=True)
    mp = core.utils.time_series.get_median(mp_, xarray=True)
    m = core.utils.time_series.get_median(m_, xarray=True)
    h = core.utils.time_series.get_median(h_, xarray=True)
    s.data *= -1
    ss.data *= -1
    mp.data *= -1
    m.data *= -1
    h.data *= -1
    v = "rolling"
    return (
        core.utils.time_series.find_peak(m, version=v),
        core.utils.time_series.find_peak(mp, version=v),
        core.utils.time_series.find_peak(s, version=v),
        core.utils.time_series.find_peak(ss, version=v),
        core.utils.time_series.find_peak(h, version=v),
    )
