"""Create plots of some extra key eruption parameters."""

from collections import namedtuple
from typing import Literal

import matplotlib.pyplot as plt
import volcano_base.manipulate as vbm
import xarray as xr
from volcano_base.load import FindFiles

import paper1_code as core

SAVE_PATH = core.utils.if_save.create_savedir()
COLOR = core.config._C
FigElement = namedtuple("FigElement", ["data", "label", "color", "ls"])


class ReffPlot:
    """Plot the aerosol effective radius."""

    FINDER = (
        FindFiles()
        .find({"ens1", "ens3"}, {"tt-2sep", "tt-4sep", "medium-2sep", "medium-4sep"})
        .sort("ensemble", "sim")
        .copy
    )
    sad_ = FINDER().keep("SAD_AERO")
    reff_ = FINDER().keep("REFF_AERO")
    temp_ = FINDER().keep("T")

    def print(self) -> None:
        """Print all data that is being used."""
        print(self.sad_)
        print(self.reff_)
        print(self.temp_)

    def ens2median(self, arr: list[xr.DataArray]) -> xr.DataArray:
        """Combine a list of arrays from different (known) ensembles into a median."""
        arr = vbm.shift_arrays(arr, daily=False)
        # arr = vbm.shift_arrays(arr, custom=1, daily=False)
        arr_ = vbm.get_median(arr, xarray=True)
        arr_ = arr_[: int(12 * 16)]
        return arr_.assign_coords(time=vbm.dt2float(arr_.time.data) - 1850)

    def compute(self) -> xr.Dataset:
        """Compute the effective radius for all simulations."""
        sad = self.sad_.load()
        reff = self.reff_.load()
        temp = self.temp_.load()
        reff_s21 = core.utils.reff.Reff(reff[0], temp[0], sad[0]).calculate_reff()
        reff_s41 = core.utils.reff.Reff(reff[1], temp[1], sad[1]).calculate_reff()
        reff_m21 = core.utils.reff.Reff(reff[2], temp[2], sad[2]).calculate_reff()
        reff_m41 = core.utils.reff.Reff(reff[3], temp[3], sad[3]).calculate_reff()
        reff_s23 = core.utils.reff.Reff(reff[4], temp[4], sad[4]).calculate_reff()
        reff_s43 = core.utils.reff.Reff(reff[5], temp[5], sad[5]).calculate_reff()
        reff_m23 = core.utils.reff.Reff(reff[6], temp[6], sad[6]).calculate_reff()
        reff_m43 = core.utils.reff.Reff(reff[7], temp[7], sad[7]).calculate_reff()
        e2m = self.ens2median
        attrs = {"plot_c": COLOR[0], "plot_ls": "-"}
        reff_s2 = e2m([reff_s21, reff_s23]).assign_attrs(**attrs).rename("SMALL, 2sep")
        attrs = {"plot_c": COLOR[1], "plot_ls": "-"}
        reff_s4 = e2m([reff_s41, reff_s43]).assign_attrs(**attrs).rename("SMALL, 4sep")
        attrs = {"plot_c": COLOR[2], "plot_ls": "-"}
        reff_m2 = e2m([reff_m21, reff_m23]).assign_attrs(**attrs).rename("MEDIUM, 2sep")
        attrs = {"plot_c": COLOR[3], "plot_ls": "-"}
        reff_m4 = e2m([reff_m41, reff_m43]).assign_attrs(**attrs).rename("MEDIUM, 4sep")
        return xr.merge([reff_s2, reff_s4, reff_m2, reff_m4])

    def load(self) -> xr.Dataset:
        """Get or generate the data as a xarray data set."""
        file = SAVE_PATH / "reff.nc"
        if file.exists():
            return xr.load_dataset(file)
        ds = self.compute().assign_attrs(
            dict(description="Global stratospheric mean aerosol effective radius.")
        )
        ds.to_netcdf(file)
        return ds

    def plot(self) -> None:
        """Plot the computed arrays."""
        plt.figure()
        plt.semilogy()
        data = self.load()
        for name, r in data.data_vars.items():
            r.plot(label=name, c=r.plot_c, ls=r.plot_ls)  # type: ignore[call-arg]
        plt.xlabel("Time after first eruption [yr]")
        plt.ylabel(r"$R_{\text{eff}}$ $[\mathrm{\mu m}]$")
        plt.legend()
        plt.savefig(SAVE_PATH / "reff")
        plt.show()


class OHPlot:
    """Create plots of the OH CESM output field.

    Attributes
    ----------
    oh_c : FindFiles
        Object holding the file keys to the control simulation.
    oh_m : FindFiles
        Object holding the file keys to the smallest eruption simulation.
    oh_p : FindFiles
        Object holding the file keys to the intermediate eruption simulation.
    oh_s : FindFiles
        Object holding the file keys to the large eruption simulation.
    oh_e : FindFiles
        Object holding the file keys to the extreme eruption simulation.
    oh_m2 : FindFiles
        Object holding the file keys to the smallest 2-year double eruption simulation.
    oh_m4 : FindFiles
        Object holding the file keys to the smallest 4-year double eruption simulation.
    oh_p2 : FindFiles
        Object holding the file keys to the intermediate 2-year double eruption simulation.
    oh_p4 : FindFiles
        Object holding the file keys to the intermediate 4-year double eruption simulation.
    """

    _FINDER: FindFiles = (
        FindFiles().find("OH", "e_fSST1850").sort("sim", "ensemble").copy
    )
    oh_c: FindFiles = _FINDER().keep("control")
    # Only ens5 start in 1850 in the following three experiments. The rest were saved
    # from 1859 onwards.
    oh_m: FindFiles = _FINDER().keep("medium", "ens5")
    oh_p: FindFiles = _FINDER().keep("medium-plus", "ens5")
    oh_s: FindFiles = _FINDER().keep("strong", "ens5")
    oh_e: FindFiles = _FINDER().keep("size5000")
    oh_m2: FindFiles = _FINDER().keep("medium-2sep")
    oh_m4: FindFiles = _FINDER().keep("medium-4sep")
    oh_p2: FindFiles = _FINDER().keep("tt-2sep", {"ens1", "ens3"})
    oh_p4: FindFiles = _FINDER().keep("tt-4sep", {"ens1", "ens3"})

    @staticmethod
    def _remove_lev(arr: xr.DataArray) -> xr.DataArray:
        return arr.sum(dim="lev")

    def ens2median(self, arr: list[xr.DataArray]) -> xr.DataArray:
        """Combine a list of arrays from different (known) ensembles into a median."""
        arr = vbm.shift_arrays(arr, daily=False)
        # arr = vbm.shift_arrays(arr, custom=1, daily=False)
        arr = vbm.mean_flatten(arr, dims=["lat", "lon"])
        arr = vbm.data_array_operation(arr, self._remove_lev)
        arr_ = vbm.get_median(arr, xarray=True)
        arr_ = arr_[: int(12 * 16)]
        return arr_.assign_coords(time=vbm.dt2float(arr_.time.data) - 1850)

    def print_available(self) -> None:
        """Print all available data."""
        print(self._FINDER())

    def print(self) -> None:
        """Print all data that is being used."""
        print(self.oh_c)
        print(self.oh_m)
        print(self.oh_p)
        print(self.oh_s)
        print(self.oh_e)
        print(self.oh_m2)
        print(self.oh_m4)
        print(self.oh_p2)
        print(self.oh_p4)

    def compute(self) -> xr.Dataset:
        """Compute the global stratospheric mean OH for all simulations."""
        e2m = self.ens2median
        attrs = {"plot_c": COLOR[0], "plot_ls": "-"}
        oh_c_xr = e2m(self.oh_c.load()).assign_attrs(**attrs).rename("CONTROL")
        attrs = {"plot_c": COLOR[1], "plot_ls": "-"}
        oh_m_xr = e2m(self.oh_m.load()).assign_attrs(**attrs).rename("SMALL")
        attrs = {"plot_c": COLOR[2], "plot_ls": "-"}
        oh_p_xr = e2m(self.oh_p.load()).assign_attrs(**attrs).rename("MEDIUM")
        attrs = {"plot_c": COLOR[3], "plot_ls": "-"}
        oh_s_xr = e2m(self.oh_s.load()).assign_attrs(**attrs).rename("STRONG")
        attrs = {"plot_c": COLOR[4], "plot_ls": "-"}
        oh_e_xr = e2m(self.oh_e.load()).assign_attrs(**attrs).rename("EXTREME")
        attrs = {"plot_c": COLOR[1], "plot_ls": ":"}
        oh_m2_xr = e2m(self.oh_m2.load()).assign_attrs(**attrs).rename("_SMALL, 2sep")
        attrs = {"plot_c": COLOR[1], "plot_ls": "--"}
        oh_m4_xr = e2m(self.oh_m4.load()).assign_attrs(**attrs).rename("_SMALL, 4sep")
        attrs = {"plot_c": COLOR[2], "plot_ls": ":"}
        oh_p2_xr = e2m(self.oh_p2.load()).assign_attrs(**attrs).rename("_MEDIUM, 2sep")
        attrs = {"plot_c": COLOR[2], "plot_ls": "--"}
        oh_p4_xr = e2m(self.oh_p4.load()).assign_attrs(**attrs).rename("_MEDIUM, 4sep")
        return xr.merge(
            [
                oh_c_xr,
                oh_m_xr,
                oh_p_xr,
                oh_s_xr,
                oh_e_xr,
                oh_m2_xr,
                oh_m4_xr,
                oh_p2_xr,
                oh_p4_xr,
            ]
        )

    def load(self) -> xr.Dataset:
        """Get or generate the data as a xarray data set."""
        file = SAVE_PATH / "oh.nc"
        if file.exists():
            return xr.load_dataset(file)
        ds = self.compute().assign_attrs(
            dict(description="Global stratospheric mean OH concentration.")
        )
        ds.to_netcdf(file)
        return ds

    def plot(self, using: Literal["saved", "archive"] = "saved") -> None:
        """Plot the computed arrays.

        Parameters
        ----------
        using : Literal["saved", "archive"]
            Use data saved by this class (default) or computed from the archive (slow)
            to plot the data.
        """
        plt.figure()
        plt.semilogy()
        data = self.load()
        for name, o in data.data_vars.items():
            o.plot(label=name, color=o.plot_c, ls=o.plot_ls)  # type: ignore[call-arg]
        plt.legend()
        plt.xlabel("Time after first eruption [yr]")
        plt.ylabel("OH concentration")
        plt.savefig(SAVE_PATH / "oh")
        plt.show()


class SO2BurdenPlot:
    """Plot the SO2 column burden."""

    FINDER = (
        FindFiles()
        .find("TMSO2", "e_fSST1850", "h0")
        .keep_most_recent()
        .sort("sim", "ensemble")
        .copy
    )
    oh_c = FINDER().keep("control", "ens1")
    oh_m = FINDER().keep("medium", {f"ens{i}" for i in [2, 3, 4, 5]})
    oh_m2 = FINDER().keep("medium-2sep")
    oh_m4 = FINDER().keep("medium-4sep")
    oh_p = FINDER().keep("medium-plus", {f"ens{i}" for i in [2, 3, 4, 5]})
    oh_s = FINDER().keep("strong", {f"ens{i}" for i in [2, 3, 4, 5]})
    oh_e = FINDER().keep("size5000")
    oh_p2 = FINDER().keep("tt-2sep", {"ens1", "ens3"})
    oh_p4 = FINDER().keep("tt-4sep", {"ens1", "ens3"})

    @staticmethod
    def ens2median(arr: list[xr.DataArray]) -> xr.DataArray:
        """Combine a list of arrays from different (known) ensembles into a median."""
        arr = vbm.shift_arrays(arr, daily=False)
        # arr = vbm.shift_arrays(arr, custom=1, daily=False)
        arr = vbm.mean_flatten(arr, dims=["lat", "lon"])
        arr_ = vbm.get_median(arr, xarray=True)
        arr_ = arr_[: int(12 * 10)]
        return arr_.assign_coords(time=vbm.dt2float(arr_.time.data) - 1850)

    def print(self) -> None:
        """Print all data that is being used."""
        print(self.oh_c)
        print(self.oh_m)
        print(self.oh_p)
        print(self.oh_s)
        print(self.oh_e)
        print(self.oh_m2)
        print(self.oh_m4)
        print(self.oh_p2)
        print(self.oh_p4)

    def compute(self) -> xr.Dataset:
        """Compute the global mean TMSO2 for all simulations."""
        e2m = self.ens2median
        attrs = {"plot_ls": "-", "plot_c": COLOR[0]}
        oh_c_xr = e2m(self.oh_c.load()).assign_attrs(**attrs).rename("CONTROL")
        attrs = {"plot_c": COLOR[1], "plot_ls": "-"}
        oh_m_xr = e2m(self.oh_m.load()).assign_attrs(**attrs).rename("SMALL")
        attrs = {"plot_c": COLOR[2], "plot_ls": "-"}
        oh_p_xr = e2m(self.oh_p.load()).assign_attrs(**attrs).rename("MEDIUM")
        attrs = {"plot_c": COLOR[3], "plot_ls": "-"}
        oh_s_xr = e2m(self.oh_s.load()).assign_attrs(**attrs).rename("STRONG")
        attrs = {"plot_c": COLOR[4], "plot_ls": "-"}
        oh_e_xr = e2m(self.oh_e.load()).assign_attrs(**attrs).rename("EXTREME")
        attrs = {"plot_c": COLOR[1], "plot_ls": ":"}
        oh_m2_xr = e2m(self.oh_m2.load()).assign_attrs(**attrs).rename("_SMALL, 2sep")
        attrs = {"plot_c": COLOR[1], "plot_ls": "--"}
        oh_m4_xr = e2m(self.oh_m4.load()).assign_attrs(**attrs).rename("_SMALL, 4sep")
        attrs = {"plot_c": COLOR[2], "plot_ls": ":"}
        oh_p2_xr = e2m(self.oh_p2.load()).assign_attrs(**attrs).rename("_MEDIUM, 2sep")
        attrs = {"plot_c": COLOR[2], "plot_ls": "--"}
        oh_p4_xr = e2m(self.oh_p4.load()).assign_attrs(**attrs).rename("_MEDIUM, 4sep")
        return xr.merge(
            [
                oh_c_xr,
                oh_m_xr,
                oh_p_xr,
                oh_s_xr,
                oh_e_xr,
                oh_m2_xr,
                oh_m4_xr,
                oh_p2_xr,
                oh_p4_xr,
            ],
        )

    def load(self) -> xr.Dataset:
        """Get or generate the data as a xarray data set."""
        file = SAVE_PATH / "so2-burden.nc"
        if file.exists():
            return xr.load_dataset(file)
        ds = self.compute().assign_attrs(dict(description="Global mean SO2 burden."))
        ds.to_netcdf(file)
        return ds

    def plot(self) -> None:
        """Plot the computed arrays."""
        plt.figure()
        plt.semilogy()
        data = self.load()
        for name, s in data.data_vars.items():
            s.plot(label=name, color=s.plot_c, ls=s.plot_ls)  # type: ignore[call-arg]
        plt.legend()
        plt.xlabel("Time after first eruption [yr]")
        plt.savefig(SAVE_PATH / "so2-burden")
        plt.show()


ReffPlot().plot()
SO2BurdenPlot().plot()
OHPlot().plot()
