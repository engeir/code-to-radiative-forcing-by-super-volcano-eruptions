"""Load Gregory et al. (2016) data."""

# FIXME: add doi.

import pathlib
import sys
from typing import Literal, Self

import numpy as np
import xarray as xr

import paper1_code as core


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
