"""Script that generates plots for figure 3."""

import pathlib
import tempfile

import cosmoplots
import labellines
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import paper1_code as core


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
            core.load.cesm2.get_aod_c2w_peaks()[:3],
            core.load.cesm2.get_rf_c2w_peaks()[:3],
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

    def plot_aod_vs_rf_avg(self) -> tuple[mpl.figure.Figure, mpl.figure.Figure]:
        """Plot yearly mean RF against AOD."""
        fig3_a = plt.figure()
        ax1 = fig3_a.gca()
        fig3_b = plt.figure()
        ax2 = fig3_b.gca()
        for size, ax_ in zip(["large", "small"], [ax1, ax2], strict=True):
            self.plot_gregory_paper_gradient_lines(self.data.x_g16, ax_, size)
            plot = ax_.scatter
            if size == "large":
                plot(
                    self.data.aod_c2w_peak,
                    np.array(self.data.rf_c2w_peak) * (-1),
                    label="C2W Peaks*",
                    c="none",
                    ec="red",
                    s=15,
                    zorder=10,
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
            plot(self.data.aod_t, -self.data.rf_t, label="T Peak*", **legend)
            plot(
                self.data.aod_c2w[2], self.data.rf_c2w[2], **core.config.LEGENDS["c2ws"]
            )
            plot(
                self.data.aod_c2w[1],
                self.data.rf_c2w[1],
                **core.config.LEGENDS["c2wmp"],
            )
            plot(
                self.data.aod_c2w[0], self.data.rf_c2w[0], **core.config.LEGENDS["c2wm"]
            )
            if size == "large":
                legend = {
                    x: core.config.LEGENDS["P100"][x]
                    for x in core.config.LEGENDS["P100"]
                    if x not in "label"
                }
                plot(self.data.aod_j05, -self.data.rf_j05, label="P100 Peak*", **legend)
            legend = {
                x: core.config.LEGENDS["P"][x]
                for x in core.config.LEGENDS["P"]
                if x not in "label"
            }
            plot(self.data.aod_p, -self.data.rf_p, label="P Peak*", **legend)
            plot(
                self.data.aod_c2w[5], self.data.rf_c2w[5], **core.config.LEGENDS["c2wn"]
            )
            plot([], [], label=" ", c="none")
            plot(self.data.aod_g16, self.data.rf_g16, **core.config.LEGENDS["greg"])
            xlim = (-0.75, 15.75) if size == "large" else (0, 0.15 * 8 / 3)
            ylim = (-85, 5) if size == "large" else (-3 * 8 / 3, 1 * 8 / 3)
            ax_.set_xlim(xlim)
            ax_.set_ylim(ylim)
            ax_.set_xlabel("Aerosol optical depth [1]")
            ax_.set_ylabel("Radiative forcing $[\\mathrm{W/m^2}]$")
            kwargs = {
                "ncol": 2,
                "loc": "upper right",
                "framealpha": 0.8,
                "edgecolor": "gray",
                "fontsize": core.config.FONTSIZE,
                "labelspacing": 0.3,
                "handletextpad": 0.2,
                "columnspacing": 0.3,
            }
            ax_.legend(**kwargs)
        return fig3_a, fig3_b


def main(show_output: bool = False):
    """Run the main program."""
    TMP = tempfile.TemporaryDirectory()
    tmp_dir = pathlib.Path(TMP.name)
    save = True
    plotter = DoPlotting(show_output)
    large, small = plotter.plot_aod_vs_rf_avg()
    if save:
        SAVE_PATH = core.utils.if_save.create_savedir()
        large.savefig(tmp_dir / "aod_vs_rf_avg_full.png")
        small.savefig(tmp_dir / "aod_vs_rf_avg_inset.png")
        cosmoplots.combine(
            tmp_dir / "aod_vs_rf_avg_full.png",
            tmp_dir / "aod_vs_rf_avg_inset.png",
        ).using(fontsize=50).in_grid(1, 2).save(SAVE_PATH / "figure2.png")
        if (fig2 := (SAVE_PATH / "figure2.png")).exists():
            print(f"Successfully saved figure 2 to {fig2.resolve()}")
    if show_output:
        plt.show()
    else:
        plt.close("all")
    TMP.cleanup()


if __name__ == "__main__":
    main(show_output=True)
