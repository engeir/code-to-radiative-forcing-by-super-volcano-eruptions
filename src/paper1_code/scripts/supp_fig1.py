"""Script that generates plots for figure 2."""

import pathlib
import tempfile
import warnings

import cosmoplots
import matplotlib as mpl
import matplotlib.pyplot as plt
import plastik

import paper1_code as core


class SetupNeededData:
    """Class that loads all data used in the plotting procedures."""

    def __init__(self):
        aod_m, aod_mp, aod_s, aod_ss, aod_h = core.load.cesm2.get_aod_arrs()
        self.aod = aod_m + aod_mp + aod_s + aod_ss + aod_h
        rf_m, rf_mp, rf_s, rf_ss, rf_h = core.load.cesm2.get_rf_arrs()
        self.rf = rf_m + rf_mp + rf_s + rf_ss + rf_h
        temp_m, temp_mp, temp_s, temp_ss, temp_h = core.load.cesm2.get_trefht_arrs()
        self.temp = temp_m + temp_mp + temp_s + temp_ss + temp_h


class DoPlotting:
    """Class that takes care of all the plotting."""

    def __init__(self, print_summary: bool):
        self.print_summary = print_summary
        self.data = SetupNeededData()

    def _array_leginizer(self, ax: mpl.axes.Axes) -> mpl.axes.Axes:
        c4 = plastik.colors.create_colorlist("cmc.batlow", 4)
        c14 = [c4[0]] * 4 + [c4[1]] * 4 + [c4[3]] * 4 + ["r"] + [c4[2]] * 2
        for n, c_ in zip(ax.get_lines(), c14, strict=False):
            n.set_color(c_)
        # Otherwise, it yells at me with UserWarning's cuz of the leading underscore
        warnings.simplefilter("ignore")
        ax.legend(
            [
                r"C2W$\downarrow$",
                r"_C2W$\downarrow$",
                r"_C2W$\downarrow$",
                r"_C2W$\downarrow$",
                "C2W$-$",
                "_C2W$-$",
                "_C2W$-$",
                "_C2W$-$",
                r"C2W$\uparrow$",
                r"_C2W$\uparrow$",
                r"_C2W$\uparrow$",
                r"_C2W$\uparrow$",
                r"C2WS$\uparrow$",
                r"C2WN$\uparrow$",
                r"_C2WN$\uparrow$",
            ],
            fontsize=core.config.FONTSIZE,
            loc="right",
            reverse=True,
        ).get_frame().set_alpha(0.8)
        warnings.resetwarnings()
        return ax

    def plot_arrays(
        self,
    ) -> tuple[mpl.figure.Figure, mpl.figure.Figure, mpl.figure.Figure]:
        """Plot the data that is used in other analysis methods.

        Returns
        -------
        tuple[mpl.figure.Figure, mpl.figure.Figure, mpl.figure.Figure]
            The figures returned are
            - AOD normalized
            - RF normalized
            - TREFHT normalized
        """
        # Check that they include the same items
        aod = core.utils.time_series.keep_whole_years(self.data.aod, freq="MS")
        rf = core.utils.time_series.keep_whole_years(self.data.rf, freq="MS")
        temp = core.utils.time_series.keep_whole_years(self.data.temp, freq="MS")
        length_years = 8
        for i, (arr1, arr2, arr3) in enumerate(zip(aod, rf, temp, strict=True)):
            aod[i] = arr1[: int(length_years * 12)]
            rf[i] = arr2[: int(length_years * 12)]
            temp[i] = arr3[: int(length_years * 12)]
        for i, array in enumerate(aod):
            # aod_array_ = array.assign_coords(
            #     time=array.time.data - datetime.timedelta(days=1850 * 365)
            # )
            aod[i] = array.assign_coords(
                time=core.utils.time_series.dt2float(array.time.data)
            )
        for i, array in enumerate(rf):
            # rf_array_: xr.DataArray = array.assign_coords(
            #     time=array.time.data - datetime.timedelta(days=1850 * 365)
            # )
            rf[i] = array.assign_coords(
                time=core.utils.time_series.dt2float(array.time.data)
            )
        for i, array in enumerate(temp):
            # temp_array_: xr.DataArray = array.assign_coords(
            #     time=array.time.data - datetime.timedelta(days=1850 * 365)
            # )
            temp[i] = array.assign_coords(
                time=core.utils.time_series.dt2float(array.time.data)
            )
        newaod, newrf, newtemp = core.utils.time_series.normalize_peaks(
            (aod, "aod"), (rf, "rf"), (temp, "rf")
        )
        fig2_a = self._plot_arrays(newaod, "Normalized \naerosol optical depth $[1]$")
        fig2_b = self._plot_arrays(newrf, "Normalized \nradiative forcing $[1]$")
        fig2_c = self._plot_arrays(newtemp, "Normalized \ntemperature $[1]$")
        return fig2_a, fig2_b, fig2_c

    def _plot_arrays(self, arrays, y_label):
        result = plt.figure()
        ax_a = result.gca()
        for a in arrays:
            ax_a.plot(a.time.data, a.data)
        ax_a = self._array_leginizer(ax_a)
        plt.xlabel(r"Time after eruption $[\mathrm{year}]$")
        plt.ylabel(y_label)
        return result


def main(show_output: bool = False):
    """Run the main program."""
    TMP = tempfile.TemporaryDirectory()
    tmp_dir = pathlib.Path(TMP.name)
    save = False
    plotter = DoPlotting(show_output)
    aod, rf, temp = plotter.plot_arrays()
    if save:
        SAVE_PATH = core.utils.if_save.create_savedir()
        aod.savefig(tmp_dir / "aod_arrays_normalized")
        rf.savefig(tmp_dir / "rf_arrays_normalized")
        cosmoplots.combine(
            tmp_dir / "aod_arrays_normalized.png",
            tmp_dir / "rf_arrays_normalized.png",
        ).using(fontsize=8).in_grid(1, 2).save(
            SAVE_PATH / "arrays_combined_normalized.png"
        )
        if (fig1 := (SAVE_PATH / "arrays_combined_normalized.png")).exists():
            print(f"Successfully saved figure 1 to {fig1.resolve()}")
    if show_output:
        plt.show()
    else:
        plt.close("all")
    TMP.cleanup()


if __name__ == "__main__":
    main(show_output=True)
