"""Data that is used in several figures are loaded here."""

import datetime
import itertools
import pathlib
import re
from typing import Literal

import numpy as np
import scipy
import xarray as xr

import paper1_code as core

FINDER = core.utils.load_auto.FindFiles()


def get_aod_arrs(shift: int | None = None) -> tuple[list[xr.DataArray], ...]:
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
    return m, mp, s, h


def get_rf_arrs(shift: int | None = None) -> tuple[list[xr.DataArray], ...]:
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
    return m_, mp_, s_, h_


def _get_trefht_arrs() -> (
    tuple[
        list[xr.DataArray], list[xr.DataArray], list[xr.DataArray], list[xr.DataArray]
    ]
):
    data = FINDER.find(
        "e_BWma1850",
        {f"ens{i}" for i in range(5)},
        {"strong", "medium", "medium-plus", "strong-highlat"},
        "TREFHT",
        "h0",
    ).sort("attr", "ensemble")
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
    m = core.utils.time_series.shift_arrays(m, daily=False)
    mp = core.utils.time_series.shift_arrays(mp, daily=False)
    s = core.utils.time_series.shift_arrays(s, daily=False)
    h = core.utils.time_series.shift_arrays(h, daily=False)
    return m, mp, s, h


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


def get_so2_tambora_peak() -> float:
    """Get the SO2 injection used in VolMIP volc-long-eq for the Tambora eruption.

    See
    https://view.es-doc.org/index.html?renderMethod=id&project=cmip6&id=fc04f8eb-feff-4fa4-ba91-41cf9041a2ef&version=1
    """
    return 56.2


def get_aod_tambora() -> float:
    """From EVAv1.2(eVolv2k), Tambora 1815, Toohey and Sigl (2017).

    Notes
    -----
    Download data from https://www.wdc-climate.de/ui/entry?acronym=eVolv2k_v3.
    """
    return 0.355


def get_rf_tambora() -> float:
    """From Raible et al. (2016), p. 573.

    Notes
    -----
    https://doi.org/10.1002/wcc.407
    """
    return 5


def get_trefht_tambora() -> float:
    """From Raible et al. (2016) or Marshall et al. (2018).

    Notes
    -----
    Based on two simulations from the VolMIP ensemble, 1.5 K is also realistic.
    """
    return 1


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


def get_so2_j05() -> float:
    """Based on the paper by Jones et al. (2005).

    The SO2 is described to last over some time, thus the value set here might be
    too low when compared to a "total SO2 injected" value. (Bottom of page 726,
    section 3 Validity of approach).

    Notes
    -----
    DOI: 10.1007/s00382-005-0066-8
    """
    return 1400


def get_aod_j05() -> float:
    """Based on the paper by Jones et al. (2005).

    Notes
    -----
    DOI: 10.1007/s00382-005-0066-8
    """
    return 15


def get_rf_j05() -> float:
    """Top-of-atmosphere radiative imbalance due to Mount Pinatubo, times 100.

    See Jones et al. (2005).
    """
    return 60


def get_trefht_j05() -> float:
    """Based on the paper by Jones et al. (2005).

    Notes
    -----
    DOI: 10.1007/s00382-005-0066-8
    """
    return 10.7


def get_so2_t10() -> float:
    """Based on the paper by Timmreck et al. (2010).

    Actually, it is the YTT (Young Toba Tuff).

    Notes
    -----
    DOI: 10.1029/2010GL045464
    """
    return 850 * 2


def get_aod_t10() -> float:
    """Based on the paper by Timmreck et al. (2010).

    Actually, it is the YTT (Young Toba Tuff).

    Notes
    -----
    DOI: 10.1029/2010GL045464
    """
    # A factor of 3-5 smaller than the Jones et al. 2005 AOD peak
    # 15 / 3.5 = 4.2857142857143
    return 4.286


def get_rf_t10() -> float:
    """Top-of-atmosphere radiative imbalance due to Mount Pinatubo, times 100.

    Actually, it is the YTT (Young Toba Tuff).

    See Timmreck et al. (2010).
    """
    return 18


def get_trefht_t10() -> float:
    """Based on the paper by Jones et al. (2005).

    Notes
    -----
    DOI: 10.1007/s00382-005-0066-8
    """
    return 3.5


def get_so2_pinatubo() -> float:
    """Get SO2 injected values based on observational data.

    This range between 10 to 17 Tg (Sukhodolov, 2018) (values used in models that
    capture well the temperature response), but others report about 18 Tg (Guo et
    al., 2004; Toohey and Sigl, 2017) (value obtained from observational analysis).
    """
    return 18


def get_aod_pinatubo() -> float:
    """Aerosol optical depth due to Mount Pinatubo.

    See for example Sukhodolov (2018).
    """
    return 0.15


def get_rf_pinatubo() -> float:
    """Top-of-atmosphere radiative imbalance due to Mount Pinatubo.

    Douglass, D. H., Knox, R. S., et al. (2006) report a value of ~3.4 while
    Gregory, J. M., Andrews, T., et al., (2016) report a value of ~3.0.
    """
    return 3.2


def get_trefht_pinatubo() -> float:
    """Based on the paper by Hansen et al. (1999).

    The GISS paper is an analysis of surface temperature between 1880 and 1999 based
    on observational data, primarily based on meteorological station measurements.
    See for example figure 7.

    Notes
    -----
    DOI: 10.1029/1999JD900835
    """
    return 0.5


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
    m_, mp_, s_, h_ = _get_trefht_arrs()
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


def normalize_peaks(*args: tuple[list | np.ndarray, str]) -> tuple[list, ...]:
    """Normalize the input arrays.

    The string (see description of `args` in the parameters section) only negates the
    arrays. Completely pointless actually, since this should rather be done after the
    fact, but also why not.

    Parameters
    ----------
    *args : tuple[list | np.ndarray, str]
        Each tuple sent to `args` contains an array and a string describing if the array
        is an AOD or RF array. But really the only difference is that is the string is
        `aod` we multiply by `1`, and if the string is `rf` we multiply by -1.

    Returns
    -------
    tuple[list, ...]
        However many tuples with arrays are sent in, as many lists are returned
    """
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


def get_m20(find_all_peaks: bool = False) -> tuple[np.ndarray, ...]:
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
    time, so2, aod, rf, temp = [], [], [], [], []
    if find_all_peaks:
        for arr in data:
            # Find peak using savgol filter, then plot SO2 versus {AOD, ERF, T}.
            rf_arr = scipy.signal.savgol_filter(
                arr["effective_radiative_forcing"], 12, 3
            )
            temp_arr = scipy.signal.savgol_filter(
                arr["surface_temperature_adjustment"], 12, 3
            )
            aod_arr = scipy.signal.savgol_filter(
                arr["stratospheric_aerosol_optical_depth_at_550_nm"], 12, 3
            )
            so2.append(arr.attrs["SO2 emission (Tg)"])
            aod.append(aod_arr.max())
            rf.append(rf_arr.min())
            temp.append(temp_arr.max())
        return np.asarray(so2), np.asarray(aod), -np.asarray(rf), np.asarray(temp)
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


def _get_ob16_rf_temp_arrays() -> tuple[list[xr.DataArray], list[xr.DataArray]]:
    """Create samples from Otto-Bliesner et al. 2016.

    Returns
    -------
    tuple[list[xr.DataArray], list[xr.DataArray]]
        The AOD and RF arrays in two lists
    """
    # Need AOD and RF seasonal and annual means, as well as an array of equal length
    # with the corresponding time-after-eruption.
    path = pathlib.Path(core.config.DATA_DIR_ROOT) / "cesm-lme"
    pattern = re.compile("([A-Z]+)-00[1-5]\\.npz$", re.X)
    files_ = list(path.rglob("*00[1-5].npz"))
    rf, temp = [], []
    for file in files_:
        if isinstance(search := pattern.search(str(file)), re.Match):
            array = _load_numpy(file.resolve())
            s = "0850-01-01"
            t = xr.cftime_range(
                start=s, periods=len(array.data), calendar="noleap", freq="D"
            )
            if search.groups()[0] == "TREFHT":
                temp.append(array.assign_coords({"time": t}))
            elif search.groups()[0] == "FSNTOA":
                rf.append(array.assign_coords({"time": t}))
    return rf, temp


def _load_numpy(np_file) -> xr.DataArray:
    """Load the content of an npz file as an xarray DataArray."""
    with np.load(np_file, allow_pickle=True) as data:
        two_dim_data = 2
        if data["data"].ndim == two_dim_data:
            if "lev" in data.files and data["lev"].shape != ():
                lev_str = "lev"
            elif "ilev" in data.files and data["ilev"].shape != ():
                lev_str = "ilev"
            else:
                raise KeyError(f"There is no level information in the file {np_file}")
            coords = {"time": data["times"], lev_str: data[lev_str]}
            dims = ["time", lev_str]
        else:
            coords = {"time": data["times"]}
            dims = ["time"]
        xarr = xr.DataArray(data["data"], dims=dims, coords=coords)
    return xarr


def _remove_seasonality_ob16(arr: xr.DataArray, monthly: bool = False) -> xr.DataArray:
    """Remove seasonality by subtracting CESM LME control run."""
    file_name = (
        pathlib.Path(core.config.DATA_DIR_ROOT)
        / "cesm-lme"
        / "TREFHT850forcing-control-003.npz"
    )
    if file_name.exists():
        array = _load_numpy(file_name.resolve())
        s = "0850-01-01"
        t = xr.cftime_range(
            start=s, periods=len(array.data), calendar="noleap", freq="D"
        )
        raw_temp = array.assign_coords({"time": t})
    if monthly:
        raw_temp = raw_temp.resample(time="MS").mean()
        raw_temp, arr = xr.align(raw_temp, arr)
        month_mean = raw_temp.groupby("time.month").mean("time")
        return arr.groupby("time.month") - month_mean + core.config.MEANS["TREFHT"]
    day_mean = raw_temp.groupby("time.dayofyear").mean()
    raw_temp, arr = xr.align(raw_temp, arr)
    return arr.groupby("time.dayofyear") - day_mean + core.config.MEANS["TREFHT"]


def _gao_remove_decay_in_forcing(
    frc: np.ndarray, y: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    new_frc = np.zeros_like(frc)
    limit = 2e-6
    place_here = 1
    for i, v in enumerate(frc[1:]):
        if frc[i - 1] < v and v > limit and frc[i - 1] < limit:
            new_frc[i + place_here] = v
        if new_frc[i + place_here - 1] > limit and v > new_frc[i + place_here - 1]:
            new_frc[i + place_here - 1] = 0
            new_frc[i + place_here] = v
    # Go from monthly to daily (this is fine as long as we use a spiky forcing). We
    # start in December.
    new_frc = _month2day(new_frc, start=12)
    # The new time axis now goes down to one day
    y = np.linspace(501, 2002, (2002 - 501) * 365 + 1)
    y = y[: len(new_frc)]
    return new_frc, y


def _month2day(
    arr: np.ndarray,
    start: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] = 1,
) -> np.ndarray:
    # Go from monthly to daily
    newest = np.array([])
    # Add 30, 29 or 27 elements between all elements: months -> days
    days_ = (30, 27, 30, 29, 30, 29, 30, 30, 29, 30, 29, 30)
    days = itertools.cycle(days_)
    for _ in range(start - 1):
        next(days)
    for month in arr:
        insert_ = np.zeros(next(days))
        newest = np.r_[newest, np.array([month])]
        newest = np.r_[newest, insert_]
    # The new time axis now goes down to one day
    return newest


def _get_so2_ob16_full_timeseries() -> tuple[np.ndarray, np.ndarray]:
    """Load the npz file with volcanic injection.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Arrays containing time and value of SO2 peaks
    """
    file = "IVI2LoadingLatHeight501-2000_L18_c20100518.nc"
    ds = xr.open_dataset(pathlib.Path(core.config.DATA_DIR_ROOT) / "cesm-lme" / file)
    year = ds.time.data
    avgs_list = core.utils.time_series.mean_flatten([ds.colmass], dims=["lat"])
    avgs = avgs_list[0].data
    # Scale so that the unit is now in Tg (Otto-Bliesner et al. (2016)).
    avgs = avgs / avgs.max() * 257.9
    return year, avgs


def _get_so2_ob16() -> xr.DataArray:
    """Load in mean stratospheric volcanic sulfate aerosol injections.

    Returns
    -------
    xr.DataArray
        The stratospheric sulfate injections used as forcing in the CESM LME
        simulations.

    Notes
    -----
    The data is from Gao et al. (2008) `data
    <http://climate.envsci.rutgers.edu/IVI2/>`_, and was used as input to the model
    simulations by Otto-Bliesner et al. (2017).
    """
    y, g = _get_so2_ob16_full_timeseries()
    y = y - y[0] + 501
    g, y = _gao_remove_decay_in_forcing(g, y)
    freq = "D"
    da = xr.DataArray(
        g,
        dims=["time"],
        coords={"time": core.utils.time_series.float2dt(y, freq)},
        name="Mean stratospheric volcanic sulfate aerosol injections [Tg]",
    )
    da = da.assign_coords(time=da.time.data + datetime.timedelta(days=14))
    return da


def get_ob16() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return Otto-Bliesner et al. 2016 SO2, RF and temperature peaks.

    The peaks are best estimates from the full time series.

    Returns
    -------
    tuple[np.ndarray, np.ndarray, np.ndarray]
        SO2 peaks, RF peaks and temperature peaks
    """
    # Temperature
    ds, temp_ = _get_ob16_rf_temp_arrays()
    temp_xr = core.utils.time_series.get_median(temp_, xarray=True)
    # Seasonality is removed by use of a control run temperature time series, where we
    # compute a climatology mean for each day of the year which is subtracted from the
    # time series.
    # temp_xr = temp_xr.assign_coords(time=core.utils.time_series.float2dt(temp_xr.time.data))
    temp_xr = _remove_seasonality_ob16(temp_xr)
    # Adjust the temperature so its mean is at zero, and fluctuations are positive. We
    # also remove a slight drift by means of a linear regression fit.
    temp_xr *= -1
    x_ax = core.utils.time_series.dt2float(temp_xr.time.data)
    temp_lin_reg = scipy.stats.linregress(x_ax, temp_xr.data)
    temp_xr.data -= x_ax * temp_lin_reg.slope + temp_lin_reg.intercept

    # Add RF from the FSNTOA variable (daily) ---------------------------------------- #
    # We load in the original FSNTOA 5 member ensemble and compute the ensemble mean.
    rf = core.utils.time_series.get_median(ds, xarray=True)
    # Remove noise in Fourier domain (seasonal and 6-month cycles)
    rf_fr = core.utils.time_series.remove_seasonality([rf.copy()])[0]
    rf_fr = core.utils.time_series.remove_seasonality([rf_fr], freq=2)[0]
    # Subtract the mean and flip
    rf_fr.data -= rf_fr.data.mean()
    rf_fr.data *= -1

    # Scale forcing from SO4 to SO2
    so2_start = _get_so2_ob16() / 3 * 2
    # A 210 days shift forward give the best timing of the temperature peak and 150
    # days forward give the timing for the radiative forcing peak. A 190 days shift
    # back give the best timing for when the temperature and radiative forcing
    # perturbations start (eruption day). Done by eye measure.
    d1, d2, d3 = 190, 150, 210
    so2_start = so2_start.assign_coords(
        time=so2_start.time.data - datetime.timedelta(days=d1)
    )
    so2_rf_peak = so2_start.assign_coords(
        time=so2_start.time.data + datetime.timedelta(days=d2)
    )
    so2_temp_peak = so2_start.assign_coords(
        time=so2_start.time.data + datetime.timedelta(days=d3)
    )

    so2_start, so2_rf_peak, so2_temp_peak, rf_fr, temp = xr.align(
        so2_start, so2_rf_peak, so2_temp_peak, rf_fr, temp_xr
    )

    if not len(so2_start) % 2:
        so2_start = so2_start[:-1]
        so2_rf_peak = so2_rf_peak[:-1]
        so2_temp_peak = so2_rf_peak[:-1]
        rf_fr = rf_fr[:-1]
        temp = temp[:-1]
    _cesm_lme_so2_start = so2_start
    _cesm_lme_so2_rf_peak = so2_rf_peak
    _cesm_lme_so2_temp_peak = so2_temp_peak
    _cesm_lme_rf = rf_fr
    _cesm_lme_temp = temp
    # Mask out all non-zero forcing values, and the corresponding temperature values.
    _idx_rf = np.argwhere(so2_rf_peak.data > 0)
    _idx_temp = np.argwhere(so2_temp_peak.data > 0)
    so2 = so2_rf_peak.data[_idx_rf].flatten()
    rf_v = rf_fr.data[_idx_rf].flatten()
    temp_v = temp.data[_idx_temp].flatten()
    _ids = so2.argsort()
    return so2[_ids], rf_v[_ids], temp_v[_ids]
