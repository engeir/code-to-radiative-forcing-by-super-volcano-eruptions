"""Script that generates plots for figure 1."""

import pathlib
import tempfile

import cosmoplots
import matplotlib as mpl
import numpy as np
import scipy
import xarray as xr
from matplotlib import patches as mpatches
from matplotlib import pyplot as plt
from matplotlib.legend_handler import HandlerLine2D

import paper1_code as core

CLR = ["#1f77b4", "#ff7f0e", "#2ca02c"]
MIN_PERCENTILE = 5
MAX_PERCENTILE = 95


def _load_all_files() -> core.utils.load_auto.FindFiles:
    """Make sure that all necessary files are available."""
    matching_files = (
        core.utils.load_auto.FindFiles(ft=".npz")
        .find(
            "e_BWma1850",
            [f"ens{i+1}" for i in range(4)],
            {"medium", "medium-plus", "strong"},
            "TREFHT",
            "h1",
        )
        .sort("sim", "attr", "ensemble")
    )
    m_list = [
        ("e_BWma1850", "medium", "ens1", "TREFHT", "h1", "20230828"),
        ("e_BWma1850", "medium", "ens2", "TREFHT", "h1", "20230828"),
        ("e_BWma1850", "medium", "ens3", "TREFHT", "h1", "20230828"),
        ("e_BWma1850", "medium", "ens4", "TREFHT", "h1", "20230828"),
        ("e_BWma1850", "medium-plus", "ens1", "TREFHT", "h1", "20230828"),
        ("e_BWma1850", "medium-plus", "ens2", "TREFHT", "h1", "20230828"),
        ("e_BWma1850", "medium-plus", "ens3", "TREFHT", "h1", "20230828"),
        ("e_BWma1850", "medium-plus", "ens4", "TREFHT", "h1", "20230828"),
        ("e_BWma1850", "strong", "ens1", "TREFHT", "h1", "20230828"),
        ("e_BWma1850", "strong", "ens2", "TREFHT", "h1", "20230828"),
        ("e_BWma1850", "strong", "ens3", "TREFHT", "h1", "20230828"),
        ("e_BWma1850", "strong", "ens4", "TREFHT", "h1", "20230828"),
    ]
    if matching_files.get_files() != m_list:
        # Here we might want to ask the user if they would like to download the files
        # from the Fram archive storage.
        raise FileNotFoundError("Missing the nescessary files to do this analysis.")
    return matching_files


def _get_shifted_data(
    files: core.utils.load_auto.FindFiles
) -> tuple[list[xr.DataArray], list[xr.DataArray], list[xr.DataArray]]:
    """Get shifted data from the medium, medium-plus and strong eruption simulations.

    Parameters
    ----------
    files : core.utils.load_auto.FindFiles
        An instance of FindFiles that contains the necessary files

    Returns
    -------
    medium : list[xr.DataArray]
        Shifted data from the medium eruption simulation.
    medium_plus : list[xr.DataArray]
        Shifted data from the medium-plus eruption simulation.
    strong : list[xr.DataArray]
        Shifted data from the strong eruption simulation.
    """
    medium = files.copy().keep("medium").load()
    plus = files.copy().keep("medium-plus").load()
    strong = files.copy().keep("strong").load()
    for i, a in enumerate(medium):
        medium[i] = a.compute()
    for i, a in enumerate(plus):
        plus[i] = a.compute()
    for i, a in enumerate(strong):
        strong[i] = a.compute()
    medium_ = core.utils.time_series.remove_seasonality(medium)
    plus_ = core.utils.time_series.remove_seasonality(plus)
    strong_ = core.utils.time_series.remove_seasonality(strong)
    medium__ = core.utils.time_series.shift_arrays(medium_)
    plus__ = core.utils.time_series.shift_arrays(plus_)
    strong__ = core.utils.time_series.shift_arrays(strong_)
    return medium__, plus__, strong__


def waveform_max(
    files: core.utils.load_auto.FindFiles, save: bool = False
) -> mpl.figure.Figure:
    """Compare shape of TREFHT variable from medium and strong eruption simulations.

    The seasonal effects are removed by finding the median across four realisations.
    Comparison is done by shifting the signals to zero and then dividing by their
    maximum values.

    Parameters
    ----------
    files : core.utils.load_auto.FindFiles
        An instance of FindFiles that contains the necessary files
    save : bool
        Save the plot.

    Returns
    -------
    mpl.figure.Figure
        The figure object that is created by the function
    """
    medium, plus, strong = _get_shifted_data(files)
    for i, s in enumerate(strong):
        strong[i] = s[: len(medium[0])]

    # Find median values
    eq_temp = core.config.MEANS["TREFHT"]
    medium_med = np.median(medium, axis=0) - eq_temp
    plus_med = np.median(plus, axis=0) - eq_temp
    strong_med = np.median(strong, axis=0) - eq_temp
    win_len = 365
    medium_max = -scipy.signal.savgol_filter(medium_med, win_len, 3).min()
    plus_max = -scipy.signal.savgol_filter(plus_med, win_len, 3).min()
    strong_max = -scipy.signal.savgol_filter(strong_med, win_len, 3).min()
    medium_scaled = medium_med / medium_max
    plus_scaled = plus_med / plus_max
    strong_scaled = strong_med / strong_max

    # Percentiles
    n = 1
    low_range = np.linspace(MIN_PERCENTILE, 50, num=n, endpoint=False)
    high_range = np.linspace(50, MAX_PERCENTILE, num=n + 1)[1:]
    medium_perc1 = np.percentile(medium, low_range, axis=0) - eq_temp
    medium_perc1 = medium_perc1 / medium_max
    medium_perc2 = np.percentile(medium, high_range, axis=0) - eq_temp
    medium_perc2 = medium_perc2 / medium_max
    plus_perc1 = np.percentile(plus, low_range, axis=0) - eq_temp
    plus_perc1 = plus_perc1 / plus_max
    plus_perc2 = np.percentile(plus, high_range, axis=0) - eq_temp
    plus_perc2 = plus_perc2 / plus_max
    strong_perc1 = np.percentile(strong, low_range, axis=0) - eq_temp
    strong_perc1 = strong_perc1 / strong_max
    strong_perc2 = np.percentile(strong, high_range, axis=0) - eq_temp
    strong_perc2 = strong_perc2 / strong_max

    x_m = medium[0].time.data
    x_p = plus[0].time.data
    x_s = strong[0].time.data
    fig = plt.figure()
    ax = fig.gca()
    ax.set_xlabel(r"Time $[\mathrm{yr}]$")
    ax.set_ylabel("Normalised temperature anomaly $[1]$")
    (medium_line,) = ax.plot(x_m, medium_scaled, c="k")
    (plus_line,) = ax.plot(x_p, plus_scaled, ":", c="k")
    (strong_line,) = ax.plot(x_s, strong_scaled, "--", c="k")
    alpha = 1 / n if n != 1 else 0.7
    medium_fill = mpatches.Patch(facecolor=CLR[0], alpha=1.0, linewidth=0)
    for p1, p2 in zip(medium_perc1, medium_perc2, strict=True):
        ax.fill_between(x_m, p1, p2, alpha=alpha, color=CLR[0], edgecolor=None)
    plus_fill = mpatches.Patch(facecolor=CLR[1], alpha=1.0, linewidth=0)
    for p1, p2 in zip(plus_perc1, plus_perc2, strict=True):
        ax.fill_between(x_p, p1, p2, alpha=alpha, color=CLR[1], edgecolor=None)
    strong_fill = mpatches.Patch(facecolor=CLR[2], alpha=1.0, linewidth=0)
    for p1, p2 in zip(strong_perc1, strong_perc2, strict=True):
        ax.fill_between(x_s, p1, p2, alpha=alpha, color=CLR[2], edgecolor=None)
    # Vertical line at the time of the eruption
    ax.axvline(1850 + (31 + 15) / 356, c="k")

    # Combine shading and line labels
    plt.legend(
        [
            (strong_fill, strong_line),
            (plus_fill, plus_line),
            (medium_fill, medium_line),
        ],
        [
            r"C2W$\uparrow$, $C" + f" = {strong_max:.2f}" + r"$",
            r"C2W$-$, $C" + f" = {plus_max:.2f}" + r"$",
            r"C2W$\downarrow$, $C" + f" = {medium_max:.2f}" + r"$",
        ],
        loc="lower right",
        handler_map={
            medium_line: HandlerLine2D(marker_pad=0),
            plus_line: HandlerLine2D(marker_pad=0),
            strong_line: HandlerLine2D(marker_pad=0),
        },
        framealpha=0.6,
    )
    return plt.gcf()


def waveform_integrate(
    files: core.utils.load_auto.FindFiles, save: bool = False
) -> mpl.figure.Figure:
    """Compare shape of TREFHT variable from medium and strong eruption simulations.

    The median across four realisations is computed, with shading given from the 25th
    and 75th percentiles. Comparison is done by shifting the signals to zero and then
    dividing by their own integral.

    Parameters
    ----------
    files : core.utils.load_auto.FindFiles
        An instance of FindFiles that contains the necessary files
    save : bool
        Save the plot.

    Returns
    -------
    mpl.figure.Figure
        The figure object that is created by the function
    """
    medium, plus, strong = _get_shifted_data(files)
    for i, s in enumerate(strong):
        strong[i] = s[: len(medium[0])]

    # Find median values
    eq_temp = core.config.MEANS["TREFHT"]
    medium_med = np.median(medium, axis=0) - eq_temp
    plus_med = np.median(plus, axis=0) - eq_temp
    strong_med = np.median(strong, axis=0) - eq_temp
    medium_int = -np.trapz(medium_med, medium[0].time.data)
    plus_int = -np.trapz(plus_med, plus[0].time.data)
    strong_int = -np.trapz(strong_med, strong[0].time.data)
    medium_scaled = medium_med / medium_int
    plus_scaled = plus_med / plus_int
    strong_scaled = strong_med / strong_int

    # Percentiles
    n = 1
    low_range = np.linspace(MIN_PERCENTILE, 50, num=n, endpoint=False)
    high_range = np.linspace(50, MAX_PERCENTILE, num=n + 1)[1:]
    medium_perc1 = np.percentile(medium, low_range, axis=0) - eq_temp
    medium_perc1 = medium_perc1 / medium_int
    medium_perc2 = np.percentile(medium, high_range, axis=0) - eq_temp
    medium_perc2 = medium_perc2 / medium_int
    plus_perc1 = np.percentile(plus, low_range, axis=0) - eq_temp
    plus_perc1 = plus_perc1 / plus_int
    plus_perc2 = np.percentile(plus, high_range, axis=0) - eq_temp
    plus_perc2 = plus_perc2 / plus_int
    strong_perc1 = np.percentile(strong, low_range, axis=0) - eq_temp
    strong_perc1 = strong_perc1 / strong_int
    strong_perc2 = np.percentile(strong, high_range, axis=0) - eq_temp
    strong_perc2 = strong_perc2 / strong_int

    x_m = medium[0].time.data
    x_p = plus[0].time.data
    x_s = strong[0].time.data
    fig = plt.figure()
    ax = fig.gca()
    ax.set_xlabel(r"Time $[\mathrm{yr}]$")
    ax.set_ylabel("Normalised temperature anomaly $[1]$")
    (medium_line,) = ax.plot(x_m, medium_scaled, c="k")
    (plus_line,) = ax.plot(x_p, plus_scaled, ":", c="k")
    (strong_line,) = ax.plot(x_s, strong_scaled, "--", c="k")
    alpha = 1 / n if n != 1 else 0.7
    medium_fill = mpatches.Patch(facecolor=CLR[0], alpha=1.0, linewidth=0)
    for p1, p2 in zip(medium_perc1, medium_perc2, strict=True):
        ax.fill_between(x_m, p1, p2, alpha=alpha, color=CLR[0], edgecolor=None)
    plus_fill = mpatches.Patch(facecolor=CLR[1], alpha=1.0, linewidth=0)
    for p1, p2 in zip(plus_perc1, plus_perc2, strict=True):
        ax.fill_between(x_p, p1, p2, alpha=alpha, color=CLR[1], edgecolor=None)
    strong_fill = mpatches.Patch(facecolor=CLR[2], alpha=1.0, linewidth=0)
    for p1, p2 in zip(strong_perc1, strong_perc2, strict=True):
        ax.fill_between(x_s, p1, p2, alpha=alpha, color=CLR[2], edgecolor=None)
    # Vertical line at the time of the eruption
    ax.axvline(1850 + (31 + 15) / 356, c="k")

    # Combine shading and line labels
    plt.legend(
        [
            (strong_fill, strong_line),
            (plus_fill, plus_line),
            (medium_fill, medium_line),
        ],
        [
            r"C2W$\uparrow$, $C" + f" = {strong_int:.2f}" + r"$",
            r"C2W$-$, $C" + f" = {plus_int:.2f}" + r"$",
            r"C2W$\downarrow$, $C" + f" = {medium_int:.2f}" + r"$",
        ],
        loc="lower right",
        handler_map={
            medium_line: HandlerLine2D(marker_pad=0),
            plus_line: HandlerLine2D(marker_pad=0),
            strong_line: HandlerLine2D(marker_pad=0),
        },
        framealpha=0.6,
    )
    return plt.gcf()


def main():
    """Run the main program."""
    TMP = tempfile.TemporaryDirectory()
    tmp_dir = pathlib.Path(TMP.name)
    save = True
    files = _load_all_files()
    wint = waveform_integrate(files, save=save)
    wmax = waveform_max(files, save=save)
    if save:
        SAVE_PATH = core.scripts.if_save.create_savedir()
        wmax.savefig(tmp_dir / "compare-waveform-max")
        wint.savefig(tmp_dir / "compare-waveform-integrate")
        cosmoplots.combine(
            tmp_dir / "compare-waveform-max.png",
            tmp_dir / "compare-waveform-integrate.png",
        ).using(fontsize=50, gravity="southwest", pos=(5, 30)).in_grid(1, 2).save(
            SAVE_PATH / "compare-waveform.png"
        )
        if (fig1 := (SAVE_PATH / "compare-waveform.png")).exists():
            print(f"Successfully saved figure 1 to {fig1.resolve()}")
    plt.show()
    TMP.cleanup()


if __name__ == "__main__":
    main()
