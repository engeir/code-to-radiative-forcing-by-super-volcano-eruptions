"""Script that generates plots for figure 2."""

import datetime
import pathlib
import tempfile
import warnings

import cosmoplots
import matplotlib as mpl
import matplotlib.pyplot as plt
import plastik
import xarray as xr

import paper1_code as core
from paper1_code.scripts import load_data as core_load


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
        fontsize=core.config.FONTSIZE,
        loc="right",
        reverse=True,
    ).get_frame().set_alpha(0.8)
    warnings.resetwarnings()
    return ax


def plot_arrays() -> tuple[mpl.figure.Figure, mpl.figure.Figure]:
    """Plot the data that is used in other analysis methods.

    Returns
    -------
    tuple[mpl.figure.Figure, mpl.figure.Figure]
        The figures returned are
        - AOD normalized
        - RF normalized
    """
    # AOD data and RF data
    aod_m, aod_mp, aod_s, aod_h = core_load.get_aod_arrs()
    aod = aod_m + aod_mp + aod_s + aod_h
    aod = core.utils.time_series.shift_arrays(aod, custom=1)
    rf_m, rf_mp, rf_s, rf_h = core_load.get_rf_arrs()
    rf = rf_m + rf_mp + rf_s + rf_h
    rf = core.utils.time_series.shift_arrays(rf, custom=1)
    # Check that they include the same items
    aod = core.utils.time_series.keep_whole_years(aod, freq="MS")
    rf = core.utils.time_series.keep_whole_years(rf, freq="MS")
    for i, (arr1, arr2) in enumerate(zip(aod, rf, strict=True)):
        aod[i] = arr1[: int(4 * 12)]
        rf[i] = arr2[: int(4 * 12)]
    aod_full = aod
    rf_full = rf
    for i, array in enumerate(aod_full):
        aod_array_ = array.assign_coords(
            time=array.time.data - datetime.timedelta(days=1850 * 365)
        )
        aod_full[i] = aod_array_.assign_coords(
            time=core.utils.time_series.dt2float(aod_array_.time.data)
        )
    for i, array in enumerate(rf_full):
        rf_array_: xr.DataArray = array.assign_coords(
            time=array.time.data - datetime.timedelta(days=1850 * 365)
        )
        rf_full[i] = rf_array_.assign_coords(
            time=core.utils.time_series.dt2float(rf_array_.time.data)
        )
    newaod, newrf = core_load.normalize_peaks((aod_full, "aod"), (rf_full, "rf"))

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
    for t in newrf:
        t.plot(ax=ax)
    ax = _array_leginizer(ax)
    plt.xlabel(r"Time after eruption $[\mathrm{year}]$")
    plt.ylabel("Normalized \nradiative forcing $[1]$")
    return fig1, fig2


def main(show_output: bool = False):
    """Run the main program."""
    TMP = tempfile.TemporaryDirectory()
    tmp_dir = pathlib.Path(TMP.name)
    save = True
    aod, rf = plot_arrays()
    if save:
        SAVE_PATH = core.scripts.if_save.create_savedir()
        aod.savefig(tmp_dir / "aod_arrays_normalized")
        rf.savefig(tmp_dir / "rf_arrays_normalized")
        cosmoplots.combine(
            tmp_dir / "aod_arrays_normalized.png",
            tmp_dir / "rf_arrays_normalized.png",
        ).using(fontsize=50).in_grid(1, 2).save(
            SAVE_PATH / "arrays_combined_normalized.png"
        )
        if (fig2 := (SAVE_PATH / "arrays_combined_normalized.png")).exists():
            print(f"Successfully saved figure 2 to {fig2.resolve()}")
    if show_output:
        plt.show()
    else:
        plt.close("all")
    TMP.cleanup()


if __name__ == "__main__":
    main(show_output=True)
