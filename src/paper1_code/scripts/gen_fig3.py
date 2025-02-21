"""Script that generates plots for figure 3."""

import warnings
from typing import overload

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import plastik
import scipy
from matplotlib import ticker

import paper1_code as core

convert_aod = core.utils.time_series.convert_aod


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

    @overload
    def _plot_ratio(
        self,
        aod: list[np.ndarray],
        rf: list[np.ndarray],
        aod_m20: np.ndarray | None,
        rf_m20: np.ndarray | None,
        ax: mpl.axes.Axes,
        **kwargs,
    ) -> mpl.axes.Axes: ...
    @overload
    def _plot_ratio(
        self,
        aod: list[np.ndarray],
        rf: list[np.ndarray],
        aod_m20: np.ndarray | None,
        rf_m20: np.ndarray | None,
        **kwargs,
    ) -> mpl.figure.Figure: ...
    def _plot_ratio(
        self,
        aod: list[np.ndarray],
        rf: list[np.ndarray],
        aod_m20: np.ndarray | None = None,
        rf_m20: np.ndarray | None = None,
        ax: mpl.axes.Axes | None = None,
        **kwargs,
    ) -> mpl.figure.Figure | mpl.axes.Axes:
        if self.print_summary:
            print(
                f"Using {len(self.data.time_m20)} out of 82 eruptions from the M20 dataset."
            )
        l_c2wm = core.config.LEGENDS["c2wm"]
        l_c2wmp = core.config.LEGENDS["c2wmp"]
        l_c2ws = core.config.LEGENDS["c2ws"]
        l_c2wn = core.config.LEGENDS["c2wn"]
        l_c2wss = core.config.LEGENDS["c2wss"]
        year_zero = 0
        ax_ = (fig := plt.figure()).gca() if ax is None else ax
        ax_.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
        ax_.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
        ax_.set_xlim((-0.0, 3.0))
        for i, ell in enumerate([l_c2wss, l_c2wn, l_c2ws, l_c2wmp, l_c2wm], start=-4):
            if i == -2:  # noqa: PLR2004
                continue
            ratio_s = rf[abs(i)] / convert_aod(aod[abs(i)])
            x = np.asarray([float(t) - year_zero for t in self.data.text[abs(i)]])
            # Full
            year_mask = (x > self.period1[0]) & (x < self.period2[1])
            x = x[year_mask]
            ratio_s = ratio_s[year_mask]
            # Remove "zorder" from dictionary ell
            ell_ = ell.copy()
            ell_.pop("zorder")
            year_masks = [
                (x > self.period1[0]) & (x < self.period1[1]),
                (x > self.period2[0]) & (x < self.period2[1]),
            ]
            label_regression_lines = True
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
                label = ell["label"] if label_regression_lines else "_Hidden"
                ax_.plot(x_means, y, zorder=abs(i), c=ell["c"], label=label)
                label_regression_lines = False
                if self.print_summary:
                    print(rf"Slope: \({rs:.2f}\pm{rse:.2f}\)", end="\t")
                ax_.fill_between(
                    x_means,
                    y_means - y_std,
                    y_means + y_std,
                    alpha=0.3,
                    zorder=abs(i),
                    color=ell["c"],
                )
            if self.print_summary:
                print(f"{ell['label']}")
        if aod_m20 is not None and rf_m20 is not None:
            self._m20_plots(rf_m20, aod_m20, ax_, **kwargs)
        xlabel = kwargs.pop("xlabel", "Time after eruption $[\\mathrm{year}]$")
        ylabel = kwargs.pop(
            "ylabel",
            "$\\text{ERF}/\\text{SAOD}$ $[\\mathrm{W.m^{-2}}]$",
        )
        ax_.set_xlabel(xlabel)
        ax_.set_ylabel(ylabel)
        return fig if ax is None else ax_

    def _m20_plots(self, rf_m20, aod_m20, ax, **kwargs):
        mell = core.config.LEGENDS["m20"]
        mell_ = mell.copy()
        mell_.pop("zorder")
        warnings.simplefilter("ignore")
        # Dividing by zero is fine...
        ratio_nonan = rf_m20.flatten() / convert_aod(aod_m20.flatten())
        warnings.resetwarnings()
        idx = np.argwhere(~np.isnan(ratio_nonan))
        ratio_nonan = ratio_nonan[idx].flatten()
        time_nonan = (self.data.time_m20.flatten() - self.data.time_m20.flatten()[0])[
            idx
        ].flatten()
        label_regression_lines = True
        for low, high in [self.period1, self.period2]:
            mask = (time_nonan > low) & (time_nonan < high)
            result = scipy.stats.linregress(
                time_nonan[mask],
                ratio_nonan[mask],
            )
            rs = result.slope
            rse = result.stderr
            ri = result.intercept
            if self.print_summary:
                print(rf"Slope: \({rs:.2f}\pm{rse:.2f}\)", end="\t")
            x = time_nonan[mask]
            y = x * rs + ri
            warnings.simplefilter("ignore")
            # Dividing by zero is fine...
            y_means = (rf_m20 / convert_aod(aod_m20)).mean(axis=0)
            y_std = (rf_m20 / convert_aod(aod_m20)).std(axis=0)
            warnings.resetwarnings()
            if "xlabel" not in kwargs:
                ax.plot(x, y, zorder=2, c=mell["c"], label="_Hidde", alpha=0.5)
            label = mell["label"] if label_regression_lines else "_Hidden"
            ax.plot(x, y, zorder=2, c=mell["c"], label=label)
            label_regression_lines = False
            t_fill = self.data.time_m20[0, :] - self.data.time_m20.flatten()[0]
            mask2 = (t_fill > low) & (t_fill < high)
            ax.fill_between(
                t_fill[mask2],
                (y_means - y_std)[mask2],
                (y_means + y_std)[mask2],
                alpha=0.3,
                zorder=2,
                color=mell["c"],
            )
        if self.print_summary:
            print(f"{mell['label']}")

    @overload
    def plot_ratio(self, with_m20_data: bool, ax: mpl.axes.Axes) -> mpl.axes.Axes: ...
    @overload
    def plot_ratio(self, with_m20_data: bool) -> mpl.figure.Figure: ...
    def plot_ratio(
        self, with_m20_data: bool = False, ax: mpl.axes.Axes | None = None
    ) -> mpl.figure.Figure | mpl.axes.Axes:
        """Plot ratio between SAOD and RF during the first three years of the eruption."""
        return self._plot_ratio(
            self.data.aod,
            self.data.rf,
            self.data.aod_m20 if with_m20_data else None,
            self.data.rf_m20 if with_m20_data else None,
            ax=ax,
        )

    @overload
    def plot_ratio_scaled(
        self, with_m20_data: bool, ax: mpl.axes.Axes
    ) -> mpl.axes.Axes: ...
    @overload
    def plot_ratio_scaled(self, with_m20_data: bool) -> mpl.figure.Figure: ...
    def plot_ratio_scaled(
        self, with_m20_data: bool = False, ax: mpl.axes.Axes | None = None
    ) -> mpl.figure.Figure | mpl.axes.Axes:
        """Plot ratio between scaled SAOD and RF during the first three years of the eruption."""
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
        ylabel = "Normalized ERF / \nNormalized SAOD $[1]$"
        return self._plot_ratio(
            aod,
            rf,
            aod_m20,
            rf_m20,
            xlabel=xlabel,
            ylabel=ylabel,
            ax=ax,
        )


def main(show_output: bool = False):
    """Run the main program."""
    save = True
    fig, axs = plastik.figure_grid(
        rows=2, columns=1, using={"expand_top": 1.10, "share_axes": "x"}
    )
    plotter = DoPlotting(show_output)
    plotter.plot_ratio(with_m20_data=True, ax=axs[0])
    plotter.plot_ratio_scaled(with_m20_data=True, ax=axs[1])
    unique_labels: dict[str, mpl.lines.Line2D] = {}
    for ax in fig.axes:
        line, label = ax.get_legend_handles_labels()
        for i, lab in enumerate(label):
            if lab not in unique_labels:
                unique_labels[lab] = line[i]
    fig.legend(
        handles=list(unique_labels.values()),
        labels=list(unique_labels.keys()),
        ncols=3,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.005),
        frameon=False,
    )
    if save:
        SAVE_PATH = core.utils.if_save.create_savedir()
        fig.savefig(SAVE_PATH / "figure3")
        if (fig3 := (SAVE_PATH / "figure3.pdf")).exists():
            print(f"Successfully saved figure 3 to {fig3.resolve()}")
    if show_output:
        plt.show()
    else:
        plt.close("all")


if __name__ == "__main__":
    main(show_output=True)
