"""Script that generates plots for figure 4."""

import os
from typing import overload

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import plastik
import scipy.stats

import paper1_code as core

convert_aod = core.utils.time_series.convert_aod
xlim_so2 = (-150, 3700)


class SetupNeededData:
    """Class that loads all data used in the plotting procedures."""

    def __init__(self):
        # C2W
        self.so2 = core.load.cesm2.get_so2_c2w_peaks()
        self.aod = convert_aod(core.load.cesm2.get_aod_c2w_peaks())
        self.rf = core.load.cesm2.get_rf_c2w_peaks()
        self.rf_coupled = core.load.cesm2.get_rf_coupled_c2w_peaks()
        self.temp = core.load.cesm2.get_trefht_c2w_peaks()
        # Marshall et al. 2020
        self.so2_m20, self.aod_m20, self.rf_m20, self.temp_m20 = core.load.m20.get_m20(
            find_all_peaks=True
        )
        self.aod_m20 = convert_aod(self.aod_m20)
        # Otto-Bliesner et al. 2016
        self.so2_ob16, self.rf_ob16, self.temp_ob16 = core.load.ob16.get_ob16()
        # Mt. Pinatubo
        self.so2_pinatubo, self.aod_pinatubo, self.rf_pinatubo, self.temp_pinatubo = (
            core.load.pinatubo.get_so2_pinatubo(),
            convert_aod(core.load.pinatubo.get_aod_pinatubo()),
            core.load.pinatubo.get_rf_pinatubo(),
            core.load.pinatubo.get_trefht_pinatubo(),
        )
        # Mt. Tambora
        self.so2_tambora = core.load.tambora.get_so2_tambora()
        self.aod_tambora = convert_aod(core.load.tambora.get_aod_tambora())
        self.rf_tambora = core.load.tambora.get_rf_tambora()
        self.temp_tambora = core.load.tambora.get_trefht_tambora()
        # Jones et al. 2005
        self.so2_j05, self.aod_j05, self.rf_j05, self.temp_j05 = (
            core.load.j05.get_so2_j05(),
            convert_aod(core.load.j05.get_aod_j05()),
            core.load.j05.get_rf_j05(),
            core.load.j05.get_trefht_j05(),
        )
        # Robock et al. 2009
        self.so2_r09, self.rf_r09, self.temp_r09 = (
            core.load.r09.get_so2_r09(),
            core.load.r09.get_rf_r09(),
            core.load.r09.get_trefht_r09(),
        )
        # Timmreck et al. 2010
        self.so2_t10, self.aod_t10, self.rf_t10, self.temp_t10 = (
            core.load.t10.get_so2_t10(),
            convert_aod(core.load.t10.get_aod_t10()),
            core.load.t10.get_rf_t10(),
            core.load.t10.get_trefht_t10(),
        )
        # English et al. 2013
        self.so2_e13, self.aod_e13 = (
            core.load.e13.get_so2_e13(),
            convert_aod(core.load.e13.get_aod_e13()),
        )
        # Metzner et al. 2014
        self.so2_m14, self.aod_m14, self.rf_m14, self.temp_m14 = (
            core.load.m14.get_so2_m14(),
            convert_aod(core.load.m14.get_aod_m14()),
            core.load.m14.get_rf_m14(),
            core.load.m14.get_trefht_m14(),
        )
        # Brenna et al. 2020
        self.so2_b20, self.aod_b20, self.rf_b20, self.temp_b20 = (
            core.load.b20.get_so2_b20(),
            convert_aod(core.load.b20.get_aod_b20()),
            core.load.b20.get_rf_b20(),
            core.load.b20.get_trefht_b20(),
        )
        # Osipov et al. 2020
        self.so2_osi20, self.aod_osi20, self.temp_osi20 = (
            core.load.osi20.get_so2_osi20(),
            convert_aod(core.load.osi20.get_aod_osi20()),
            core.load.osi20.get_trefht_osi20(),
        )
        # McGraw et al. 2024
        self.so2_mcg24, self.rf_mcg24, self.temp_mcg24 = (
            core.load.mcg24.get_so2_mcg24(),
            core.load.mcg24.get_rf_mcg24(),
            core.load.mcg24.get_trefht_mcg24(),
        )


class DoPlotting:
    """Class that takes care of all the plotting."""

    def __init__(self, print_summary: bool):
        self.print_summary = print_summary
        self.data = SetupNeededData()

    @overload
    def plot_so2_vs_aod(self, ax: mpl.axes.Axes) -> mpl.axes.Axes: ...
    @overload
    def plot_so2_vs_aod(self) -> mpl.figure.Figure: ...
    def plot_so2_vs_aod(
        self, ax: mpl.axes.Axes | None = None
    ) -> mpl.figure.Figure | mpl.axes.Axes:
        """Plot SO2 against AOD peaks."""
        ihl = self.data.so2[-1]
        ahl = self.data.aod[-1]
        ax_ = (fig5_a := plt.figure()).gca() if ax is None else ax
        x_lin = np.linspace(30, 3000)
        coeff = self.data.aod[-2] / 3000 ** (2 / 3)
        ax_.plot(
            x_lin,
            coeff * x_lin ** (2 / 3),
            ls="--",
            c="grey",
            label=r"$\propto\mathrm{SO_2}^{2/3}$",
        )
        if os.environ["AOD"] == "exp":
            ax_.semilogy(
                self.data.so2[:-1], self.data.aod[:-1], **core.config.LEGENDS["c2w"]
            )
        else:
            ax_.plot(
                self.data.so2[:-1], self.data.aod[:-1], **core.config.LEGENDS["c2w"]
            )
        ax_.scatter(ihl, ahl, **core.config.LEGENDS["c2wn"])
        ax_.scatter(self.data.so2_m20, self.data.aod_m20, **core.config.LEGENDS["m20*"])
        ax_.plot(self.data.so2_e13, self.data.aod_e13, **core.config.LEGENDS["e13"])
        ax_.plot(self.data.so2_m14, self.data.aod_m14, **core.config.LEGENDS["m14"])
        ax_.plot(self.data.so2_b20, self.data.aod_b20, **core.config.LEGENDS["b20"])
        ax_.plot(
            self.data.so2_osi20, self.data.aod_osi20, **core.config.LEGENDS["osi20"]
        )
        ax_.scatter(
            self.data.so2_pinatubo, self.data.aod_pinatubo, **core.config.LEGENDS["P"]
        )
        ax_.scatter(
            self.data.so2_tambora, self.data.aod_tambora, **core.config.LEGENDS["VT"]
        )
        ax_.scatter(self.data.so2_j05, self.data.aod_j05, **core.config.LEGENDS["P100"])
        ax_.scatter(self.data.so2_t10, self.data.aod_t10, **core.config.LEGENDS["t10"])
        ax1 = core.utils.misc.create_axes_inset(
            ax_, (0, 110, 0, 1), (0.62, 0.1, 0.35, 0.4), "lr->lr", "ul->ul"
        )
        ax1.plot(self.data.so2[:-1], self.data.aod[:-1], **core.config.LEGENDS["c2w"])
        ax1.scatter(
            self.data.so2_pinatubo, self.data.aod_pinatubo, **core.config.LEGENDS["P"]
        )
        ax1.scatter(
            self.data.so2_tambora, self.data.aod_tambora, **core.config.LEGENDS["VT"]
        )
        ax1.scatter(self.data.so2_m20, self.data.aod_m20, **core.config.LEGENDS["m20*"])
        ax1.plot(self.data.so2_e13, self.data.aod_e13, **core.config.LEGENDS["e13"])
        ax1.plot(self.data.so2_m14, self.data.aod_m14, **core.config.LEGENDS["m14"])
        ax1.plot(self.data.so2_b20, self.data.aod_b20, **core.config.LEGENDS["b20"])
        ax1.plot(
            self.data.so2_osi20, self.data.aod_osi20, **core.config.LEGENDS["osi20"]
        )
        ax1.set_yticks([0, 1])
        ax1.patch.set_alpha(0.8)
        ax_.set_xlim(xlim_so2)
        ax_.set_xlabel(r"Injected $\mathrm{SO_2}$ [Tg]")
        ax_.set_ylabel("AOD [1]")
        if ax is None:
            kwargs = {
                "loc": "upper right" if os.environ["AOD"] == "exp" else "upper left",
                "framealpha": 0.8,
                "edgecolor": "gray",
                "fontsize": core.config.FONTSIZE,
                "ncol": 2,
                "labelspacing": 0.3,
                "handletextpad": 0.2,
                "columnspacing": 0.3,
            }
            ax_.legend(**kwargs)
        return fig5_a if ax is None else ax_

    @overload
    def plot_so2_vs_rf(self, ax: mpl.axes.Axes) -> mpl.axes.Axes: ...
    @overload
    def plot_so2_vs_rf(self) -> mpl.figure.Figure: ...
    def plot_so2_vs_rf(  # noqa: PLR0915
        self, ax: mpl.axes.Axes | None = None
    ) -> mpl.figure.Figure | mpl.axes.Axes:
        """Plot SO2 against RF peaks."""
        ytt_leg = core.config.LEGENDS["P100"].copy()
        ytt_leg.pop("marker")
        ytt_leg.pop("label")
        c2w_leg = core.config.LEGENDS["c2w"].copy()
        c2w_leg["ls"] = "--"
        c2w_leg["marker"] = core.config.POINTS_DICTS["triangle_right"]
        c2w_leg["label"] = "STrop$^{a}$"
        thl_leg = core.config.LEGENDS["c2wn"].copy()
        thl_leg.pop("marker")
        thl_leg["marker"] = core.config.POINTS_DICTS["tri_right"]
        ihl = self.data.so2[-1]
        thl = self.data.rf[-1]
        thl_coup = self.data.rf_coupled[-1]
        ax_ = (fig5_b := plt.figure()).gca() if ax is None else ax
        ax_.plot(self.data.so2[:-1], self.data.rf[:-1], **core.config.LEGENDS["c2w"])
        ax_.plot(self.data.so2[:-1], self.data.rf_coupled[:-1], **c2w_leg)
        ax_.scatter(ihl, thl, **core.config.LEGENDS["c2wn"])
        ax_.scatter(ihl, thl_coup, **thl_leg)
        ax_.scatter(
            self.data.so2_ob16, self.data.rf_ob16, **core.config.LEGENDS["ob16"]
        )
        ax_.scatter(self.data.so2_m20, self.data.rf_m20, **core.config.LEGENDS["m20*"])
        # ax_.plot(self.data.so2_r09, self.data.rf_r09, **core.config.LEGENDS["r09"])
        ax_.plot(self.data.so2_b20, self.data.rf_b20, **core.config.LEGENDS["b20"])
        ax_.plot(self.data.so2_m14, self.data.rf_m14, **core.config.LEGENDS["m14"])
        ax_.plot(
            self.data.so2_mcg24, self.data.rf_mcg24, **core.config.LEGENDS["mcg24"]
        )
        ax_.scatter(
            self.data.so2_pinatubo, self.data.rf_pinatubo, **core.config.LEGENDS["P"]
        )
        ax_.scatter(
            self.data.so2_tambora, self.data.rf_tambora, **core.config.LEGENDS["VT"]
        )
        ax_.scatter(self.data.so2_j05, self.data.rf_j05, **core.config.LEGENDS["P100"])
        ax_.scatter(self.data.so2_t10, self.data.rf_t10, **core.config.LEGENDS["t10"])
        # Fit from Niemeier and Timreck (2015) (they use S, and not SO2, which has half
        # the mass)
        # s = np.linspace(0, 3000 // 2, 10000)
        # warnings.simplefilter("ignore")
        # Dividing by zero is fine...
        # rf = 65 * np.exp(-((2246 / s) ** (0.23)))
        # warnings.resetwarnings()
        # ax_.plot(s * 2, rf, "--", label="N15", c=ytt_leg["c"])
        # x_aod = np.linspace(0, 3000, 1000)
        # ax.plot(x_aod, 5 * x_aod**(1/3), label="sqrt")
        # ax.plot(x_aod, 6 * np.log(x_aod + 1), label="log")
        # ax1.set_xlim((0, 190))
        # ax1.set_ylim((-2.2, 20))
        # Inset
        x0, y0, width, height = 0.62, 0.1, 0.35, 0.4
        x1, x2, y1, y2 = 0, 190, -2.2, 20
        ax1 = core.utils.misc.create_axes_inset(
            ax_, (x1, x2, y1, y2), (x0, y0, width, height), "lr->lr", "ul->ul"
        )
        ax1.plot(self.data.so2[:-1], self.data.rf[:-1], **core.config.LEGENDS["c2w"])
        ax1.plot(self.data.so2[:-1], self.data.rf_coupled[:-1], **c2w_leg)
        ax1.scatter(ihl, thl, **core.config.LEGENDS["c2wn"])
        ax1.scatter(ihl, thl_coup, **thl_leg)
        ax1.scatter(
            self.data.so2_ob16, self.data.rf_ob16, **core.config.LEGENDS["ob16"]
        )
        ax1.scatter(self.data.so2_m20, self.data.rf_m20, **core.config.LEGENDS["m20*"])
        ax1.plot(self.data.so2_b20, self.data.rf_b20, **core.config.LEGENDS["b20"])
        ax1.plot(self.data.so2_m14, self.data.rf_m14, **core.config.LEGENDS["m14"])
        ax1.plot(
            self.data.so2_mcg24, self.data.rf_mcg24, **core.config.LEGENDS["mcg24"]
        )
        ax1.scatter(
            self.data.so2_pinatubo, self.data.rf_pinatubo, **core.config.LEGENDS["P"]
        )
        ax1.scatter(
            self.data.so2_tambora, self.data.rf_tambora, **core.config.LEGENDS["VT"]
        )
        ax1.scatter(self.data.so2_j05, self.data.rf_j05, **core.config.LEGENDS["P100"])
        ax1.scatter(self.data.so2_t10, self.data.rf_t10, **core.config.LEGENDS["t10"])
        # ax1.plot(s * 2, rf, "--", label="N15", c=ytt_leg["c"])
        ax1.patch.set_alpha(0.8)
        ax_.set_xlim(xlim_so2)
        ax_.set_xlabel(r"Injected $\mathrm{SO_2}$ [Tg]")
        ax_.set_ylabel("ERF $[\\mathrm{W/m^2}]$")
        if ax is None:
            kwargs = {
                "loc": "upper left",
                "framealpha": 0.8,
                "edgecolor": "gray",
                "fontsize": core.config.FONTSIZE,
                "ncol": 2,
                "labelspacing": 0.3,
                "handletextpad": 0.2,
                "columnspacing": 0.3,
            }
            ax_.legend(**kwargs)
        return fig5_b if ax is None else ax_

    @overload
    def plot_so2_vs_temp(self, ax: mpl.axes.Axes) -> mpl.axes.Axes: ...
    @overload
    def plot_so2_vs_temp(self) -> mpl.figure.Figure: ...
    def plot_so2_vs_temp(
        self, ax: mpl.axes.Axes | None = None
    ) -> mpl.figure.Figure | mpl.axes.Axes:
        """Plot SO2 against temperature peaks."""
        c2wsn_temp = self.data.temp[-1]
        ax_ = (fig5_c := plt.figure()).gca() if ax is None else ax
        ax_.plot(self.data.so2[:-1], self.data.temp[:-1], **core.config.LEGENDS["c2w"])
        ax_.scatter(self.data.so2[-1], c2wsn_temp, **core.config.LEGENDS["c2wn"])
        self._plot_so2_temp_common_data(ax_)
        ax_.scatter(
            self.data.so2_j05, self.data.temp_j05, **core.config.LEGENDS["P100"]
        )
        ax_.scatter(self.data.so2_t10, self.data.temp_t10, **core.config.LEGENDS["t10"])
        ax_1 = core.utils.misc.create_axes_inset(
            ax_, (0, 190, -0.4, 1.5), (0.62, 0.1, 0.35, 0.4), "lr->lr", "ul->ul"
        )
        ax_1.plot(self.data.so2[:-1], self.data.temp[:-1], **core.config.LEGENDS["c2w"])
        self._plot_so2_temp_common_data(ax_1)
        ax_1.patch.set_alpha(0.8)
        ax_.set_xlim(xlim_so2)
        ax_.set_ylim((-0.75, 15.75))
        ax_.set_xlabel(r"Injected $\mathrm{SO_2}$ [Tg]")
        ax_.set_ylabel("GMST [K]")
        if ax is None:
            kwargs = {
                "loc": "upper left",
                "framealpha": 0.8,
                "edgecolor": "gray",
                "fontsize": core.config.FONTSIZE,
                "ncol": 2,
                "labelspacing": 0.3,
                "handletextpad": 0.2,
                "columnspacing": 0.3,
            }
            ax_.legend(**kwargs)
        return fig5_c if ax is None else ax_

    def _plot_so2_temp_common_data(self, ax):
        ax.scatter(
            self.data.so2_ob16, self.data.temp_ob16, **core.config.LEGENDS["ob16"]
        )
        ax.scatter(self.data.so2_m20, self.data.temp_m20, **core.config.LEGENDS["m20*"])
        ax.plot(self.data.so2_b20, self.data.temp_b20, **core.config.LEGENDS["b20"])
        ax.plot(
            self.data.so2_mcg24, self.data.temp_mcg24, **core.config.LEGENDS["mcg24"]
        )
        ax.plot(self.data.so2_m14, self.data.temp_m14, **core.config.LEGENDS["m14"])
        ax.plot(
            self.data.so2_osi20, self.data.temp_osi20, **core.config.LEGENDS["osi20"]
        )
        ax.scatter(
            self.data.so2_pinatubo, self.data.temp_pinatubo, **core.config.LEGENDS["P"]
        )
        ax.scatter(
            self.data.so2_tambora, self.data.temp_tambora, **core.config.LEGENDS["VT"]
        )
        ax.plot(self.data.so2_r09, self.data.temp_r09, **core.config.LEGENDS["r09"])

    @overload
    def plot_aod_vs_rf(self, ax: mpl.axes.Axes) -> mpl.axes.Axes: ...
    @overload
    def plot_aod_vs_rf(self) -> mpl.figure.Figure: ...
    def plot_aod_vs_rf(
        self, ax: mpl.axes.Axes | None = None
    ) -> mpl.figure.Figure | mpl.axes.Axes:
        """Plot AOD peaks against RF peaks."""
        c2w_leg = core.config.LEGENDS["c2w"].copy()
        c2w_leg["ls"] = "--"
        c2w_leg["marker"] = core.config.POINTS_DICTS["triangle_right"]
        c2w_leg["label"] = "STrop$^{a}$"
        aod_hl = self.data.aod[-1]
        rf_hl = self.data.rf[-1]
        rf_hl_coup = self.data.rf_coupled[-1]
        rf_m20 = self.data.rf_m20[np.argsort(self.data.aod_m20)]
        aod_m20 = self.data.aod_m20[np.argsort(self.data.aod_m20)]
        ax_ = (fig5_d := plt.figure()).gca() if ax is None else ax
        ax_.plot(self.data.aod[:-1], self.data.rf[:-1], **core.config.LEGENDS["c2w"])
        ax_.plot(self.data.aod[:-1], self.data.rf_coupled[:-1], **c2w_leg)
        self._plot_aod_rf_data(ax_, aod_hl, rf_hl, rf_hl_coup)
        ax_.scatter(aod_m20, rf_m20, **core.config.LEGENDS["m20*"])
        ax_.plot(self.data.aod_b20, self.data.rf_b20, **core.config.LEGENDS["b20"])
        ax_.plot(self.data.aod_m14, self.data.rf_m14, **core.config.LEGENDS["m14"])
        if os.environ["AOD"] == "exp":
            ax_1 = core.utils.misc.create_axes_inset(
                ax_, (0, 0.65, 0, 19), (0.45, 0.52, 0.4, 0.4), "lr->lr", "ul->ul"
            )
        else:
            ax_1 = core.utils.misc.create_axes_inset(
                ax_, (0, 1, 0, 19), (0.57, 0.12, 0.4, 0.4), "lr->lr", "ul->ul"
            )
        ax_1.plot(self.data.aod, self.data.rf, **core.config.LEGENDS["c2w"])
        ax_1.plot(self.data.aod, self.data.rf_coupled, **c2w_leg)
        self._plot_aod_rf_data(ax_1, aod_hl, rf_hl, rf_hl_coup)
        ax_1.plot(self.data.aod_b20, self.data.rf_b20, **core.config.LEGENDS["b20"])
        ax_1.plot(self.data.aod_m14, self.data.rf_m14, **core.config.LEGENDS["m14"])
        ax_1.scatter(aod_m20, rf_m20, **core.config.LEGENDS["m20*"])
        ax_1.patch.set_alpha(0.8)
        ax_.set_xlabel("AOD [1]")
        ax_.set_ylabel("ERF $[\\mathrm{W/m^2}]$")
        if ax is None:
            kwargs = {
                "loc": "upper left",
                "framealpha": 0.8,
                "edgecolor": "gray",
                "fontsize": core.config.FONTSIZE,
                "ncol": 2,
                "labelspacing": 0.3,
                "handletextpad": 0.2,
                "columnspacing": 0.3,
            }
            ax_.legend(**kwargs)
        return fig5_d if ax is None else ax_

    def _plot_aod_rf_data(self, ax, aod_hl, rf_hl, rf_hl_coup):
        thl_leg = core.config.LEGENDS["c2wn"].copy()
        thl_leg.pop("marker")
        thl_leg["marker"] = core.config.POINTS_DICTS["tri_right"]
        ax.scatter(aod_hl, rf_hl, **core.config.LEGENDS["c2wn"])
        ax.scatter(aod_hl, rf_hl_coup, **thl_leg)
        ax.scatter(
            self.data.aod_pinatubo, self.data.rf_pinatubo, **core.config.LEGENDS["P"]
        )
        ax.scatter(
            self.data.aod_tambora, self.data.rf_tambora, **core.config.LEGENDS["VT"]
        )
        ax.scatter(self.data.aod_j05, self.data.rf_j05, **core.config.LEGENDS["P100"])
        ax.scatter(self.data.aod_t10, self.data.rf_t10, **core.config.LEGENDS["t10"])

    @overload
    def plot_aod_vs_temperature(self, ax: mpl.axes.Axes) -> mpl.axes.Axes: ...
    @overload
    def plot_aod_vs_temperature(self) -> mpl.figure.Figure: ...
    def plot_aod_vs_temperature(
        self, ax: mpl.axes.Axes | None = None
    ) -> mpl.figure.Figure | mpl.axes.Axes:
        """Plot AOD peaks against temperature peaks."""
        aod_hl = self.data.aod[-1]
        trefht_hl = self.data.temp[-1]
        temp_m20 = self.data.temp_m20[np.argsort(self.data.aod_m20)]
        aod_m20 = self.data.aod_m20[np.argsort(self.data.aod_m20)]
        ax_ = (fig5_e := plt.figure()).gca() if ax is None else ax
        ax_.plot(self.data.aod[:-1], self.data.temp[:-1], **core.config.LEGENDS["c2w"])
        ax_.scatter(aod_hl, trefht_hl, **core.config.LEGENDS["c2wn"])
        self._plot_aod_temp_data(ax_, aod_m20, temp_m20)
        ax_.scatter(
            self.data.aod_j05, self.data.temp_j05, **core.config.LEGENDS["P100"]
        )
        ax_.scatter(self.data.aod_t10, self.data.temp_t10, **core.config.LEGENDS["t10"])
        if os.environ["AOD"] == "exp":
            ax_1 = core.utils.misc.create_axes_inset(
                ax_, (0, 0.65, 0, 1.2), (0.45, 0.52, 0.4, 0.4), "lr->lr", "ul->ul"
            )
        else:
            ax_1 = core.utils.misc.create_axes_inset(
                ax_, (0, 1, 0, 1.2), (0.57, 0.12, 0.4, 0.4), "lr->lr", "ul->ul"
            )
        ax_1.plot(self.data.aod, self.data.temp, **core.config.LEGENDS["c2w"])
        self._plot_aod_temp_data(ax_1, aod_m20, temp_m20)
        ax_1.patch.set_alpha(0.8)
        ax_.set_xlabel("AOD [1]")
        ax_.set_ylabel("GMST [K]")
        if ax is None:
            kwargs = {
                "loc": "upper left",
                "framealpha": 0.8,
                "edgecolor": "gray",
                "fontsize": core.config.FONTSIZE,
                "ncol": 2,
                "labelspacing": 0.3,
                "handletextpad": 0.2,
                "columnspacing": 0.3,
            }
            ax_.legend(**kwargs)
        return fig5_e if ax is None else ax_

    def _plot_aod_temp_data(self, ax, aod_m20, temp_m20):
        ax.scatter(aod_m20, temp_m20, **core.config.LEGENDS["m20*"])
        ax.plot(self.data.aod_b20, self.data.temp_b20, **core.config.LEGENDS["b20"])
        ax.plot(self.data.aod_m14, self.data.temp_m14, **core.config.LEGENDS["m14"])
        ax.plot(
            self.data.aod_osi20, self.data.temp_osi20, **core.config.LEGENDS["osi20"]
        )
        ax.scatter(
            self.data.aod_pinatubo, self.data.temp_pinatubo, **core.config.LEGENDS["P"]
        )
        ax.scatter(
            self.data.aod_tambora, self.data.temp_tambora, **core.config.LEGENDS["VT"]
        )

    @overload
    def plot_rf_vs_temp(self, ax: mpl.axes.Axes) -> mpl.axes.Axes: ...
    @overload
    def plot_rf_vs_temp(self) -> mpl.figure.Figure: ...
    def plot_rf_vs_temp(
        self, ax: mpl.axes.Axes | None = None
    ) -> mpl.figure.Figure | mpl.axes.Axes:
        """Plot RF peaks against temperature peaks."""
        rf_hl, trefht_hl = self.data.rf[-1], self.data.temp[-1]
        rf_hl_coup = self.data.rf_coupled[-1]
        temp_lme = self.data.temp_ob16[np.argsort(self.data.rf_ob16)]
        rf_lme = self.data.rf_ob16[np.argsort(self.data.rf_ob16)]
        temp_m20 = self.data.temp_m20[np.argsort(self.data.rf_m20)]
        rf_m20 = self.data.rf_m20[np.argsort(self.data.rf_m20)]
        ax_ = (fig5_f := plt.figure()).gca() if ax is None else ax
        ax_.axvline(x=65, c="grey", linewidth=0.5)
        ax_.text(65, 2, r"$65\,\mathrm{W/m^{2}}$", ha="right")
        ax_.axhline(y=10, c="grey", linewidth=0.5)
        ax_.text(40, 10, r"$10\,\mathrm{K}$", va="bottom")
        self._plot_rf_temp_data(
            ax_,
            (rf_hl, trefht_hl),
            (rf_hl_coup, trefht_hl),
            (rf_lme, temp_lme),
            (rf_m20, temp_m20),
        )
        ax1 = core.utils.misc.create_axes_inset(
            ax_, (-1.2, 19, -0.4, 1.5), (0.1, 0.55, 0.35, 0.4), "lr->lr", "ul->ul"
        )
        self._plot_rf_temp_data(
            ax1,
            (rf_hl, trefht_hl),
            (rf_hl_coup, trefht_hl),
            (rf_lme, temp_lme),
            (rf_m20, temp_m20),
        )
        # ax1.set_yticks([0, 1])
        ax1.patch.set_alpha(0.8)
        ax_.set_xlabel("ERF $[\\mathrm{W/m^2}]$")
        ax_.set_ylabel("GMST [K]")
        if ax is None:
            kwargs = {
                "loc": "upper left",
                "framealpha": 0.8,
                "edgecolor": "gray",
                "fontsize": core.config.FONTSIZE,
                "ncol": 2,
                "labelspacing": 0.3,
                "handletextpad": 0.2,
                "columnspacing": 0.3,
            }
            ax_.legend(**kwargs)
        return fig5_f if ax is None else ax_

    def _plot_rf_temp_data(self, ax, hl, hl_coup, lme, m20):
        c2w_leg = core.config.LEGENDS["c2w"].copy()
        c2w_leg["ls"] = "--"
        c2w_leg["marker"] = core.config.POINTS_DICTS["triangle_right"]
        c2w_leg["label"] = "STrop$^{a}$"
        thl_leg = core.config.LEGENDS["c2wn"].copy()
        thl_leg.pop("marker")
        thl_leg["marker"] = core.config.POINTS_DICTS["tri_right"]
        thl_leg["label"] = "S1629N$^{a}$"
        rf_hl, trefht_hl = hl
        rf_hl_coup, _ = hl_coup
        rf_lme, temp_lme = lme
        rf_m20, temp_m20 = m20
        # ax.scatter(rf_m20, temp_m20, **core.config.LEGENDS["m20*"])
        # ax.plot(self.data.rf_b20, self.data.temp_b20, **core.config.LEGENDS["b20"])
        # ax.plot(
        #     self.data.rf_osi20, self.data.temp_osi20, **core.config.LEGENDS["osi20"]
        # )
        # ax.scatter(
        #     self.data.rf_pinatubo, self.data.temp_pinatubo, **core.config.LEGENDS["P"]
        # )
        # ax.scatter(
        #     self.data.rf_tambora, self.data.temp_tambora, **core.config.LEGENDS["VT"]
        # )
        # --
        ax.plot(self.data.rf[:-1], self.data.temp[:-1], **core.config.LEGENDS["c2w"])
        ax.plot(self.data.rf_coupled[:-1], self.data.temp[:-1], **c2w_leg)
        # ax.plot(self.data.rf_r09, self.data.temp_r09, **core.config.LEGENDS["r09"])
        ax.scatter(rf_hl, trefht_hl, **core.config.LEGENDS["c2wn"])
        ax.scatter(rf_hl_coup, trefht_hl, **thl_leg)
        ax.scatter(rf_lme, temp_lme, **core.config.LEGENDS["ob16"])
        ax.scatter(rf_m20, temp_m20, **core.config.LEGENDS["m20*"])
        ax.plot(self.data.rf_b20, self.data.temp_b20, **core.config.LEGENDS["b20"])
        ax.plot(
            self.data.rf_mcg24, self.data.temp_mcg24, **core.config.LEGENDS["mcg24"]
        )
        ax.plot(self.data.rf_m14, self.data.temp_m14, **core.config.LEGENDS["m14"])
        ax.scatter(
            self.data.rf_pinatubo, self.data.temp_pinatubo, **core.config.LEGENDS["P"]
        )
        ax.scatter(
            self.data.rf_tambora, self.data.temp_tambora, **core.config.LEGENDS["VT"]
        )
        ax.scatter(self.data.rf_j05, self.data.temp_j05, **core.config.LEGENDS["P100"])
        ax.scatter(self.data.rf_t10, self.data.temp_t10, **core.config.LEGENDS["t10"])

    def compute_parsonr(self) -> None:
        """Compute the Pearson coefficient across the data."""
        # Compute Pearson stats
        all_so2 = [
            "so2",
            "b20",
            "e13",
            "j05",
            "m14",
            # "m20",
            "mcg24",
            "osi20",
            "pinatubo",
            "r09",
            "t10",
            "tambora",
            # "ob16",
        ]
        all_aod = [
            "aod",
            "b20",
            "e13",
            "j05",
            "m14",
            # "m20",
            "osi20",
            "pinatubo",
            "t10",
            "tambora",
        ]
        all_rf = [
            "rf",
            "b20",
            "j05",
            "m14",
            # "m20",
            "mcg24",
            "pinatubo",
            "t10",
            "tambora",
            # "ob16",
        ]
        all_temp = [
            "temp",
            "b20",
            "j05",
            "m14",
            "mcg24",
            "osi20",
            "pinatubo",
            "r09",
            "t10",
            "tambora",
            # "ob16",
        ]
        for p1, p2 in [
            (all_so2, all_aod),
            (all_so2, all_rf),
            (all_so2, all_temp),
            (all_aod, all_rf),
            (all_aod, all_temp),
            (all_rf, all_temp),
        ]:
            stat_x = np.asarray(getattr(self.data, p1[0]))
            stat_y = np.asarray(getattr(self.data, p2[0]))
            for p in p1[1:]:
                if p in p2:
                    stat_x = np.concatenate(
                        (stat_x, np.atleast_1d(getattr(self.data, f"{p1[0]}_{p}")))
                    )
                    stat_y = np.concatenate(
                        (stat_y, np.atleast_1d(getattr(self.data, f"{p2[0]}_{p}")))
                    )
            print(f"Pearson stat for {p1[0]} and {p2[0]}")
            print(scipy.stats.pearsonr(stat_x, stat_y))


def main(show_output: bool = False):
    """Run the main program."""
    save = True
    fig, axs = plastik.figure_grid(
        rows=3, columns=2, using={"expand_top": 1.08, "adjust_ylabel": 0.01 - 0.15}
    )
    plotter = DoPlotting(show_output)
    plotter.compute_parsonr()
    plotter.plot_so2_vs_aod(axs[0])
    plotter.plot_so2_vs_rf(axs[1])
    plotter.plot_so2_vs_temp(axs[2])
    plotter.plot_aod_vs_rf(axs[3])
    plotter.plot_aod_vs_temperature(axs[4])
    plotter.plot_rf_vs_temp(axs[5])
    unique_labels: dict[str, mpl.lines.Line2D] = {}
    for ax in fig.axes:
        line, label = ax.get_legend_handles_labels()
        for i, lab in enumerate(label):
            if lab not in unique_labels:
                unique_labels[lab] = line[i]
    # Reorder
    order = [
        # 1
        "STrop",
        "S1629N",
        r"$\propto\mathrm{SO_2}^{2/3}$",
        # 2
        "STrop$^{a}$",
        "S1629N$^{a}$",
        "T10$^{a}$",
        # 3
        "B20$^{a}$",
        "OB16",
        "M14$^{a}$",
        # 4
        "E13",
        "M20",
        "J05",
        # 5
        "McG24$^{a}$",
        "Os20",
        "R09",
        # 6
        "T",
        "P",
    ]
    for o in order:
        if o in unique_labels:
            tmp = unique_labels.pop(o)
            unique_labels[o] = tmp
    fig.legend(
        handles=list(unique_labels.values()),
        labels=list(unique_labels.keys()),
        ncols=6,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.005),
        frameon=False,
    )
    if save:
        SAVE_PATH = core.utils.if_save.create_savedir()
        fig.savefig(SAVE_PATH / "figure4")
        if (fig4 := (SAVE_PATH / "figure4.pdf")).exists():
            print(f"Successfully saved figure 4 to {fig4.resolve()}")
    if show_output:
        plt.show()
    else:
        plt.close("all")


if __name__ == "__main__":
    main(show_output=True)
