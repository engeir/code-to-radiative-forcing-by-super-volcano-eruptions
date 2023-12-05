"""Script that generates plots for figure 1."""

import pathlib
import tempfile
from typing import Literal

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

    def __init__(self, version: Literal["aod", "rf", "temp"]):
        if version == "aod":
            load_func = core.load.cesm2.get_aod_arrs
        elif version == "rf":
            load_func = core.load.cesm2.get_rf_arrs
        elif version == "temp":
            load_func = core.load.cesm2.get_trefht_arrs
        else:
            raise AttributeError("I do not recognize this version.")
        (
            medium,
            plus,
            strong,
            *_,
        ) = load_func(remove_seasonality=True, shift=0)
        for i, s in enumerate(strong):
            strong[i] = s[: len(medium[0])]
        self._version = version
        self.medium = medium
        self.plus = plus
        self.strong = strong


class DoPlotting:
    """Class that takes care of all the plotting."""

    def __init__(self, print_summary: bool, version):
        self.print_summary = print_summary
        self.data = SetupNeededData(version)
        self.n_year = 6
        self.version = version

    def _plot(
        self,
        medium,
        plus,
        strong,
    ) -> mpl.figure.Figure:
        medium_const, medium_scaled = medium
        plus_const, plus_scaled = plus
        strong_const, strong_scaled = strong
        # Percentiles
        n = 1
        low_range = np.linspace(MIN_PERCENTILE, 50, num=n, endpoint=False)
        high_range = np.linspace(50, MAX_PERCENTILE, num=n + 1)[1:]
        medium_perc1 = np.percentile(self.data.medium, low_range, axis=0)
        medium_perc1 = medium_perc1 / medium_const
        medium_perc2 = np.percentile(self.data.medium, high_range, axis=0)
        medium_perc2 = medium_perc2 / medium_const
        plus_perc1 = np.percentile(self.data.plus, low_range, axis=0)
        plus_perc1 = plus_perc1 / plus_const
        plus_perc2 = np.percentile(self.data.plus, high_range, axis=0)
        plus_perc2 = plus_perc2 / plus_const
        strong_perc1 = np.percentile(self.data.strong, low_range, axis=0)
        strong_perc1 = strong_perc1 / strong_const
        strong_perc2 = np.percentile(self.data.strong, high_range, axis=0)
        strong_perc2 = strong_perc2 / strong_const

        x_m = self.data.medium[0].time.data
        x_p = self.data.plus[0].time.data
        x_s = self.data.strong[0].time.data
        fig = plt.figure()
        ax = fig.gca()
        ax.set_xlabel(r"Time $[\mathrm{yr}]$")
        if self.version == "temp":
            attr_name = "temperature"
        elif self.version == "rf":
            attr_name = "radiative forcing"
        elif self.version == "aod":
            attr_name = "aerosol optical depth"
        ax.set_ylabel(f"Normalised \n{attr_name} anomaly $[1]$")
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
                r"C2W$\uparrow$, $C" + f" = {strong_const:.2f}" + r"$",
                f"C2W$-$, $C = {plus_const:.2f}$",
                r"C2W$\downarrow$, $C" + f" = {medium_const:.2f}" + r"$",
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
        # Find median values
        medium_med = np.median(self.data.medium, axis=0)
        plus_med = np.median(self.data.plus, axis=0)
        strong_med = np.median(self.data.strong, axis=0)
        medium_const = scipy.signal.savgol_filter(medium_med, self.n_year, 3).max()
        plus_const = scipy.signal.savgol_filter(plus_med, self.n_year, 3).max()
        strong_const = scipy.signal.savgol_filter(strong_med, self.n_year, 3).max()
        medium_scaled = medium_med / medium_const
        plus_scaled = plus_med / plus_const
        strong_scaled = strong_med / strong_const
        return self._plot(
            (medium_const, medium_scaled),
            (plus_const, plus_scaled),
            (strong_const, strong_scaled),
        )

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
        # Find median values
        medium_med = np.median(self.data.medium, axis=0)
        plus_med = np.median(self.data.plus, axis=0)
        strong_med = np.median(self.data.strong, axis=0)
        medium_const = np.trapz(medium_med, self.data.medium[0].time.data)
        plus_const = np.trapz(plus_med, self.data.plus[0].time.data)
        strong_const = np.trapz(strong_med, self.data.strong[0].time.data)
        medium_scaled = medium_med / medium_const
        plus_scaled = plus_med / plus_const
        strong_scaled = strong_med / strong_const

        return self._plot(
            (medium_const, medium_scaled),
            (plus_const, plus_scaled),
            (strong_const, strong_scaled),
        )


def main(show_output: bool = False):
    """Run the main program."""
    TMP = tempfile.TemporaryDirectory()
    tmp_dir = pathlib.Path(TMP.name)
    save = True
    plotter_aod = DoPlotting(show_output, "aod")
    wint_aod = plotter_aod.waveform_integrate()
    wmax_aod = plotter_aod.waveform_max()
    plotter_rf = DoPlotting(show_output, "rf")
    wint_rf = plotter_rf.waveform_integrate()
    wmax_rf = plotter_rf.waveform_max()
    plotter_temp = DoPlotting(show_output, "temp")
    wint_temp = plotter_temp.waveform_integrate()
    wmax_temp = plotter_temp.waveform_max()
    if save:
        SAVE_PATH = core.utils.if_save.create_savedir()
        wmax_aod.savefig(tmp_dir / "compare-waveform-max-aod")
        wint_aod.savefig(tmp_dir / "compare-waveform-integrate-aod")
        wmax_rf.savefig(tmp_dir / "compare-waveform-max-rf")
        wint_rf.savefig(tmp_dir / "compare-waveform-integrate-rf")
        wmax_temp.savefig(tmp_dir / "compare-waveform-max-temp")
        wint_temp.savefig(tmp_dir / "compare-waveform-integrate-temp")
        cosmoplots.combine(
            tmp_dir / "compare-waveform-max-temp.png",
            tmp_dir / "compare-waveform-integrate-temp.png",
        ).using(fontsize=50).in_grid(1, 2).save(SAVE_PATH / "figure1.png")
        cosmoplots.combine(
            tmp_dir / "compare-waveform-max-aod.png",
            tmp_dir / "compare-waveform-max-rf.png",
            tmp_dir / "compare-waveform-integrate-aod.png",
            tmp_dir / "compare-waveform-integrate-rf.png",
        ).using(fontsize=50).in_grid(2, 2).with_labels("(a)", "(c)", "(b)", "(d)").save(
            SAVE_PATH / "figure2.png"
        )
        if (fig1 := (SAVE_PATH / "figure1.png")).exists():
            print(f"Successfully saved figure 1 to {fig1.resolve()}")
        if (fig2 := (SAVE_PATH / "figure2.png")).exists():
            print(f"Successfully saved figure 2 to {fig2.resolve()}")
    if show_output:
        plt.show()
    else:
        plt.close("all")
    TMP.cleanup()


if __name__ == "__main__":
    main(show_output=True)
