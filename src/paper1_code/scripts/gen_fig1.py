"""Script that generates plots for figure 1."""

from typing import Literal, overload

import matplotlib as mpl
import numpy as np
import plastik
import scipy
from matplotlib import patches as mpatches
from matplotlib import pyplot as plt
from matplotlib import ticker
from matplotlib.legend_handler import HandlerLine2D

import paper1_code as core

mpl.style.use(
    [
        "https://raw.githubusercontent.com/uit-cosmo/cosmoplots/main/cosmoplots/default.mplstyle",
        "paper1_code.extra",
        "paper1_code.jgr",
        {"legend.handlelength": 1.65},
    ],
)

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

    @overload
    def _plot(
        self,
        simulations: list[tuple[float, np.ndarray]],
        style: Literal["plot", "semilogy", "loglog"],
        ax: mpl.axes.Axes,
    ) -> mpl.axes.Axes: ...
    @overload
    def _plot(
        self,
        simulations: list[tuple[float, np.ndarray]],
        style: Literal["plot", "semilogy", "loglog"],
    ) -> mpl.figure.Figure: ...
    @overload
    def _plot(
        self,
        simulations: list[tuple[float, np.ndarray]],
    ) -> mpl.figure.Figure: ...
    def _plot(  # noqa: PLR0915
        self,
        simulations: list[tuple[float, np.ndarray]],
        style: Literal["plot", "semilogy", "loglog"] = "plot",
        ax: mpl.axes.Axes | None = None,
    ) -> mpl.figure.Figure | mpl.axes.Axes:
        # Percentiles
        low = np.linspace(MIN_PERCENTILE, 50, num=1, endpoint=False)
        high = np.linspace(50, MAX_PERCENTILE, num=1 + 1)[1:]
        ax_ = plt.figure().gca() if ax is None else ax
        getattr(ax_, style)()
        ax_.set_xlabel(r"Time after eruption $[\mathrm{yr}]$")
        ax_, ax1 = self._plot_create_axis_labels(ax_)
        getattr(ax1, style)()
        if style != "plot":
            ax_.set_ylim((1e-3, 3))
        if style == "loglog":
            # Find peak, set time = 0
            idm = int(np.argmax(simulations[0][1]))
            idp = int(np.argmax(simulations[1][1]))
            ids = int(np.argmax(simulations[2][1]))
            idss = int(np.argmax(simulations[3][1]))
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
        medium_scaled = simulations[0][1][idm:]
        plus_scaled = simulations[1][1][idp:]
        strong_scaled = simulations[2][1][ids:]
        superstrong_scaled = simulations[3][1][idss:]
        a = 0.7
        for p1, p2 in zip(
            np.percentile(self.data.medium, low, axis=0) / simulations[0][0],
            np.percentile(self.data.medium, high, axis=0) / simulations[0][0],
            strict=True,
        ):
            ax_.fill_between(x_, p1[idm:], p2[idm:], alpha=a, color=self.m_c, ec=None)
            ax1.fill_between(x_, p1[idm:], p2[idm:], alpha=a, color=self.m_c, ec=None)
        for p1, p2 in zip(
            np.percentile(self.data.plus, low, axis=0) / simulations[1][0],
            np.percentile(self.data.plus, high, axis=0) / simulations[1][0],
            strict=True,
        ):
            ax_.fill_between(x_, p1[idp:], p2[idp:], alpha=a, color=self.mp_c, ec=None)
            ax1.fill_between(x_, p1[idp:], p2[idp:], alpha=a, color=self.mp_c, ec=None)
        for p1, p2 in zip(
            np.percentile(self.data.strong, low, axis=0) / simulations[2][0],
            np.percentile(self.data.strong, high, axis=0) / simulations[2][0],
            strict=True,
        ):
            ax_.fill_between(x_, p1[ids:], p2[ids:], alpha=a, color=self.s_c, ec=None)
            ax1.fill_between(x_, p1[ids:], p2[ids:], alpha=a, color=self.s_c, ec=None)
        for p1, p2 in zip(
            np.percentile(self.data.superstrong, low, axis=0) / simulations[3][0],
            np.percentile(self.data.superstrong, high, axis=0) / simulations[3][0],
            strict=True,
        ):
            ax_.fill_between(
                x_, p1[idss:], p2[idss:], alpha=a, color=self.ss_c, ec=None
            )
            ax1.fill_between(
                x_, p1[idss:], p2[idss:], alpha=a, color=self.ss_c, ec=None
            )
        ax1.patch.set_alpha(0.3)
        ax1.xaxis.set_major_locator(ticker.MultipleLocator(1))
        ax1.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))

        # Combine shading and line labels
        if self.version == "temp":
            s26 = ""
            s400 = ""
            s1629 = ""
            s3000 = ""
            unit = r"Unit: $\mathrm{K}$"
        elif self.version == "rf":
            s26 = ""
            s400 = ""
            s1629 = ""
            s3000 = ""
            unit = r"Unit: $\mathrm{W/m^{2}}$"
        elif self.version == "aod":
            s26 = f"{core.config.LEGENDS['c2wm']['label']}, "
            s400 = f"{core.config.LEGENDS['c2wmp']['label']}, "
            s1629 = f"{core.config.LEGENDS['c2ws']['label']}, "
            s3000 = f"{core.config.LEGENDS['c2wss']['label']}, "
            unit = r"Unit: $1$"
        ax_.legend(
            [
                (
                    mpatches.Patch(facecolor=self.ss_c, alpha=1.0, linewidth=0),
                    ax_.plot(x_, superstrong_scaled, "-.", c="k")[0],
                ),
                (
                    mpatches.Patch(facecolor=self.s_c, alpha=1.0, linewidth=0),
                    ax_.plot(x_, strong_scaled, "--", c="k")[0],
                ),
                (
                    mpatches.Patch(facecolor=self.mp_c, alpha=1.0, linewidth=0),
                    ax_.plot(x_, plus_scaled, ":", c="k")[0],
                ),
                (
                    mpatches.Patch(facecolor=self.m_c, alpha=1.0, linewidth=0),
                    ax_.plot(x_, medium_scaled, c="k")[0],
                ),
            ],
            [
                s3000 + f"${core.utils.misc.n_significant(simulations[3][0], 3)}$",
                s1629 + f"${core.utils.misc.n_significant(simulations[2][0], 3)}$",
                s400 + f"${core.utils.misc.n_significant(simulations[1][0], 3)}$",
                s26 + f"${core.utils.misc.n_significant(simulations[0][0], 3)}$",
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
            title=unit,
        )
        ax1.plot(x_, medium_scaled, c="k")
        ax1.plot(x_, plus_scaled, ":", c="k")
        ax1.plot(x_, strong_scaled, "--", c="k")
        ax1.plot(x_, superstrong_scaled, "-.", c="k")
        return plt.gcf() if ax is None else ax_

    def _plot_create_axis_labels(
        self, ax_: mpl.axes.Axes
    ) -> tuple[mpl.axes.Axes, mpl.axes.Axes]:
        # length = 25
        # ax_.set_xlim((-0.05 * length, 1.05 * length))
        if self.version == "temp":
            ax_.set_ylabel("Normalised \nGMST anomaly $[1]$")
            ax_.set_ylim((-0.4, 1.6))
            ax1 = core.utils.misc.create_axes_inset(
                ax_, (-0.5, 3.5, -0.3, 1.2), (0.3, 0.5, 0.33, 0.47)
            )
        elif self.version == "rf":
            ax_.set_ylabel("Normalised \nERF anomaly $[1]$")
            ax_.set_ylim((-0.4, 1.6))
            ax1 = core.utils.misc.create_axes_inset(
                ax_, (-0.5, 3.5, -0.2, 1.3), (0.3, 0.5, 0.33, 0.47)
            )
        elif self.version == "aod":
            ax_.set_ylabel("Normalised \nSAOD anomaly $[1]$")
            ax1 = core.utils.misc.create_axes_inset(
                ax_, (-0.5, 3.5, -0.03, 1.03), (0.3, 0.3, 0.33, 0.67)
            )
        return ax_, ax1

    @overload
    def waveform_max(
        self, style: Literal["plot", "semilogy", "loglog"], ax: mpl.axes.Axes
    ) -> mpl.axes.Axes: ...
    @overload
    def waveform_max(
        self, style: Literal["plot", "semilogy", "loglog"]
    ) -> mpl.figure.Figure: ...
    def waveform_max(
        self,
        style: Literal["plot", "semilogy", "loglog"],
        ax: mpl.axes.Axes | None = None,
    ) -> mpl.figure.Figure | mpl.axes.Axes:
        """Compare shape of TREFHT variable from medium and strong eruption simulations.

        The seasonal effects are removed by finding the median across four realisations.
        Comparison is done by shifting the signals to zero and then dividing by their
        maximum values.

        Parameters
        ----------
        style : Literal["plot", "semilogy", "loglog"]
            The axis style of the plot
        ax : mpl.axes.Axes | None
            The axes that should be used for the plotting, otherwise a new figure is
            created.

        Returns
        -------
        mpl.figure.Figure | mpl.axes.Axes
            The figure object that is created by the function, or the updated axes.
        """
        if self.version == "aod":
            self._convert_aod()
        # Find median values
        # medium_med = np.median(self.data.medium, axis=0)
        # plus_med = np.median(self.data.plus, axis=0)
        # strong_med = np.median(self.data.strong, axis=0)
        # superstrong_med = np.median(self.data.superstrong, axis=0)
        medium_med = core.utils.time_series.get_median(
            self.data.medium, xarray=True
        ).data
        plus_med = core.utils.time_series.get_median(self.data.plus, xarray=True).data
        strong_med = core.utils.time_series.get_median(
            self.data.strong, xarray=True
        ).data
        superstrong_med = core.utils.time_series.get_median(
            self.data.superstrong, xarray=True
        ).data
        extreme = (
            "max"
            if abs(self.data.medium[0].data.min()) < abs(self.data.medium[0].data.max())
            else "min"
        )
        filter_ = scipy.signal.savgol_filter
        medium_const, plus_const, strong_const, superstrong_const, _ = (
            core.load.cesm2.get_rf_c2w_peaks()
        )
        medium_const = getattr(filter_(medium_med, self.n_year, 3), extreme)()
        plus_const = getattr(filter_(plus_med, self.n_year, 3), extreme)()
        strong_const = getattr(filter_(strong_med, self.n_year, 3), extreme)()
        superstrong_const = getattr(filter_(superstrong_med, self.n_year, 3), extreme)()
        medium_scaled = medium_med / medium_const
        plus_scaled = plus_med / plus_const
        strong_scaled = strong_med / strong_const
        superstrong_scaled = superstrong_med / superstrong_const
        return self._plot(
            [
                (medium_const, medium_scaled),
                (plus_const, plus_scaled),
                (strong_const, strong_scaled),
                (superstrong_const, superstrong_scaled),
            ],
            style,
            ax=ax,  # type: ignore[arg-type]
        )

    def _convert_aod(self):
        _medium = self.data.medium[:]
        for i, _m in enumerate(_medium):
            _medium[i].data = core.utils.time_series.convert_aod(_m.data)
        self.data.medium = _medium
        _plus = self.data.plus[:]
        for i, _p in enumerate(_plus):
            _plus[i].data = core.utils.time_series.convert_aod(_p.data)
        _strong = self.data.strong[:]
        self.data.plus = _plus
        for i, _s in enumerate(_strong):
            _strong[i].data = core.utils.time_series.convert_aod(_s.data)
        self.data.strong = _strong
        _superstrong = self.data.superstrong[:]
        for i, _ss in enumerate(_superstrong):
            _superstrong[i].data = core.utils.time_series.convert_aod(_ss.data)
        self.data.superstrong = _superstrong


def main(show_output: bool = False):
    """Run the main program."""
    save = True
    fig, axs = plastik.figure_grid(rows=3, columns=1, using={"share_axes": "x"})
    plotter_temp = DoPlotting(show_output, "temp")
    plotter_temp.waveform_max(style="plot", ax=axs[2])
    plotter_aod = DoPlotting(show_output, "aod")
    plotter_aod.waveform_max(style="plot", ax=axs[0])
    plotter_rf = DoPlotting(show_output, "rf")
    plotter_rf.waveform_max(style="plot", ax=axs[1])
    if save:
        SAVE_PATH = core.utils.if_save.create_savedir()
        fig.savefig(SAVE_PATH / "figure1")
        if (fig1 := (SAVE_PATH / "figure1.pdf")).exists():
            print(f"Successfully saved figure 1 to {fig1.resolve()}")
    if show_output:
        plt.show()
    else:
        plt.close("all")


if __name__ == "__main__":
    main(show_output=True)
