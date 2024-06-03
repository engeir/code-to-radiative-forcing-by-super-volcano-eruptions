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
from matplotlib import ticker
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
            superstrong,
            *_,
        ) = load_func(remove_seasonality=True, shift=0)
        for i, s in enumerate(strong):
            strong[i] = s[: len(medium[0])]
        for i, s in enumerate(superstrong):
            superstrong[i] = s[: len(medium[0])]
        self._version = version
        self.medium = medium
        self.plus = plus
        self.strong = strong
        self.superstrong = superstrong


class DoPlotting:
    """Class that takes care of all the plotting."""

    def __init__(self, print_summary: bool, version):
        self.print_summary = print_summary
        self.data = SetupNeededData(version)
        self.n_year = 6
        self.version = version
        self.m_c = core.config.LEGENDS["c2wm"]["c"]
        self.mp_c = core.config.LEGENDS["c2wmp"]["c"]
        self.s_c = core.config.LEGENDS["c2ws"]["c"]
        self.ss_c = core.config.LEGENDS["c2wss"]["c"]

    def _plot(  # noqa: PLR0913, PLR0915
        self,
        medium: tuple[float, np.ndarray],
        plus: tuple[float, np.ndarray],
        strong: tuple[float, np.ndarray],
        superstrong: tuple[float, np.ndarray],
        style: Literal["plot", "semilogy", "loglog"] = "plot",
    ) -> mpl.figure.Figure:
        # Percentiles
        low = np.linspace(MIN_PERCENTILE, 50, num=1, endpoint=False)
        high = np.linspace(50, MAX_PERCENTILE, num=1 + 1)[1:]
        ax = plt.figure().gca()
        getattr(ax, style)()
        ax.set_xlabel(r"Time after eruption $[\mathrm{yr}]$")
        if self.version == "temp":
            ax.set_ylabel("Normalised \ntemperature anomaly $[1]$")
            ax.set_ylim((-0.6, 1.7))
            ax1 = ax.inset_axes((0.2, 0.6, 0.33, 0.37))
            ax1.set_ylim((-0.5, 1.5))
        elif self.version == "rf":
            ax.set_ylabel("Normalised \nradiative forcing anomaly $[1]$")
            ax.set_ylim((-0.5, 1.5))
            ax1 = ax.inset_axes((0.2, 0.5, 0.33, 0.47))
            ax1.set_ylim((-0.5, 1.5))
        elif self.version == "aod":
            ax.set_ylabel("Normalised \naerosol optical depth anomaly $[1]$")
            ax1 = ax.inset_axes((0.2, 0.3, 0.33, 0.67))
        getattr(ax1, style)()
        if style != "plot":
            ax.set_ylim((1e-3, 3))
        if style == "loglog":
            # Find peak, set time = 0
            idm = int(np.argmax(medium[1]))
            idp = int(np.argmax(plus[1]))
            ids = int(np.argmax(strong[1]))
            idss = int(np.argmax(superstrong[1]))
        else:
            idm = 0
            idp = 0
            ids = 0
            idss = 0
        if not all(
            (
                (
                    self.data.medium[0].time.data[idm:]
                    == self.data.plus[0].time.data[idp:]
                ).all(),
                (
                    self.data.plus[0].time.data[idp:]
                    == self.data.strong[0].time.data[ids:]
                ).all(),
                (
                    self.data.strong[0].time.data[ids:]
                    == self.data.superstrong[0].time.data[idss:]
                ).all(),
            )
        ):
            raise ValueError("Time arrays are not equal.")
        x_ = self.data.medium[0].time.data[idm:]
        x_ -= x_[0]
        medium_scaled = medium[1][idm:]
        plus_scaled = plus[1][idp:]
        strong_scaled = strong[1][ids:]
        superstrong_scaled = superstrong[1][idss:]
        a = 0.7
        for p1, p2 in zip(
            np.percentile(self.data.medium, low, axis=0) / medium[0],
            np.percentile(self.data.medium, high, axis=0) / medium[0],
            strict=True,
        ):
            ax.fill_between(x_, p1[idm:], p2[idm:], alpha=a, color=self.m_c, ec=None)
            ax1.fill_between(x_, p1[idm:], p2[idm:], alpha=a, color=self.m_c, ec=None)
        for p1, p2 in zip(
            np.percentile(self.data.plus, low, axis=0) / plus[0],
            np.percentile(self.data.plus, high, axis=0) / plus[0],
            strict=True,
        ):
            ax.fill_between(x_, p1[idp:], p2[idp:], alpha=a, color=self.mp_c, ec=None)
            ax1.fill_between(x_, p1[idp:], p2[idp:], alpha=a, color=self.mp_c, ec=None)
        for p1, p2 in zip(
            np.percentile(self.data.strong, low, axis=0) / strong[0],
            np.percentile(self.data.strong, high, axis=0) / strong[0],
            strict=True,
        ):
            ax.fill_between(x_, p1[ids:], p2[ids:], alpha=a, color=self.s_c, ec=None)
            ax1.fill_between(x_, p1[ids:], p2[ids:], alpha=a, color=self.s_c, ec=None)
        for p1, p2 in zip(
            np.percentile(self.data.superstrong, low, axis=0) / superstrong[0],
            np.percentile(self.data.superstrong, high, axis=0) / superstrong[0],
            strict=True,
        ):
            ax.fill_between(x_, p1[idss:], p2[idss:], alpha=a, color=self.ss_c, ec=None)
            ax1.fill_between(
                x_, p1[idss:], p2[idss:], alpha=a, color=self.ss_c, ec=None
            )
        ax1.set_xlim((-0.5, 3.5))
        ax1.patch.set_alpha(0.3)
        ax1.xaxis.set_major_locator(ticker.MultipleLocator(1))
        ax1.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))

        # Combine shading and line labels
        plt.legend(
            [
                (
                    mpatches.Patch(facecolor=self.ss_c, alpha=1.0, linewidth=0),
                    ax.plot(x_, superstrong_scaled, "--", c="k")[0],
                ),
                (
                    mpatches.Patch(facecolor=self.s_c, alpha=1.0, linewidth=0),
                    ax.plot(x_, strong_scaled, "--", c="k")[0],
                ),
                (
                    mpatches.Patch(facecolor=self.mp_c, alpha=1.0, linewidth=0),
                    ax.plot(x_, plus_scaled, ":", c="k")[0],
                ),
                (
                    mpatches.Patch(facecolor=self.m_c, alpha=1.0, linewidth=0),
                    ax.plot(x_, medium_scaled, c="k")[0],
                ),
            ],
            [
                r"C2W$\uparrow\uparrow$, $C" + f" = {superstrong[0]:.2f}" + r"$",
                r"C2W$\uparrow$, $C" + f" = {strong[0]:.2f}" + r"$",
                f"C2W$-$, $C = {plus[0]:.2f}$",
                r"C2W$\downarrow$, $C" + f" = {medium[0]:.2f}" + r"$",
            ],
            loc="upper right",
            handler_map={
                "medium_line": HandlerLine2D(marker_pad=0),
                "plus_line": HandlerLine2D(marker_pad=0),
                "strong_line": HandlerLine2D(marker_pad=0),
                "superstrong_line": HandlerLine2D(marker_pad=0),
            },
            framealpha=0.6,
            fontsize=core.config.FONTSIZE,
        )
        ax1.plot(x_, medium_scaled, c="k")
        ax1.plot(x_, plus_scaled, ":", c="k")
        ax1.plot(x_, strong_scaled, "--", c="k")
        ax1.plot(x_, superstrong_scaled, "--", c="k")
        return plt.gcf()

    def waveform_max(
        self, style: Literal["plot", "semilogy", "loglog"] = "plot"
    ) -> mpl.figure.Figure:
        """Compare shape of TREFHT variable from medium and strong eruption simulations.

        The seasonal effects are removed by finding the median across four realisations.
        Comparison is done by shifting the signals to zero and then dividing by their
        maximum values.

        Parameters
        ----------
        style : Literal["plot", "semilogy", "loglog"]
            The axis style of the plot

        Returns
        -------
        mpl.figure.Figure
            The figure object that is created by the function
        """
        # Find median values
        medium_med = np.median(self.data.medium, axis=0)
        plus_med = np.median(self.data.plus, axis=0)
        strong_med = np.median(self.data.strong, axis=0)
        superstrong_med = np.median(self.data.superstrong, axis=0)
        extreme = (
            "max"
            if abs(self.data.medium[0].data.min()) < abs(self.data.medium[0].data.max())
            else "min"
        )
        filter_ = scipy.signal.savgol_filter
        medium_const = getattr(filter_(medium_med, self.n_year, 3), extreme)()
        plus_const = getattr(filter_(plus_med, self.n_year, 3), extreme)()
        strong_const = getattr(filter_(strong_med, self.n_year, 3), extreme)()
        superstrong_const = getattr(filter_(superstrong_med, self.n_year, 3), extreme)()
        medium_scaled = medium_med / medium_const
        plus_scaled = plus_med / plus_const
        strong_scaled = strong_med / strong_const
        superstrong_scaled = superstrong_med / superstrong_const
        return self._plot(
            (medium_const, medium_scaled),
            (plus_const, plus_scaled),
            (strong_const, strong_scaled),
            (superstrong_const, superstrong_scaled),
            style=style,
        )


def main(show_output: bool = False):
    """Run the main program."""
    TMP = tempfile.TemporaryDirectory()
    tmp_dir = pathlib.Path(TMP.name)
    save = True
    plotter_temp = DoPlotting(show_output, "temp")
    wmax_temp = plotter_temp.waveform_max()
    plotter_aod = DoPlotting(show_output, "aod")
    wmax_aod = plotter_aod.waveform_max()
    plotter_rf = DoPlotting(show_output, "rf")
    wmax_rf = plotter_rf.waveform_max()
    if save:
        SAVE_PATH = core.utils.if_save.create_savedir()
        wmax_aod.savefig(tmp_dir / "compare-waveform-max-aod")
        wmax_rf.savefig(tmp_dir / "compare-waveform-max-rf")
        wmax_temp.savefig(tmp_dir / "compare-waveform-max-temp")
        cosmoplots.combine(
            tmp_dir / "compare-waveform-max-aod.png",
            tmp_dir / "compare-waveform-max-rf.png",
            tmp_dir / "compare-waveform-max-temp.png",
        ).using(fontsize=8).in_grid(1, 3).save(SAVE_PATH / "figure1.png")
        if (fig1 := (SAVE_PATH / "figure1.png")).exists():
            print(f"Successfully saved figure 1 to {fig1.resolve()}")
    if show_output:
        plt.show()
    else:
        plt.close("all")
    TMP.cleanup()


if __name__ == "__main__":
    main(show_output=True)
