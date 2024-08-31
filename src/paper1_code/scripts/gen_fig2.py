"""Script that generates plots for figure 2."""

import os
from typing import overload

import labellines
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import plastik

import paper1_code as core

convert_aod = core.utils.time_series.convert_aod


class SetupNeededData:
    """Class that loads all data used in the plotting procedures."""

    def __init__(self):
        self.x_g16, self.aod_g16, self.rf_g16 = core.load.g16.get_gregory_paper_data()
        _, self.aod_c2w, self.rf_c2w = core.load.cesm2.get_c2w_aod_rf()
        self.aod_p, self.rf_p = (
            core.load.pinatubo.get_aod_pinatubo(),
            core.load.pinatubo.get_rf_pinatubo(),
        )
        self.aod_j05, self.rf_j05 = (
            core.load.j05.get_aod_j05(),
            core.load.j05.get_rf_j05(),
        )
        self.aod_t, self.rf_t = (
            core.load.tambora.get_aod_tambora(),
            core.load.tambora.get_rf_tambora(),
        )
        self.aod_c2w_peak, self.rf_c2w_peak = (
            core.load.cesm2.get_aod_c2w_peaks()[:5],
            core.load.cesm2.get_rf_c2w_peaks()[:5],
        )


class DoPlotting:
    """Class that takes care of all the plotting."""

    def __init__(self, print_summary: bool):
        self.print_summary = print_summary
        self.data = SetupNeededData()

    def plot_gregory_paper_gradient_lines(
        self, x, ax: mpl.axes.Axes, size: str
    ) -> None:
        """Create the gradient lines from the Gregory et al. (2016) paper."""
        col = core.config.LEGENDS["greg"]["c"]
        hadcm3_ca, ar5, hadcm3, hadgem2_amip = -26.6, -24.6, -19, -17
        (l1,) = ax.plot(x, x * (hadcm3_ca), "--", c=col, zorder=-1)
        (l2,) = ax.plot(x, x * (ar5), "--", c=col, zorder=-1)
        (l3,) = ax.plot(x, x * (hadcm3), c=col, zorder=-1)
        (l4,) = ax.plot(x, x * (hadgem2_amip), "--", c=col, zorder=-1)
        ll1 = 7 if size == "large" else 0.24
        ll2 = 7 if size == "large" else 0.28
        ll3 = 2.5 if size == "large" else 0.33
        ll4 = 7 if size == "large" else 0.32
        lablab = labellines.labelLine
        lablab(l1, ll1, outline_width=3, label=f"${hadcm3_ca}$", size=6)
        lablab(l2, ll2, outline_width=3, label=f"${ar5}$", size=6)
        lablab(l3, ll3, outline_width=3, label=f"${hadcm3}$", size=6)
        lablab(l4, ll4, outline_width=3, label=f"${hadgem2_amip}$", size=6)

    @overload
    def plot_aod_vs_rf_avg(
        self, ax1: mpl.axes.Axes, ax2: mpl.axes.Axes
    ) -> tuple[mpl.axes.Axes, mpl.axes.Axes]: ...
    @overload
    def plot_aod_vs_rf_avg(self) -> tuple[mpl.figure.Figure, mpl.figure.Figure]: ...
    def plot_aod_vs_rf_avg(
        self, ax1: mpl.axes.Axes | None = None, ax2: mpl.axes.Axes | None = None
    ) -> (
        tuple[mpl.figure.Figure, mpl.figure.Figure]
        | tuple[mpl.axes.Axes, mpl.axes.Axes]
    ):
        """Plot yearly mean RF against AOD."""
        ax1_ = (fig3_a := plt.figure()).gca() if ax1 is None else ax1
        ax2_ = (fig3_b := plt.figure()).gca() if ax2 is None else ax2
        for size, ax_ in zip(["large", "small"], [ax1_, ax2_], strict=True):
            self.plot_gregory_paper_gradient_lines(self.data.x_g16, ax_, size)
            plot = ax_.scatter
            plot(
                convert_aod(np.array(self.data.aod_c2w_peak)),
                np.array(self.data.rf_c2w_peak) * (-1),
                label="STrop Peaks*",
                c="none",
                ec="red",
                lw=1.5,
                s=15,
                zorder=4,
                **{
                    x: core.config.LEGENDS["c2w"][x]
                    for x in core.config.LEGENDS["c2w"]
                    if x not in ["c", "label", "marker", "ms", "zorder"]
                },
            )
            legend = {
                x: core.config.LEGENDS["VT"][x]
                for x in core.config.LEGENDS["VT"]
                if x not in "label"
            }
            plot(
                convert_aod(self.data.aod_t), -self.data.rf_t, label="T Peak*", **legend
            )
            plot(
                convert_aod(self.data.aod_c2w[2]),
                self.data.rf_c2w[2],
                **core.config.LEGENDS["c2ws"],
            )
            plot(
                convert_aod(self.data.aod_c2w[1]),
                self.data.rf_c2w[1],
                **core.config.LEGENDS["c2wmp"],
            )
            plot(
                convert_aod(self.data.aod_c2w[0]),
                self.data.rf_c2w[0],
                **core.config.LEGENDS["c2wm"],
            )
            legend = {
                x: core.config.LEGENDS["P100"][x]
                for x in core.config.LEGENDS["P100"]
                if x not in "label"
            }
            plot(
                convert_aod(self.data.aod_j05),
                -self.data.rf_j05,
                label="J05 Peak*",
                **legend,
            )
            plot([], [], label=" ", c="none")
            legend = {
                x: core.config.LEGENDS["P"][x]
                for x in core.config.LEGENDS["P"]
                if x not in "label"
            }
            plot(
                convert_aod(self.data.aod_p), -self.data.rf_p, label="P Peak*", **legend
            )
            plot(
                convert_aod(self.data.aod_c2w[4]),
                self.data.rf_c2w[4],
                **core.config.LEGENDS["c2wss"],
            )
            plot(
                convert_aod(self.data.aod_c2w[3]),
                self.data.rf_c2w[3],
                **core.config.LEGENDS["c2wn"],
            )
            plot(
                convert_aod(self.data.aod_g16),
                self.data.rf_g16,
                **core.config.LEGENDS["greg"],
            )
            if os.environ["AOD"] == "exp":
                xlim = (-0.1, 1.1) if size == "large" else (0, 0.15 * 8 / 3)
                ylim = (-70, 5) if size == "large" else (-3 * 8 / 3, 1 * 8 / 3)
            else:
                xlim = (-0.75, 18.75) if size == "large" else (0, 0.15 * 8 / 3)
                ylim = (-85, 5) if size == "large" else (-3 * 8 / 3, 1 * 8 / 3)
            ax_.set_xlim(xlim)
            ax_.set_ylim(ylim)
            ax_.set_xlabel("AOD [1]")
            ax_.set_ylabel("ERF $[\\mathrm{W/m^2}]$")
        return (fig3_a, fig3_b) if ax1 is None or ax2 is None else (ax1_, ax2_)


def main(show_output: bool = False):
    """Run the main program."""
    save = True
    plastik.FigureGrid().using()
    fig, axs = plastik.figure_grid(rows=2, columns=1, using={"expand_top": 1.15})
    plotter = DoPlotting(show_output)
    large, small = plotter.plot_aod_vs_rf_avg(axs[0], axs[1])
    unique_labels: dict[str, mpl.lines.Line2D] = {}
    for ax in fig.axes:
        line, label = ax.get_legend_handles_labels()
        for i, lab in enumerate(label):
            if lab not in unique_labels:
                unique_labels[lab] = line[i]
    # Reorder
    order = [
        "STrop Peaks*",
        "J05 Peak*",
        "T Peak*",
        "P Peak*",
        "S3000",
        "S1629",
        "S400",
        "S26",
        "S1629N",
        "G16",
        " ",
    ]
    for o in order:
        if o in unique_labels:
            tmp = unique_labels.pop(o)
            unique_labels[o] = tmp
    fig.legend(
        handles=list(unique_labels.values()),
        labels=list(unique_labels.keys()),
        ncols=3,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.015),
        frameon=False,
    )
    if save:
        SAVE_PATH = core.utils.if_save.create_savedir()
        fig.savefig(SAVE_PATH / "figure2")
        if (fig2 := (SAVE_PATH / "figure2.pdf")).exists():
            print(f"Successfully saved figure 2 to {fig2.resolve()}")
    if show_output:
        plt.show()
    else:
        plt.close("all")


if __name__ == "__main__":
    main(show_output=True)
