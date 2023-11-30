"""Data that is used in several figures are loaded here."""

import datetime
import pathlib
from typing import Literal

import numpy as np
import scipy
import xarray as xr

import paper1_code as core

FINDER = core.utils.load_auto.FindFiles()


def _set_aod_arrs(shift: int | None = None) -> tuple[list[xr.DataArray], ...]:
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
    return m, mp, s, h


def _set_rf_arrs(shift: int | None = None) -> tuple[list[xr.DataArray], ...]:
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
    return m_, mp_, s_, h_


def _set_cesm2_avg(
    freq: Literal["y", "ses"] = "y"
) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray]]:
    shift = None if freq == "ses" else 0
    aod_m, aod_mp, aod_s, aod_h = _set_aod_arrs(shift=shift)
    aod = aod_m + aod_mp + aod_s + aod_h
    rf_m, rf_mp, rf_s, rf_h = _set_rf_arrs(shift=shift)
    rf = rf_m + rf_mp + rf_s + rf_h
    # Check that they include the same items
    aod = core.utils.time_series.keep_whole_years(aod, freq="MS")
    rf = core.utils.time_series.keep_whole_years(rf, freq="MS")
    if freq == "y":
        return _c2w_y(aod, rf)
    elif freq == "ses":
        return _c2w_ses(aod, rf)
    raise ValueError("freq must be y or ses")


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
        # if a.ensemble == c.ensemble and a.sim == c.sim:
        # print(f"Using: {a.ensemble}, {a.sim}")
        # print(f"Using: {c.ensemble}, {c.sim}")
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
        if a.ensemble == c.ensemble and a.sim == c.sim:
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


def get_aod_peak() -> tuple[float, float, float, float]:
    """Get the AOD peak from the CESM2 simulations."""
    m_, mp_, s_, h_ = _set_aod_arrs(shift=0)
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


def get_rf_peak() -> tuple[float, float, float, float]:
    """Get the radiative forcing peak from the CESM2 simulations."""
    m_, mp_, s_, h_ = _set_rf_arrs(shift=0)
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


def _normalize_peaks(
    scale_idx: int = 0, *args: tuple[list | np.ndarray, str]
) -> tuple[list, ...]:
    out: list[list] = []
    win_length = 12
    for tup in args:
        arrs = []
        for i in range(len(tup[0])):
            array = scipy.signal.savgol_filter(tup[0][i].data, win_length, 3)
            if tup[1] == "aod":
                scaled_array = tup[0][i] / array.max()
            elif tup[1] == "rf":
                scaled_array = -tup[0][i] / array.min()
            arrs.append(scaled_array)
        out.append(arrs)
    return tuple(out)


def get_m20() -> tuple[np.ndarray, ...]:
    """Create samples from Marshall et al. 2020."""
    # Need AOD and RF seasonal and annual means, as well as an array of equal length
    # with the corresponding time-after-eruption.
    path = (
        pathlib.Path(core.config.DATA_DIR_ROOT)
        / "marshall"
        / "dap.ceda.ac.uk"
        / "badc"
        / "deposited2020"
        / "vol-clim"
        / "data"
        / "UM-UKCA_volcanic_ensemble"
    )
    files = list(path.rglob("UM_UKCA*.nc"))
    data: list[xr.Dataset] = [xr.load_dataset(file.resolve()) for file in files]
    data = core.utils.load_auto.FindFiles().sort("SO2 emission (Tg)", arrays=data)
    # We first move the July eruptions back six months to January, so all have the
    # eruption day as the first element.
    for i, arr in enumerate(data):
        if arr.attrs["Eruption season"] == "Jul":
            data[i] = arr.assign_coords(
                time=arr.time.data - datetime.timedelta(days=180)
            )
    # Check that both seasons do indeed start at the same date.
    # Let us also check that 12 elements in, we are one year ahead.
    first = str(data[0].time.data[0])
    for arr in data[1:]:
        if str(arr.time.data[0]) != first:
            raise ValueError("Seasons do not start at the same date.")
        if f"{str(arr.time.data[12])[:3]}0{str(arr.time.data[12])[3 + 1:]}" != first:
            raise ValueError("This is not same day, next year.")

    weighter = core.utils.time_series.weighted_season_avg
    time, aod, rf = [], [], []
    tropical_limit = 10
    for arr in data:
        if abs(arr.attrs["Eruption latitude (degrees N)"]) > tropical_limit:
            continue
        time.append(
            core.utils.time_series.dt2float(
                weighter(arr["effective_radiative_forcing"]).time.data,
                days_in_year=360,
            )
        )
        aod.append(weighter(arr["stratospheric_aerosol_optical_depth_at_550_nm"]).data)
        rf.append(weighter(arr["effective_radiative_forcing"]).data)
    # All arrays now have time dimensions in float format, starting at 0.0.
    return np.asarray(time), np.asarray(aod), np.asarray(rf)
