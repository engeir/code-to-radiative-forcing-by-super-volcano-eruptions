"""Script that generates plots for figure 1."""

import pathlib
import tempfile

import cosmoplots
import matplotlib as mpl
import numpy as np
import scipy
from matplotlib import patches as mpatches
from matplotlib import pyplot as plt
from matplotlib.legend_handler import HandlerLine2D

import paper1_code as core

CLR = ["#1f77b4", "#ff7f0e", "#2ca02c"]
MIN_PERCENTILE = 5
MAX_PERCENTILE = 95


class SetupNeededData:
    """Class that loads all data used in the plotting procedures."""

    def __init__(self):
        (
            self.medium,
            self.plus,
            self.strong,
            *_,
            # ) = core.load.cesm2.get_aod_arrs(remove_seasonality=True, shift=0)
        ) = core.load.cesm2.get_rf_arrs(remove_seasonality=True, shift=0)
        # ) = core.load.cesm2.get_trefht_arrs(remove_seasonality=True)


class DoPlotting:
    """Class that takes care of all the plotting."""

    def __init__(self, print_summary: bool):
        self.print_summary = print_summary
        self.data = SetupNeededData()
        self.n_year = 6

    def waveform_max(self) -> mpl.figure.Figure:
        """Compare shape of TREFHT variable from medium and strong eruption simulations.

        The seasonal effects are removed by finding the median across four realisations.
        Comparison is done by shifting the signals to zero and then dividing by their
        maximum values.

        Returns
        -------
        mpl.figure.Figure
            The figure object that is created by the function
        """
        medium, plus, strong = self.data.medium, self.data.plus, self.data.strong
        for i, s in enumerate(strong):
            strong[i] = s[: len(medium[0])]

        # Find median values
        medium_med = np.median(medium, axis=0)
        plus_med = np.median(plus, axis=0)
        strong_med = np.median(strong, axis=0)
        medium_max = scipy.signal.savgol_filter(medium_med, self.n_year, 3).max()
        plus_max = scipy.signal.savgol_filter(plus_med, self.n_year, 3).max()
        strong_max = scipy.signal.savgol_filter(strong_med, self.n_year, 3).max()
        medium_scaled = medium_med / medium_max
        plus_scaled = plus_med / plus_max
        strong_scaled = strong_med / strong_max

        # Percentiles
        n = 1
        low_range = np.linspace(MIN_PERCENTILE, 50, num=n, endpoint=False)
        high_range = np.linspace(50, MAX_PERCENTILE, num=n + 1)[1:]
        medium_perc1 = np.percentile(medium, low_range, axis=0)
        medium_perc1 = medium_perc1 / medium_max
        medium_perc2 = np.percentile(medium, high_range, axis=0)
        medium_perc2 = medium_perc2 / medium_max
        plus_perc1 = np.percentile(plus, low_range, axis=0)
        plus_perc1 = plus_perc1 / plus_max
        plus_perc2 = np.percentile(plus, high_range, axis=0)
        plus_perc2 = plus_perc2 / plus_max
        strong_perc1 = np.percentile(strong, low_range, axis=0)
        strong_perc1 = strong_perc1 / strong_max
        strong_perc2 = np.percentile(strong, high_range, axis=0)
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
            loc="upper right",
            handler_map={
                medium_line: HandlerLine2D(marker_pad=0),
                plus_line: HandlerLine2D(marker_pad=0),
                strong_line: HandlerLine2D(marker_pad=0),
            },
            framealpha=0.6,
            fontsize=core.config.FONTSIZE,
        )
        return plt.gcf()

    def waveform_integrate(self) -> mpl.figure.Figure:
        """Compare shape of TREFHT variable from medium and strong eruption simulations.

        The median across four realisations is computed, with shading given from the 25th
        and 75th percentiles. Comparison is done by shifting the signals to zero and then
        dividing by their own integral.

        Returns
        -------
        mpl.figure.Figure
            The figure object that is created by the function
        """
        medium, plus, strong = self.data.medium, self.data.plus, self.data.strong
        for i, s in enumerate(strong):
            strong[i] = s[: len(medium[0])]

        # Find median values
        medium_med = np.median(medium, axis=0)
        plus_med = np.median(plus, axis=0)
        strong_med = np.median(strong, axis=0)
        medium_int = np.trapz(medium_med, medium[0].time.data)
        plus_int = np.trapz(plus_med, plus[0].time.data)
        strong_int = np.trapz(strong_med, strong[0].time.data)
        medium_scaled = medium_med / medium_int
        plus_scaled = plus_med / plus_int
        strong_scaled = strong_med / strong_int

        # Percentiles
        n = 1
        low_range = np.linspace(MIN_PERCENTILE, 50, num=n, endpoint=False)
        high_range = np.linspace(50, MAX_PERCENTILE, num=n + 1)[1:]
        medium_perc1 = np.percentile(medium, low_range, axis=0)
        medium_perc1 = medium_perc1 / medium_int
        medium_perc2 = np.percentile(medium, high_range, axis=0)
        medium_perc2 = medium_perc2 / medium_int
        plus_perc1 = np.percentile(plus, low_range, axis=0)
        plus_perc1 = plus_perc1 / plus_int
        plus_perc2 = np.percentile(plus, high_range, axis=0)
        plus_perc2 = plus_perc2 / plus_int
        strong_perc1 = np.percentile(strong, low_range, axis=0)
        strong_perc1 = strong_perc1 / strong_int
        strong_perc2 = np.percentile(strong, high_range, axis=0)
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
            loc="upper right",
            handler_map={
                medium_line: HandlerLine2D(marker_pad=0),
                plus_line: HandlerLine2D(marker_pad=0),
                strong_line: HandlerLine2D(marker_pad=0),
            },
            framealpha=0.6,
            fontsize=core.config.FONTSIZE,
        )
        return plt.gcf()


def main(show_output: bool = False):
    """Run the main program."""
    TMP = tempfile.TemporaryDirectory()
    tmp_dir = pathlib.Path(TMP.name)
    save = True
    plotter = DoPlotting(show_output)
    wint = plotter.waveform_integrate()
    wmax = plotter.waveform_max()
    if save:
        SAVE_PATH = core.utils.if_save.create_savedir()
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
    if show_output:
        plt.show()
    else:
        plt.close("all")
    TMP.cleanup()


if __name__ == "__main__":
    main(show_output=True)
