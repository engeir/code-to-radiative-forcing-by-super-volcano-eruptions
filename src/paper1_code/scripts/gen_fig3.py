"""Script that generates plots for figure 4."""

import pathlib
import tempfile
import warnings

import cosmoplots
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy

import paper1_code as core


class SetupNeededData:
    """Class that loads all data used in the plotting procedures."""

    def __init__(self):
        self.text, self.aod, self.rf = core.load.cesm2.get_c2w_aod_rf(freq="ses")
        self.time_m20, self.aod_m20, self.rf_m20 = core.load.m20.get_m20()


class DoPlotting:
    """Class that takes care of all the plotting."""

    def __init__(self, print_summary: bool):
        self.print_summary = print_summary
        self.data = SetupNeededData()
        self.period1 = (0, 1.1)
        self.period2 = (1.1, 3)

    def _plot_ratio(
        self,
        aod: list[np.ndarray],
        rf: list[np.ndarray],
        aod_m20: np.ndarray | None = None,
        rf_m20: np.ndarray | None = None,
        **kwargs,
    ) -> mpl.figure.Figure:
        l_c2wm = core.config.LEGENDS["c2wm"]
        l_c2wmp = core.config.LEGENDS["c2wmp"]
        l_c2ws = core.config.LEGENDS["c2ws"]
        l_c2wn = core.config.LEGENDS["c2wn"]
        year_zero = 0
        fig = plt.figure()
        ax = fig.gca()
        ax.set_xlim((-0.0, 3.7))
        for i, ell in enumerate([l_c2wn, l_c2ws, l_c2wmp, l_c2wm], start=-3):
            ratio_s = rf[abs(i)] / aod[abs(i)]
            x = np.asarray([float(t) - year_zero for t in self.data.text[abs(i)]])
            # Full
            year_mask = (x > self.period1[0]) & (x < self.period2[1])
            x = x[year_mask]
            ratio_s = ratio_s[year_mask]
            ax.scatter(x, ratio_s, **ell)
            # Rise (steep, AOD rises faster than RF)
            # Recovery (flat, AOD and RF linearly dependent)
            year_masks = [
                (x > self.period1[0]) & (x < self.period1[1]),
                (x > self.period2[0]) & (x < self.period2[1]),
            ]
            for ym in year_masks:
                x_means = np.unique(x[ym])
                y_means_ = [
                    ratio_s[ym][np.argwhere(x[ym] == x_means[i])].mean()
                    for i in range(len(x_means))
                ]
                y_means = np.array(y_means_)
                y_std_ = [
                    ratio_s[ym][np.argwhere(x[ym] == x_means[i])].std()
                    for i in range(len(x_means))
                ]
                y_std = np.array(y_std_)
                result = scipy.stats.linregress(x[ym], ratio_s[ym])
                rs = result.slope
                rse = result.stderr
                ri = result.intercept
                y = x_means * rs + ri
                # Error bars
                if "xlabel" not in kwargs:
                    ax.plot(x_means, y, c=ell["c"], label="_Hidde", alpha=0.5)
                if self.print_summary:
                    print(rf"Slope: \({rs:.2f}\pm{rse:.2f}\)", end="\t")
                ax.fill_between(
                    x_means, y_means - y_std, y_means + y_std, alpha=0.3, color=ell["c"]
                )
            if self.print_summary:
                print("")
        if aod_m20 is not None and rf_m20 is not None:
            self._m20_plots(rf_m20, aod_m20, ax)
        xlabel = kwargs.pop("xlabel", "Time after eruption $[\\mathrm{year}]$")
        ylabel = kwargs.pop(
            "ylabel",
            "Radiative forcing / \nAerosol optical depth $[\\mathrm{W/m^2}]$",
        )
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        kwargs = {
            "loc": "lower right",
            "bbox_to_anchor": (0.51, -0.02, 0.5, 0.3),
            "framealpha": 0.8,
            "edgecolor": "gray",
            "fontsize": core.config.FONTSIZE,
        }
        ax.legend(**kwargs)
        return fig

    def _m20_plots(self, rf_m20, aod_m20, ax):
        mell = core.config.LEGENDS["m20"]
        warnings.simplefilter("ignore")
        # Dividing by zero is fine...
        ratio_nonan = rf_m20.flatten() / aod_m20.flatten()
        warnings.resetwarnings()
        idx = np.argwhere(~np.isnan(ratio_nonan))
        ratio_nonan = ratio_nonan[idx].flatten()
        time_nonan = (self.data.time_m20.flatten() - self.data.time_m20.flatten()[0])[
            idx
        ].flatten()
        ax.scatter(
            time_nonan[time_nonan < self.period2[1]],
            ratio_nonan[time_nonan < self.period2[1]],
            **mell,
        )
        for low, high in [(0.0, 1.1), (1.1, 3.0)]:
            mask = (time_nonan > low) & (time_nonan < high)
            result = scipy.stats.linregress(
                time_nonan[mask],
                ratio_nonan[mask],
            )
            rs = result.slope
            ri = result.intercept
            if self.print_summary:
                print(f"Mean ratio: {ratio_nonan[mask].mean()}")
                print(f"Slope: {rs}")
            x = time_nonan[mask]
            y = x * rs + ri
            warnings.simplefilter("ignore")
            # Dividing by zero is fine...
            y_means = (rf_m20 / aod_m20).mean(axis=0)
            y_std = (rf_m20 / aod_m20).std(axis=0)
            warnings.resetwarnings()
            ax.plot(x, y, c=mell["c"])
            t_fill = self.data.time_m20[0, :] - self.data.time_m20.flatten()[0]
            mask2 = (t_fill > low) & (t_fill < high)
            ax.fill_between(
                t_fill[mask2],
                (y_means - y_std)[mask2],
                (y_means + y_std)[mask2],
                alpha=0.3,
                color=mell["c"],
            )

    def plot_ratio(self, with_m20_data: bool = False) -> mpl.figure.Figure:
        """Plot ratio between AOD and RF during the first three years of the eruption."""
        return self._plot_ratio(
            self.data.aod,
            self.data.rf,
            self.data.aod_m20 if with_m20_data else None,
            self.data.rf_m20 if with_m20_data else None,
        )

    def plot_ratio_scaled(self, with_m20_data: bool = False) -> mpl.figure.Figure:
        """Plot ratio between scaled AOD and RF during the first three years of the eruption."""
        aod, rf = core.utils.time_series.normalize_peaks(
            (self.data.aod, "aod"), (self.data.rf, "rf")
        )
        if with_m20_data:
            aod_m20_, rf_m20_ = core.utils.time_series.normalize_peaks(
                (self.data.aod_m20, "aod"), (self.data.rf_m20, "rf")
            )
            aod_m20 = np.asarray(aod_m20_)
            rf_m20 = np.asarray(rf_m20_)
        else:
            aod_m20, rf_m20 = None, None
        xlabel = "Time after eruption $[\\mathrm{year}]$"
        ylabel = (
            "Normalized radiative forcing / \nNormalized aerosol optical depth $[1]$"
        )
        return self._plot_ratio(
            aod,
            rf,
            aod_m20,
            rf_m20,
            xlabel=xlabel,
            ylabel=ylabel,
        )


def main(show_output: bool = False):
    """Run the main program."""
    TMP = tempfile.TemporaryDirectory()
    tmp_dir = pathlib.Path(TMP.name)
    save = True
    plotter = DoPlotting(show_output)
    ratio = plotter.plot_ratio(with_m20_data=True)
    scaled = plotter.plot_ratio_scaled(with_m20_data=True)
    if save:
        SAVE_PATH = core.utils.if_save.create_savedir()
        ratio.savefig(tmp_dir / "aod_vs_rf_avg_loop_ratio.png")
        scaled.savefig(tmp_dir / "aod_vs_rf_avg_loop_ratio_scaled.png")
        cosmoplots.combine(
            tmp_dir / "aod_vs_rf_avg_loop_ratio.png",
            tmp_dir / "aod_vs_rf_avg_loop_ratio_scaled.png",
        ).using(fontsize=50, gravity="southwest", pos=(10, 30)).in_grid(1, 2).save(
            SAVE_PATH / "figure3.png"
        )
        if (fig3 := (SAVE_PATH / "figure3.png")).exists():
            print(f"Successfully saved figure 3 to {fig3.resolve()}")
    if show_output:
        plt.show()
    else:
        plt.close("all")
    TMP.cleanup()


if __name__ == "__main__":
    main(show_output=True)
