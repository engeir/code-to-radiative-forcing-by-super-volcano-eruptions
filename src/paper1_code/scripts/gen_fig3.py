"""Script that generates plots for figure 3."""

import pathlib
import sys
import tempfile
from typing import Literal, Self

import cosmoplots
import labellines
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import plastik
import scipy
import xarray as xr

import paper1_code as core
from paper1_code.scripts import load_data as core_load

# fmt: off
_C = core.config.COLOR_DICTS["category10"]
_P = core.config.POINTS_DICTS
_DATA_TYPES = Literal[
    "P", "P100", "VT", "c2w", "c2wm",
    "c2wmp", "c2ws", "c2wn", "greg",
]
LEGENDS: dict[_DATA_TYPES, dict] = {
    "P": {"c": _C[4], "marker": _P["star"], "s": 15, "zorder": 5, "label": "P"},
    "P100": {"c": _C[6], "marker": _P["square"], "s": 5, "zorder": 5, "label": "J05"},
    "VT": {"c": _C[8], "marker": _P["plus"], "s": 15, "zorder": 5, "label": "T"},
    "c2w": {"c": _C[0], "marker": _P["diamond"], "ms": 2, "zorder": 4, "label": "C2W"},
    "c2wm": {"c": _C[0], "marker": _P["triangle_down"], "s": 5, "zorder": 3, "label": r"C2W$\downarrow$"},
    "c2wmp": {"c": _C[1], "marker": _P["diamond"], "s": 5, "zorder": 3, "label": r"C2W$-$"},
    "c2ws": {"c": _C[2], "marker": _P["triangle_up"], "s": 5, "zorder": 3, "label": r"C2W$\uparrow$"},
    "c2wn": {"c": _C[5], "marker": _P["tri_up"], "s": 15, "zorder": 4, "label": r"C2WN$\uparrow$"},
    "greg": {"c": _C[7], "marker": _P["x"], "s": 5, "zorder": -1, "label": "G16"},
}
# fmt: on


class _GregoryPaper:
    def __init__(self) -> None:
        self._timeseries: list[xr.DataArray] = []
        self._ensemble = [1, 2, 3, 4]
        self._vars = [
            "aod",
            "tas",
            "tas-clim",
            "rf",
        ]

    def with_ensemble(self, *args: Literal[1, 2, 3, 4]) -> Self:
        self.ensemble = args or [1, 2, 3, 4]
        return self

    def with_vars(
        self,
        *args: Literal[
            "aod",
            "tas",
            "tas-clim",
            "rf",
        ],
    ) -> Self:
        self.vars = args or [
            "aod",
            "tas",
            "tas-clim",
            "rf",
        ]
        return self

    def _return_dataarray(self, ds: xr.Dataset, var: str) -> xr.DataArray:
        da: xr.DataArray = getattr(ds, var)
        da_attrs = self._keep_attrs(ds, da)
        return da.assign_attrs(da_attrs)

    def _keep_attrs(self, ds: xr.Dataset, da: xr.DataArray) -> dict:
        ds_attrs = ds.attrs
        da_attrs = da.attrs
        common = set(da_attrs) & set(ds_attrs)
        for c in common:
            ds_attrs[f"ds_{c}"] = ds_attrs[c]
            ds_attrs.pop(c)
        da_attrs.update(**ds_attrs)
        return da_attrs

    def _try_open(self, file: pathlib.Path | str) -> xr.Dataset | None:
        try:
            ds = xr.open_dataset(file)
        except OSError:
            return None
        return ds

    def _load_dataset(self, var, ensemble):
        path = pathlib.Path(core.config.DATA_DIR_ROOT) / "gregory"
        if not path.exists():
            sys.exit("Did you forget to mount the hard disk?")
        match ensemble, var:
            case _, "aod":
                ds_var = "data"
                ds = self._try_open(path / "aod.nc")
            case _, "rf":
                ds_var = "data"
                ds = self._try_open(path / "erf.nc")
            case _, "tas-clim":
                ds_var = "air_temperature"
                ds = self._try_open(path / "xfqqe.tas.nc")
            case e, "tas":
                ds_var = "air_temperature"
                ds = self._try_open(path / f"xjwgh{e}.tas.nc")
            case _:
                return None, None
        if isinstance(ds, xr.Dataset | xr.DataArray):
            ds.attrs["var_name"] = var
        return ds, ds_var

    def _load_datasets(self) -> None:
        for var in getattr(self, "vars", self._vars):
            if var != "tas":
                ds, ds_var = self._load_dataset(var, "")
                if ds is not None:
                    out = self._return_dataarray(ds, ds_var) if self._da else ds
                    self._timeseries.append(out)
            else:
                for ensemble in getattr(self, "ensemble", self._ensemble):
                    ds, ds_var = self._load_dataset(var, ensemble)
                    if ds is not None:
                        out = self._return_dataarray(ds, ds_var) if self._da else ds
                        self._timeseries.append(out)

    def load(
        self, dataarray: bool = True, true_month: bool = False
    ) -> list[xr.DataArray]:
        """Load all specified data.

        Parameters
        ----------
        dataarray : bool
            If True, all elements obtained from _GregoryPaper are xr.DataArray
            objects, otherwise they will be xr.Dataset objects.
        true_month : bool
            If True, use the same months as the original data set, otherwise the first
            month is set to January.

        Returns
        -------
        list[xr.DataArray]
            Returns a list of the specified data

        Raises
        ------
        AttributeError
            If the specified simulation parameters do not result in any matches
        """
        self._da = dataarray
        self._true_month = true_month
        self._load_datasets()
        if not self._timeseries:
            raise AttributeError(
                "The combination of simulation, variable and institution did not"
                " result in any matches. Try using fewer restrictions."
            )
        return self._timeseries


def gregory_paper() -> _GregoryPaper:
    """Get data from the simulations done by Gregory in his 2016 paper.

    Returns
    -------
    _GregoryPaper
        Returns an instance of the _GregoryPaper class

    Notes
    -----
    Data from the HadCM3 simulations by Gregory et al. (2016).

    Examples
    --------
    The `with_` methods without any parameters is equivalent to passing all possible
    parameters.

    >>> gregory_paper().with_ensemble().with_vars().load(True)
    """
    return _GregoryPaper()


def get_gregory_paper_data() -> tuple[np.ndarray, xr.DataArray, xr.DataArray]:
    """Return data from Gregory et al. (2016) paper."""
    g = gregory_paper().with_vars("rf", "aod").with_ensemble(1).load()
    rf = g[0]
    aod = g[1]
    rf = core.utils.time_series.keep_whole_years(rf)
    aod = core.utils.time_series.keep_whole_years(aod)
    rf = core.utils.time_series.weighted_year_avg(rf)
    aod = core.utils.time_series.weighted_year_avg(aod)
    greg_x = np.linspace(0, 15)
    return greg_x, aod, rf


def plot_gregory_paper_gradient_lines(x, ax: mpl.axes.Axes, size: str) -> None:
    """Create the gradient lines from the Gregory et al. (2016) paper."""
    col = LEGENDS["greg"]["c"]
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


def _set_cesm2_avg() -> tuple[list[np.ndarray], list[np.ndarray]]:
    weighter = core.utils.time_series.weighted_year_avg
    aod_m, aod_mp, aod_s, aod_h = core_load._set_aod_arrs(shift=0)
    aod = aod_m + aod_mp + aod_s + aod_h
    rf_m, rf_mp, rf_s, rf_h = core_load._set_rf_arrs(shift=0)
    rf = rf_m + rf_mp + rf_s + rf_h
    # Check that they include the same items
    aod = core.utils.time_series.keep_whole_years(aod, freq="MS")
    rf = core.utils.time_series.keep_whole_years(rf, freq="MS")
    time_ar = [np.array([])] * 6
    aod_ar = [np.array([])] * 6
    rf_ar = [np.array([])] * 6
    for a, c in zip(aod, rf, strict=True):
        # Place the arrays in lists based on eruption strength
        if a.ensemble == c.ensemble and a.sim == c.sim:
            a_, c_ = xr.align(a, c)
            match a.sim:
                case str(x) if "medium-plus" in x:
                    i = 1
                case str(x) if "medium" in x:
                    i = 0
                case str(x) if "strong-highlat" in x:
                    i = 5
                case str(x) if "strong" in x:
                    i = 2
                case str(x) if "double-overlap" in x:
                    i = 3
                case _:
                    raise ValueError(f"There is no simulation with {a.sim}")
            aod_ar[i] = np.r_[aod_ar[i], weighter(a_).data]
            time_ar[i] = np.r_[time_ar[i], weighter(a_).time.data]
            rf_ar[i] = np.r_[rf_ar[i], weighter(c_).data]
    return aod_ar, rf_ar


def get_aod_pinatubo() -> float:
    """Aerosol optical depth due to Mount Pinatubo.

    See for example Sukhodolov (2018).
    """
    return 0.15


def get_rf_pinatubo() -> float:
    """Top-of-atmosphere radiative imbalance due to Mount Pinatubo.

    Douglass, D. H., Knox, R. S., et al. (2006) report a value of ~3.4 while
    Gregory, J. M., Andrews, T., et al., (2016) report a value of ~3.0.
    """
    return 3.2


def get_aod_j05() -> float:
    """Based on the paper by Jones et al. (2005).

    Notes
    -----
    DOI: 10.1007/s00382-005-0066-8
    """
    return 15


def get_rf_j05() -> float:
    """Top-of-atmosphere radiative imbalance due to Mount Pinatubo, times 100.

    See Jones et al. (2005).
    """
    return 60


def get_aod_tambora() -> float:
    """From EVAv1.2(eVolv2k), Tambora 1815, Toohey and Sigl (2017).

    Notes
    -----
    Download data from https://www.wdc-climate.de/ui/entry?acronym=eVolv2k_v3.
    """
    return 0.355


def get_rf_tambora() -> float:
    """From Raible et al. (2016), p. 573.

    Notes
    -----
    https://doi.org/10.1002/wcc.407
    """
    return 5


def get_aod_peak() -> tuple[float, float, float]:
    """Get the AOD peak from the CESM2 simulations."""
    m_, mp_, s_, _ = core_load._set_aod_arrs(shift=0)
    s = core.utils.time_series.get_median(s_, xarray=True)
    mp = core.utils.time_series.get_median(mp_, xarray=True)
    m = core.utils.time_series.get_median(m_, xarray=True)
    return (
        scipy.signal.savgol_filter(m.data, 12, 3).max(),
        scipy.signal.savgol_filter(mp.data, 12, 3).max(),
        scipy.signal.savgol_filter(s.data, 12, 3).max(),
    )


def get_rf_peak() -> tuple[float, float, float]:
    """Get the radiative forcing peak from the CESM2 simulations."""
    m_, mp_, s_, _ = core_load._set_rf_arrs(shift=0)
    s = core.utils.time_series.get_median(s_, xarray=True)
    mp = core.utils.time_series.get_median(mp_, xarray=True)
    m = core.utils.time_series.get_median(m_, xarray=True)
    s.data *= -1
    mp.data *= -1
    m.data *= -1
    return (
        scipy.signal.savgol_filter(m.data, 12, 3).max(),
        scipy.signal.savgol_filter(mp.data, 12, 3).max(),
        scipy.signal.savgol_filter(s.data, 12, 3).max(),
    )


def plot_aod_vs_rf_avg() -> tuple[mpl.figure.Figure, mpl.figure.Figure]:
    """Plot yearly mean RF against AOD."""
    x_g16, aod_g16, rf_g16 = get_gregory_paper_data()
    aod_c2w, rf_c2w = _set_cesm2_avg()
    aod_p, rf_p = get_aod_pinatubo(), get_rf_pinatubo()
    aod_j05, rf_j05 = get_aod_j05(), get_rf_j05()
    aod_t, rf_t = get_aod_tambora(), get_rf_tambora()
    aod_c2w_peak, rf_c2w_peak = get_aod_peak(), get_rf_peak()
    # Create figures
    fig1 = plt.figure()
    ax1 = fig1.gca()
    fig2 = plt.figure()
    ax2 = fig2.gca()
    for size, ax_ in zip(["large", "small"], [ax1, ax2], strict=True):
        if size == "large":
            ax_.fill_between([0, 0.15 * 8 / 3], -3 * 8 / 3, 1 * 8 / 3, color="gray")
        plot_gregory_paper_gradient_lines(x_g16, ax_, size)
        plot = ax_.scatter
        if size == "large":
            plot(
                aod_c2w_peak,
                np.array(rf_c2w_peak) * (-1),
                label="C2W Peaks*",
                c="none",
                ec="red",
                s=15,
                zorder=10,
                **{
                    x: LEGENDS["c2w"][x]
                    for x in LEGENDS["c2w"]
                    if x not in ["c", "label", "marker", "ms", "zorder"]
                },
            )
        legend = {x: LEGENDS["VT"][x] for x in LEGENDS["VT"] if x not in "label"}
        plot(aod_t, -rf_t, label="T Peak*", **legend)
        plot(aod_c2w[2], rf_c2w[2], **LEGENDS["c2ws"])
        plot(aod_c2w[1], rf_c2w[1], **LEGENDS["c2wmp"])
        plot(aod_c2w[0], rf_c2w[0], **LEGENDS["c2wm"])
        if size == "large":
            legend = {
                x: LEGENDS["P100"][x] for x in LEGENDS["P100"] if x not in "label"
            }
            plot(aod_j05, -rf_j05, label="P100 Peak*", **legend)
            legend_width = 0.45
        else:
            legend_width = 0.41
        legend = {x: LEGENDS["P"][x] for x in LEGENDS["P"] if x not in "label"}
        plot(aod_p, -rf_p, label="P Peak*", **legend)
        plot(aod_c2w[5], rf_c2w[5], **LEGENDS["c2wn"])
        plot([], [], label=" ", c="none")
        plot(aod_g16.data, rf_g16.data, **LEGENDS["greg"])
        xlim = (-0.75, 15.75) if size == "large" else (0, 0.15 * 8 / 3)
        ylim = (-85, 5) if size == "large" else (-3 * 8 / 3, 1 * 8 / 3)
        ax_.set_xlim(xlim)
        ax_.set_ylim(ylim)
        ax_.set_xlabel("Aerosol optical depth [1]")
        ax_.set_ylabel("Radiative forcing $[\\mathrm{W/m^2}]$")
        kwargs = {
            "c_max": 2,
            "side": "bottom left",
            "anchor_": (-0.01, -0.02, legend_width, 0.3),
            "alpha": 0.8,
            "ec": "gray",
            "fontsize": 5,
            "mode": "expand",
        }
        plastik.topside_legends(ax_, **kwargs)
    return fig1, fig2


def main():
    """Run the main program."""
    TMP = tempfile.TemporaryDirectory()
    tmp_dir = pathlib.Path(TMP.name)
    save = True
    large, small = plot_aod_vs_rf_avg()
    if save:
        SAVE_PATH = core.scripts.if_save.create_savedir()
        large.savefig(tmp_dir / "aod_vs_rf_avg_full.png")
        small.savefig(tmp_dir / "aod_vs_rf_avg_inset.png")
        cosmoplots.combine(
            tmp_dir / "aod_vs_rf_avg_full.png",
            tmp_dir / "aod_vs_rf_avg_inset.png",
        ).using(fontsize=50).in_grid(1, 2).save(SAVE_PATH / "aod_vs_rf_avg.png")
        if (fig3 := (SAVE_PATH / "aod_vs_rf_avg.png")).exists():
            print(f"Successfully saved figure 3 to {fig3.resolve()}")
    plt.show()
    TMP.cleanup()


if __name__ == "__main__":
    main()
