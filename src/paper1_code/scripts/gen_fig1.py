"""Script that generates plots for figure 1."""

import cosmoplots
import numpy as np
import plastik
import scipy
import xarray as xr
from matplotlib import patches as mpatches
from matplotlib import pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
from scipy import optimize as spo

import paper1_code as core

FINDER = core.utils.load_auto.FindFiles(ft=".npz")
MIN_PERCENTILE = 5
MAX_PERCENTILE = 95

def _get_shifted_data(
    do_fourier: bool = False,
) -> tuple[list[xr.DataArray], list[xr.DataArray], list[xr.DataArray]]:
    """Get shifted data from the medium, medium-plus and strong eruption simulations.

    Parameters
    ----------
    do_fourier : bool
        It True, seasonality is removed using the Fourier method. Defaults to False.

    Returns
    -------
    medium : list[xr.DataArray]
        Shifted data from the medium eruption simulation.
    medium_plus : list[xr.DataArray]
        Shifted data from the medium-plus eruption simulation.
    strong : list[xr.DataArray]
        Shifted data from the strong eruption simulation.
    """
    matching_files = FINDER.find(
        "e_BWma1850",
        [f"ens{i+1}" for i in range(4)],
        {"medium", "medium-plus", "strong"},
        "TREFHT",
        "h1",
    ).sort("sim", "attr", "ensemble")
    medium = matching_files.copy().keep("medium").load()
    plus = matching_files.copy().keep("medium-plus").load()
    strong = matching_files.copy().keep("strong").load()
    for i, a in enumerate(medium):
        medium[i] = a.compute()
    for i, a in enumerate(plus):
        plus[i] = a.compute()
    for i, a in enumerate(strong):
        strong[i] = a.compute()
    if do_fourier:
        medium = core.utils.fourier.remove_seasonality(medium)
        plus = core.utils.fourier.remove_seasonality(plus)
        strong = core.utils.fourier.remove_seasonality(strong)
    medium = era.manipulate.shift_arrays(medium)
    plus = era.manipulate.shift_arrays(plus)
    strong = era.manipulate.shift_arrays(strong)
    return medium, plus, strong
def waveform_max(save: bool = False, do_fourier: bool = False) -> None:
    """Compare shape of TREFHT variable from medium and strong eruption simulations.

    The seasonal effects are removed by finding the median across four realisations.
    Comparison is done by shifting the signals to zero and then dividing by their
    maximum values.

    Parameters
    ----------
    save : bool
        Save the plot.
    do_fourier : bool
        It True, seasonality is removed using the Fourier method. Defaults to False.
    """
    clr = ["#1f77b4", "#ff7f0e", "#2ca02c"]
    medium, plus, strong = _get_shifted_data(do_fourier)
    for i, s in enumerate(strong):
        strong[i] = s[: len(medium[0])]

    # Find median values
    eq_temp = era.config.MEANS["TREFHT"]
    medium_med = np.median(medium, axis=0) - eq_temp
    plus_med = np.median(plus, axis=0) - eq_temp
    strong_med = np.median(strong, axis=0) - eq_temp
    win_len = 365
    medium_max = -scipy.signal.savgol_filter(medium_med, win_len, 3).min()
    plus_max = -scipy.signal.savgol_filter(plus_med, win_len, 3).min()
    strong_max = -scipy.signal.savgol_filter(strong_med, win_len, 3).min()
    # medium_max = 0.9
    # plus_max = 4.8
    # strong_max = 7.9
    print(f"{medium_max = :.4f}, {plus_max = :.4f}, {strong_max = :.4f}")
    # medium_int = 4.0424, plus_int = 21.9824, strong_int = 35.5616
    # Eruptions was 26 Tg, 400 Tg and 1629 Tg respectively.
    # Emissions was 9.71081e10 Tg, 1.48627e12 Tg and 6.05419e12 Tg respectively.
    # print(
    #     f"{medium_int / 26 = :.4f}, {plus_int / 400 = :.4f}, "
    #     + "{strong_int / 1629 = :.4f}"
    # )
    # print(
    #     f"{(eq_temp - 286.5) / 26 = :.4f}, {(eq_temp - 282.5) / 400 = :.4f}, "
    #     + "{(eq_temp - 279.3) / 1629 = :.4f}"
    # )
    # axen = plt.figure().add_axes(__FIG_STD__)
    # axen.plot([26, 400, 1629], [medium_int, plus_int, strong_int], "o")
    # axen = plt.figure().add_axes(__FIG_STD__)
    # axen.semilogx(
    #     [9.71081e10, 1.48627e12, 6.05419e12], [medium_int, plus_int, strong_int], "o"
    # )
    # plt.show()

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
    medium_fill = mpatches.Patch(facecolor=clr[0], alpha=1.0, linewidth=0)
    for p1, p2 in zip(medium_perc1, medium_perc2):
        ax.fill_between(x_m, p1, p2, alpha=alpha, color=clr[0], edgecolor=None)
    plus_fill = mpatches.Patch(facecolor=clr[1], alpha=1.0, linewidth=0)
    for p1, p2 in zip(plus_perc1, plus_perc2):
        ax.fill_between(x_p, p1, p2, alpha=alpha, color=clr[1], edgecolor=None)
    strong_fill = mpatches.Patch(facecolor=clr[2], alpha=1.0, linewidth=0)
    for p1, p2 in zip(strong_perc1, strong_perc2):
        ax.fill_between(x_s, p1, p2, alpha=alpha, color=clr[2], edgecolor=None)
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
        framealpha=0.8,
    )

    if save:
        plt.savefig("./compare-waveform-max")

def waveform_integrate(save: bool = False, do_fourier: bool = False) -> None:
    """Compare shape of TREFHT variable from medium and strong eruption simulations.

    The median across four realisations is computed, with shading given from the 25th
    and 75th percentiles. Comparison is done by shifting the signals to zero and then
    dividing by their own integral.

    Parameters
    ----------
    save : bool
        Save the plot.
    do_fourier : bool
        It True, seasonality is removed using the Fourier method. Defaults to False.
    """
    clr = ["#1f77b4", "#ff7f0e", "#2ca02c"]
    medium, plus, strong = _get_shifted_data(do_fourier)
    for i, s in enumerate(strong):
        strong[i] = s[: len(medium[0])]

    # Find median values
    eq_temp = era.config.MEANS["TREFHT"]
    medium_med = np.median(medium, axis=0) - eq_temp
    plus_med = np.median(plus, axis=0) - eq_temp
    strong_med = np.median(strong, axis=0) - eq_temp
    medium_int = -np.trapz(medium_med, medium[0].time.data)
    plus_int = -np.trapz(plus_med, plus[0].time.data)
    strong_int = -np.trapz(strong_med, strong[0].time.data)
    print(f"{medium_int = :.4f}, {plus_int = :.4f}, {strong_int = :.4f}")
    # medium_int = 4.0424, plus_int = 21.9824, strong_int = 35.5616
    # Eruptions was 26 Tg, 400 Tg and 1629 Tg respectively.
    # Emissions was 9.71081e10 Tg, 1.48627e12 Tg and 6.05419e12 Tg respectively.
    # print(
    #     f"{medium_int / 26 = :.4f}, {plus_int / 400 = :.4f}, "
    #     + "{strong_int / 1629 = :.4f}"
    # )
    # print(
    #     f"{(eq_temp - 286.5) / 26 = :.4f}, {(eq_temp - 282.5) / 400 = :.4f}, "
    #     + "{(eq_temp - 279.3) / 1629 = :.4f}"
    # )
    # axen = plt.figure().add_axes(__FIG_STD__)
    # axen.plot([26, 400, 1629], [medium_int, plus_int, strong_int], "o")
    # axen = plt.figure().add_axes(__FIG_STD__)
    # axen.semilogx(
    #     [9.71081e10, 1.48627e12, 6.05419e12], [medium_int, plus_int, strong_int], "o"
    # )
    # plt.show()

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
    medium_fill = mpatches.Patch(facecolor=clr[0], alpha=1.0, linewidth=0)
    for p1, p2 in zip(medium_perc1, medium_perc2):
        ax.fill_between(x_m, p1, p2, alpha=alpha, color=clr[0], edgecolor=None)
    plus_fill = mpatches.Patch(facecolor=clr[1], alpha=1.0, linewidth=0)
    for p1, p2 in zip(plus_perc1, plus_perc2):
        ax.fill_between(x_p, p1, p2, alpha=alpha, color=clr[1], edgecolor=None)
    strong_fill = mpatches.Patch(facecolor=clr[2], alpha=1.0, linewidth=0)
    for p1, p2 in zip(strong_perc1, strong_perc2):
        ax.fill_between(x_s, p1, p2, alpha=alpha, color=clr[2], edgecolor=None)
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
    )

    if save:
        plt.savefig("./compare-waveform-integrate")

    # Medium
    ax = era.plots.plot_percentiles(medium)
    ax.set_xlabel(r"Time $[\mathrm{yr}]$")
    ax.set_ylabel(r"Temperature $[\mathrm{K}]$")
    plt.legend([r"$26\,\mathrm{Tg}$"])
    plastik.topside_legends(plt.gca())
    # Vertical line at the time of the eruption
    plt.gca().axvline(1850 + (31 + 15) / 356, c="k")
    plt.hlines(eq_temp, medium[0].time.min(), medium[0].time.max(), color="r")
    plt.text(
        medium[0].time.max(),
        eq_temp,
        f"{eq_temp:.3f} K",
        ha="right",
        color="r",
    )
    if save:
        plt.savefig("./medium-waveform")

    ax = era.plots.plot_percentiles(plus)
    ax.set_xlabel(r"Time $[\mathrm{yr}]$")
    ax.set_ylabel(r"Temperature $[\mathrm{K}]$")
    plt.legend([r"$400\,\mathrm{Tg}$"])
    plastik.topside_legends(plt.gca())
    # Vertical line at the time of the eruption
    plt.gca().axvline(1850 + (31 + 15) / 356, c="k")
    plt.hlines(eq_temp, plus[0].time.min(), plus[0].time.max(), color="r")
    plt.text(
        plus[0].time.max(),
        eq_temp,
        f"{eq_temp:.3f} K",
        ha="right",
        color="r",
    )
    if save:
        plt.savefig("./medium-plus-waveform")

    ax = era.plots.plot_percentiles(strong)
    ax.set_xlabel(r"Time $[\mathrm{yr}]$")
    ax.set_ylabel(r"Temperature $[\mathrm{K}]$")
    plt.legend([r"$1629\,\mathrm{Tg}$"])
    plastik.topside_legends(plt.gca())
    # Vertical line at the time of the eruption
    plt.gca().axvline(1850 + (31 + 15) / 356, c="k")
    plt.hlines(eq_temp, strong[0].time.min(), strong[0].time.max(), color="r")
    plt.text(
        strong[0].time.max(),
        eq_temp,
        f"{eq_temp:.3f} K",
        ha="right",
        color="r",
    )
    if save:
        plt.savefig("./strong-waveform")

def main():
    save = False
    waveform_integrate(do_fourier=True, save=save)
    waveform_max(do_fourier=True, save=save)
    if save:
        cosmoplots.combine(
            "compare-waveform-max.png", "compare-waveform-integrate.png"
        ).using(gravity="southwest", pos=(10, 60)).in_grid(1, 2).save(
            "compare-waveform.png"
        )
    plt.show()


if __name__ == "__main__":
    pass
