"""Script that generates plots for figure 5."""

import pathlib
import tempfile
import warnings

import cosmoplots
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import paper1_code as core


class SetupNeededData:
    """Class that loads all data used in the plotting procedures."""

    def __init__(self):
        # C2W
        self.so2 = core.load.cesm2.get_so2_c2w_peaks()
        self.aod = core.load.cesm2.get_aod_c2w_peaks()
        self.rf = core.load.cesm2.get_rf_c2w_peaks()
        self.temp = core.load.cesm2.get_trefht_c2w_peaks()
        # Marshall et al. 2020
        self.so2_m20, self.aod_m20, self.rf_m20, self.temp_m20 = core.load.m20.get_m20(
            find_all_peaks=True
        )
        # Otto-Bliesner et al. 2016
        self.so2_ob16, self.rf_ob16, self.temp_ob16 = core.load.ob16.get_ob16()
        # Mt. Tambora
        self.so2_tambora = core.load.tambora.get_so2_tambora()
        self.aod_tambora = core.load.tambora.get_aod_tambora()
        self.rf_tambora = core.load.tambora.get_rf_tambora()
        self.temp_tambora = core.load.tambora.get_trefht_tambora()
        # Jones et al. 2005
        self.so2_j05, self.aod_j05, self.rf_j05, self.temp_j05 = (
            core.load.j05.get_so2_j05(),
            core.load.j05.get_aod_j05(),
            core.load.j05.get_rf_j05(),
            core.load.j05.get_trefht_j05(),
        )
        # Timmreck et al. 2010
        self.so2_t10, self.aod_t10, self.rf_t10, self.temp_t10 = (
            core.load.t10.get_so2_t10(),
            core.load.t10.get_aod_t10(),
            core.load.t10.get_rf_t10(),
            core.load.t10.get_trefht_t10(),
        )
        # Mt. Pinatubo
        self.so2_pinatubo, self.aod_pinatubo, self.rf_pinatubo, self.temp_pinatubo = (
            core.load.pinatubo.get_so2_pinatubo(),
            core.load.pinatubo.get_aod_pinatubo(),
            core.load.pinatubo.get_rf_pinatubo(),
            core.load.pinatubo.get_trefht_pinatubo(),
        )


class DoPlotting:
    """Class that takes care of all the plotting."""

    def __init__(self, print_summary: bool):
        self.print_summary = print_summary
        self.data = SetupNeededData()

    def plot_so2_vs_aod(self) -> mpl.figure.Figure:
        """Plot SO2 against AOD peaks."""
        ihl = self.data.so2[-1]
        ahl = self.data.aod[-1]
        fig5_a = plt.figure()
        ax = fig5_a.gca()
        plt.plot(self.data.so2[:-1], self.data.aod[:-1], **core.config.LEGENDS["c2w"])
        plt.scatter(ihl, ahl, **core.config.LEGENDS["c2wn"])
        plt.scatter(self.data.so2_m20, self.data.aod_m20, **core.config.LEGENDS["m20*"])
        plt.scatter(
            self.data.so2_pinatubo, self.data.aod_pinatubo, **core.config.LEGENDS["P"]
        )
        plt.scatter(
            self.data.so2_tambora, self.data.aod_tambora, **core.config.LEGENDS["VT"]
        )
        plt.scatter(self.data.so2_j05, self.data.aod_j05, **core.config.LEGENDS["P100"])
        plt.scatter(self.data.so2_t10, self.data.aod_t10, **core.config.LEGENDS["t10"])
        x0, y0, width, height = 0.62, 0.1, 0.35, 0.4
        ax1 = ax.inset_axes((x0, y0, width, height))
        ax1.plot(self.data.so2[:-1], self.data.aod[:-1], **core.config.LEGENDS["c2w"])
        ax1.scatter(
            self.data.so2_pinatubo, self.data.aod_pinatubo, **core.config.LEGENDS["P"]
        )
        ax1.scatter(
            self.data.so2_tambora, self.data.aod_tambora, **core.config.LEGENDS["VT"]
        )
        ax1.scatter(self.data.so2_m20, self.data.aod_m20, **core.config.LEGENDS["m20*"])
        ax1.set_xlim((0, 110))
        ax1.set_ylim((0.05, 0.9))
        ax1.patch.set_alpha(0.3)
        ax.indicate_inset_zoom(ax1)
        ax.set_xlim((-150, 3500))
        plt.xlabel("Injected SO2 [Tg]")
        plt.ylabel("Aerosol optical depth [1]")
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
        ax.legend(**kwargs)
        return fig5_a

    def plot_so2_vs_rf(self) -> mpl.figure.Figure:
        """Plot SO2 against RF peaks."""
        ytt_leg = core.config.LEGENDS["P100"].copy()
        ytt_leg.pop("marker")
        ytt_leg.pop("label")
        ihl = self.data.so2[-1]
        thl = self.data.rf[-1]
        fig5_b = plt.figure()
        # Fit from Niemeier and Timreck (2015) (they use S, and not SO2, which has half
        # the mass)
        s = np.linspace(0, 3000 // 2, 10000)
        warnings.simplefilter("ignore")
        # Dividing by zero is fine...
        rf = 65 * np.exp(-((2246 / s) ** (0.23)))
        warnings.resetwarnings()
        plt.plot(self.data.so2[:-1], self.data.rf[:-1], **core.config.LEGENDS["c2w"])
        plt.scatter(ihl, thl, **core.config.LEGENDS["c2wn"])
        plt.scatter(
            self.data.so2_ob16, self.data.rf_ob16, **core.config.LEGENDS["ob16"]
        )
        plt.scatter(self.data.so2_m20, self.data.rf_m20, **core.config.LEGENDS["m20*"])
        plt.scatter(
            self.data.so2_pinatubo, self.data.rf_pinatubo, **core.config.LEGENDS["P"]
        )
        plt.scatter(
            self.data.so2_tambora, self.data.rf_tambora, **core.config.LEGENDS["VT"]
        )
        plt.scatter(self.data.so2_j05, self.data.rf_j05, **core.config.LEGENDS["P100"])
        plt.scatter(self.data.so2_t10, self.data.rf_t10, **core.config.LEGENDS["t10"])
        plt.plot(s * 2, rf, "--", label="N15", c=ytt_leg["c"])
        # Inset
        x0, y0, width, height = 0.62, 0.1, 0.35, 0.4
        ax = plt.gca()
        ax1 = ax.inset_axes((x0, y0, width, height))
        ax1.plot(self.data.so2[:-1], self.data.rf[:-1], **core.config.LEGENDS["c2w"])
        ax1.scatter(ihl, thl, **core.config.LEGENDS["c2wn"])
        ax1.scatter(
            self.data.so2_ob16, self.data.rf_ob16, **core.config.LEGENDS["ob16"]
        )
        ax1.scatter(self.data.so2_m20, self.data.rf_m20, **core.config.LEGENDS["m20*"])
        ax1.scatter(
            self.data.so2_pinatubo, self.data.rf_pinatubo, **core.config.LEGENDS["P"]
        )
        ax1.scatter(
            self.data.so2_tambora, self.data.rf_tambora, **core.config.LEGENDS["VT"]
        )
        ax1.scatter(self.data.so2_j05, self.data.rf_j05, **core.config.LEGENDS["P100"])
        ax1.scatter(self.data.so2_t10, self.data.rf_t10, **core.config.LEGENDS["t10"])
        ax1.plot(s * 2, rf, "--", label="N15", c=ytt_leg["c"])
        ax1.set_xlim((0, 190))
        ax1.set_ylim((0, 28))
        ax1.patch.set_alpha(0.8)
        ax.indicate_inset_zoom(ax1)
        ax.set_xlim((-150, 3500))
        plt.xlabel("Injected SO2 [Tg]")
        plt.ylabel("Radiative forcing $[\\mathrm{W/m^2}]$")
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
        ax.legend(**kwargs)
        return fig5_b

    def plot_so2_vs_temp(self) -> mpl.figure.Figure:
        """Plot SO2 against temperature peaks."""
        c2wsn_temp = self.data.temp[-1]
        fig5_c = plt.figure()
        ax = fig5_c.gca()
        plt.plot(self.data.so2[:-1], self.data.temp[:-1], **core.config.LEGENDS["c2w"])
        plt.scatter(self.data.so2[-1], c2wsn_temp, **core.config.LEGENDS["c2wn"])
        self._plot_so2_temp_common_data(ax)
        plt.scatter(
            self.data.so2_j05, self.data.temp_j05, **core.config.LEGENDS["P100"]
        )
        plt.scatter(self.data.so2_t10, self.data.temp_t10, **core.config.LEGENDS["t10"])
        x0, y0, width, height = 0.62, 0.1, 0.35, 0.4
        ax1 = ax.inset_axes((x0, y0, width, height))
        ax1.plot(self.data.so2[:-1], self.data.temp[:-1], **core.config.LEGENDS["c2w"])
        self._plot_so2_temp_common_data(ax1)
        ax1.set_xlim((0, 190))
        ax1.set_ylim((0, 1.5))
        ax1.patch.set_alpha(0.3)
        ax.indicate_inset_zoom(ax1)
        ax.set_xlim((-150, 3500))
        plt.xlabel("Injected SO2 [Tg]")
        plt.ylabel("Temperature anomaly [K]")
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
        ax.legend(**kwargs)
        return fig5_c

    def _plot_so2_temp_common_data(self, ax):
        ax.scatter(
            self.data.so2_ob16, self.data.temp_ob16, **core.config.LEGENDS["ob16"]
        )
        ax.scatter(self.data.so2_m20, self.data.temp_m20, **core.config.LEGENDS["m20*"])
        ax.scatter(
            self.data.so2_pinatubo, self.data.temp_pinatubo, **core.config.LEGENDS["P"]
        )
        ax.scatter(
            self.data.so2_tambora, self.data.temp_tambora, **core.config.LEGENDS["VT"]
        )

    def plot_aod_vs_rf(self) -> mpl.figure.Figure:
        """Plot AOD peaks against RF peaks."""
        aod_hl = self.data.aod[-1]
        rf_hl = self.data.rf[-1]
        rf_m20 = self.data.rf_m20[np.argsort(self.data.aod_m20)]
        aod_m20 = self.data.aod_m20[np.argsort(self.data.aod_m20)]
        fig5_d = plt.figure()
        plt.plot(self.data.aod[:-1], self.data.rf[:-1], **core.config.LEGENDS["c2w"])
        plt.scatter(aod_hl, rf_hl, **core.config.LEGENDS["c2wn"])
        plt.scatter(
            self.data.aod_pinatubo, self.data.rf_pinatubo, **core.config.LEGENDS["P"]
        )
        plt.scatter(
            self.data.aod_tambora, self.data.rf_tambora, **core.config.LEGENDS["VT"]
        )
        plt.scatter(self.data.aod_j05, self.data.rf_j05, **core.config.LEGENDS["P100"])
        plt.scatter(self.data.aod_t10, self.data.rf_t10, **core.config.LEGENDS["t10"])
        plt.scatter(aod_m20, rf_m20, **core.config.LEGENDS["m20*"])
        x0, y0, width, height = 0.57, 0.12, 0.4, 0.4
        ax = plt.gca()
        ax1 = ax.inset_axes((x0, y0, width, height))
        # x_aod = np.linspace(0, 15, 100)
        # ax.plot(x_aod, 15 * x_aod**0.5)
        # ax.plot(x_aod, 22 * np.log(x_aod + 1))
        ax1.plot(self.data.aod, self.data.rf, **core.config.LEGENDS["c2w"])
        ax1.scatter(aod_hl, rf_hl, **core.config.LEGENDS["c2wn"])
        ax1.scatter(
            self.data.aod_pinatubo, self.data.rf_pinatubo, **core.config.LEGENDS["P"]
        )
        ax1.scatter(
            self.data.aod_tambora, self.data.rf_tambora, **core.config.LEGENDS["VT"]
        )
        ax1.scatter(self.data.aod_j05, self.data.rf_j05, **core.config.LEGENDS["P100"])
        ax1.scatter(self.data.aod_t10, self.data.rf_t10, **core.config.LEGENDS["t10"])
        ax1.scatter(aod_m20, rf_m20, **core.config.LEGENDS["m20*"])
        ax1.set_xlim((0, 1))
        ax1.set_ylim((0, 19))
        ax1.patch.set_alpha(0.3)
        ax.indicate_inset_zoom(ax1)
        plt.xlabel("Aerosol optical depth [1]")
        plt.ylabel("Radiative forcing $[\\mathrm{W/m^2}]$")
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
        ax.legend(**kwargs)
        return fig5_d

    def plot_aod_vs_temperature(self) -> mpl.figure.Figure:
        """Plot AOD peaks against temperature peaks."""
        aod_hl = self.data.aod[-1]
        trefht_hl = self.data.temp[-1]
        temp_m20 = self.data.temp_m20[np.argsort(self.data.aod_m20)]
        aod_m20 = self.data.aod_m20[np.argsort(self.data.aod_m20)]
        fig5_e = plt.figure()
        ax = fig5_e.gca()
        plt.plot(self.data.aod[:-1], self.data.temp[:-1], **core.config.LEGENDS["c2w"])
        plt.scatter(aod_hl, trefht_hl, **core.config.LEGENDS["c2wn"])
        plt.scatter(aod_m20, temp_m20, **core.config.LEGENDS["m20*"])
        plt.scatter(
            self.data.aod_pinatubo, self.data.temp_pinatubo, **core.config.LEGENDS["P"]
        )
        plt.scatter(
            self.data.aod_tambora, self.data.temp_tambora, **core.config.LEGENDS["VT"]
        )
        plt.scatter(
            self.data.aod_j05, self.data.temp_j05, **core.config.LEGENDS["P100"]
        )
        plt.scatter(self.data.aod_t10, self.data.temp_t10, **core.config.LEGENDS["t10"])
        x0, y0, width, height = 0.57, 0.12, 0.4, 0.4
        ax1 = ax.inset_axes((x0, y0, width, height))
        # x_aod = np.linspace(0, 15, 100)
        # ax.plot(x_aod, 2 * x_aod**0.5)
        # ax.plot(x_aod, 3 * np.log(x_aod + 1))
        ax1.plot(self.data.aod, self.data.temp, **core.config.LEGENDS["c2w"])
        ax1.scatter(aod_m20, temp_m20, **core.config.LEGENDS["m20*"])
        ax1.scatter(
            self.data.aod_pinatubo, self.data.temp_pinatubo, **core.config.LEGENDS["P"]
        )
        ax1.scatter(
            self.data.aod_tambora, self.data.temp_tambora, **core.config.LEGENDS["VT"]
        )
        ax1.set_xlim((0, 1))
        ax1.set_ylim((0, 1.2))
        ax1.patch.set_alpha(0.3)
        ax.indicate_inset_zoom(ax1)
        plt.xlabel("Aerosol optical depth [1]")
        plt.ylabel("Temperature anomaly [K]")
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
        ax.legend(**kwargs)
        return fig5_e

    def plot_rf_vs_temp(self) -> mpl.figure.Figure:
        """Plot RF peaks against temperature peaks."""
        rf_hl, trefht_hl = self.data.rf[-1], self.data.temp[-1]
        temp_lme = self.data.temp_ob16[np.argsort(self.data.rf_ob16)]
        rf_lme = self.data.rf_ob16[np.argsort(self.data.rf_ob16)]
        temp_m20 = self.data.temp_m20[np.argsort(self.data.rf_m20)]
        rf_m20 = self.data.rf_m20[np.argsort(self.data.rf_m20)]
        fig5_f = plt.figure()
        ax = fig5_f.gca()
        plt.plot(self.data.rf[:-1], self.data.temp[:-1], **core.config.LEGENDS["c2w"])
        plt.scatter(rf_hl, trefht_hl, **core.config.LEGENDS["c2wn"])
        plt.scatter(rf_lme, temp_lme, **core.config.LEGENDS["ob16"])
        plt.scatter(rf_m20, temp_m20, **core.config.LEGENDS["m20*"])
        plt.scatter(
            self.data.rf_pinatubo, self.data.temp_pinatubo, **core.config.LEGENDS["P"]
        )
        plt.scatter(
            self.data.rf_tambora, self.data.temp_tambora, **core.config.LEGENDS["VT"]
        )
        ax.scatter(self.data.rf_j05, self.data.temp_j05, **core.config.LEGENDS["P100"])
        plt.scatter(self.data.rf_t10, self.data.temp_t10, **core.config.LEGENDS["t10"])
        plt.xlabel("Radiative forcing $[\\mathrm{W/m^2}]$")
        plt.ylabel("Temperature anomaly [K]")
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
        ax.legend(**kwargs)
        return fig5_f


def main(show_output: bool = False):
    """Run the main program."""
    TMP = tempfile.TemporaryDirectory()
    tmp_dir = pathlib.Path(TMP.name)
    save = True
    plotter = DoPlotting(show_output)
    so2_vs_aod = plotter.plot_so2_vs_aod()
    so2_vs_rf = plotter.plot_so2_vs_rf()
    so2_vs_temp = plotter.plot_so2_vs_temp()
    aod_vs_rf = plotter.plot_aod_vs_rf()
    aod_vs_temp = plotter.plot_aod_vs_temperature()
    rf_vs_temp = plotter.plot_rf_vs_temp()
    if save:
        SAVE_PATH = core.utils.if_save.create_savedir()
        so2_vs_aod.savefig(tmp_dir / "injection_vs_aod")
        so2_vs_rf.savefig(tmp_dir / "injection_vs_rf")
        so2_vs_temp.savefig(tmp_dir / "injection_vs_temperature")
        aod_vs_rf.savefig(tmp_dir / "aod_vs_rf")
        aod_vs_temp.savefig(tmp_dir / "aod_vs_temperature")
        rf_vs_temp.savefig(tmp_dir / "rf_vs_temperature")
        cosmoplots.combine(
            tmp_dir / "injection_vs_aod.png",
            tmp_dir / "injection_vs_rf.png",
            tmp_dir / "injection_vs_temperature.png",
            tmp_dir / "aod_vs_rf.png",
            tmp_dir / "aod_vs_temperature.png",
            tmp_dir / "rf_vs_temperature.png",
        ).using(fontsize=8).in_grid(w=2, h=3).save(SAVE_PATH / "figure4.png")
        if (fig4 := (SAVE_PATH / "figure4.png")).exists():
            print(f"Successfully saved figure 4 to {fig4.resolve()}")
    if show_output:
        plt.show()
    else:
        plt.close("all")
    TMP.cleanup()


if __name__ == "__main__":
    main(show_output=True)
