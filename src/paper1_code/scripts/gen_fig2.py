"""Script that generates plots for figure 2."""

import datetime
import pathlib
import tempfile
import warnings

import cosmoplots
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import plastik
import scipy
import xarray as xr

import paper1_code as core

FINDER = core.utils.load_auto.FindFiles()


def _set_aod_arrs() -> tuple[list[xr.DataArray], ...]:
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
    s = core.utils.time_series.shift_arrays(s, daily=False)
    mp = core.utils.time_series.shift_arrays(mp, daily=False)
    m = core.utils.time_series.shift_arrays(m, daily=False)
    h = core.utils.time_series.shift_arrays(h, custom=12)
    h = core.utils.time_series.shift_arrays(h, daily=False)
    for i, arr in enumerate(s):
        s[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(mp):
        mp[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(m):
        m[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(h):
        h[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    return m, mp, s, h


def _set_toa_arrs() -> tuple[list[xr.DataArray], ...]:
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
    s_ = core.utils.time_series.shift_arrays(s_, daily=False)
    mp_ = core.utils.time_series.shift_arrays(mp_, daily=False)
    m_ = core.utils.time_series.shift_arrays(m_, daily=False)
    h_ = core.utils.time_series.shift_arrays(h_, custom=12)
    h_ = core.utils.time_series.shift_arrays(h_, daily=False)
    for i, arr in enumerate(s_):
        s_[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(mp_):
        mp_[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(m_):
        m_[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(h_):
        h_[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    return m_, mp_, s_, h_


def _array_leginizer(ax: mpl.axes.Axes) -> mpl.axes.Axes:
    c4 = plastik.colors.create_colorlist("cmc.batlow", 4)
    c14 = [c4[0]] * 4 + [c4[1]] * 4 + [c4[3]] * 4 + [c4[2]] * 2
    for n, c_ in zip(ax.get_lines(), c14, strict=False):
        n.set_color(c_)
    # Otherwise, it yells at me with UserWarning's cuz of the leading underscore
    warnings.simplefilter("ignore")
    ax.legend(
        [
            r"C2W$\downarrow$",
            r"_C2W$\downarrow$",
            r"_C2W$\downarrow$",
            r"_C2W$\downarrow$",
            "C2W$-$",
            "_C2W$-$",
            "_C2W$-$",
            "_C2W$-$",
            r"C2W$\uparrow$",
            r"_C2W$\uparrow$",
            r"_C2W$\uparrow$",
            r"_C2W$\uparrow$",
            r"C2WN$\uparrow$",
            r"_C2WN$\uparrow$",
        ],
        fontsize=6,
        loc="right",
        reverse=True,
    ).get_frame().set_alpha(0.8)
    warnings.resetwarnings()
    return ax


def _normalize_peaks(
    scale_idx: int = 0, *args: tuple[list, list | np.ndarray, str]
) -> tuple[list, ...]:
    out: list[list] = []
    win_length = 12
    for tup in args:
        arrs, peaks = [], []
        assert len(tup[0]) == len(tup[1])
        for i in range(len(tup[0])):
            array = scipy.signal.savgol_filter(tup[0][i].data, win_length, 3)
            if tup[2] == "aod":
                scaled_array = tup[0][i] / array.max()
            elif tup[2] == "toa":
                scaled_array = -tup[0][i] / array.min()
            arrs.append(scaled_array)
            peaks.append(tup[1][i] / tup[1][i])
        out.append([arrs, np.asarray(peaks)])
    return tuple(out)


def plot_arrays() -> tuple[mpl.figure.Figure, mpl.figure.Figure]:
    """Plot the data that is used in other analysis methods.

    Returns
    -------
    tuple[mpl.figure.Figure, mpl.figure.Figure]
        The figures returned are
        - AOD normalized
        - TOA normalized
    """
    # AOD data and TOA data
    aod_m, aod_mp, aod_s, aodh = _set_aod_arrs()
    aod = aod_m + aod_mp + aod_s + aodh
    aod = core.utils.time_series.shift_arrays(aod, custom=1)
    rf_m, rf_mp, rf_s, rf_h = _set_toa_arrs()
    toa = rf_m + rf_mp + rf_s + rf_h
    toa = core.utils.time_series.shift_arrays(toa, custom=1)
    # Check that they include the same items
    aod = core.utils.time_series.keep_whole_years(aod, freq="MS")
    toa = core.utils.time_series.keep_whole_years(toa, freq="MS")
    for i, (arr1, arr2) in enumerate(zip(aod, toa, strict=True)):
        aod[i] = arr1[: int(4 * 12)]
        toa[i] = arr2[: int(4 * 12)]
    aod_full = aod
    toa_full = toa
    for i, array in enumerate(aod_full):
        aod_array_ = array.assign_coords(
            time=array.time.data - datetime.timedelta(days=1850 * 365)
        )
        aod_full[i] = aod_array_.assign_coords(
            time=core.utils.time_series.dt2float(aod_array_.time.data)
        )
    for i, array in enumerate(toa_full):
        rf_array_: xr.DataArray = array.assign_coords(
            time=array.time.data - datetime.timedelta(days=1850 * 365)
        )
        toa_full[i] = rf_array_.assign_coords(
            time=core.utils.time_series.dt2float(rf_array_.time.data)
        )
    aod_p = [1] * len(aod_full)
    toa_p = [1] * len(toa_full)
    newaod_, newtoa_ = _normalize_peaks(
        2, (aod_full, aod_p, "aod"), (toa_full, toa_p, "toa")
    )
    newaod, _ = newaod_
    newtoa, _ = newtoa_

    # AOD normal
    fig1 = plt.figure()
    ax = plt.gca()
    for a in newaod:
        a.plot(ax=ax)
    ax = _array_leginizer(ax)
    plt.xlabel(r"Time after eruption $[\mathrm{year}]$")
    plt.ylabel("Normalized \naerosol optical depth $[1]$")
    # RF normal
    fig2 = plt.figure()
    ax = plt.gca()
    for t in newtoa:
        t.plot(ax=ax)
    ax = _array_leginizer(ax)
    plt.xlabel(r"Time after eruption $[\mathrm{year}]$")
    plt.ylabel("Normalized \nradiative forcing $[1]$")
    return fig1, fig2


def main():
    """Run the main program."""
    TMP = tempfile.TemporaryDirectory()
    save = True
    aod, rf = plot_arrays()
    if save:
        SAVE_PATH = core.scripts.if_save.create_savedir()
        aod.savefig(pathlib.Path(TMP.name) / "aod_arrays_normalized")
        rf.savefig(pathlib.Path(TMP.name) / "toa_arrays_normalized")
        cosmoplots.combine(
            pathlib.Path(TMP.name) / "aod_arrays_normalized.png",
            pathlib.Path(TMP.name) / "toa_arrays_normalized.png",
        ).using(fontsize=50).in_grid(1, 2).save(
            SAVE_PATH / "arrays_combined_normalized.png"
        )
        if (fig2 := (SAVE_PATH / "arrays_combined_normalized.png")).exists():
            print(f"Successfully saved figure 2 to {fig2.resolve()}")
    plt.show()
    TMP.cleanup()


if __name__ == "__main__":
    main()
