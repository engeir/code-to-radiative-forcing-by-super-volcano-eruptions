"""Load Marshall et al. 2020 data.

Notes
-----
See https://doi.org/10.5285/232164e8b1444978a41f2acf8bbbfe91 for access to the complete
dataset.
"""

import datetime

import numpy as np
import scipy
import xarray as xr

import paper1_code as core


def get_m20(find_all_peaks: bool = False) -> tuple[np.ndarray, ...]:
    """Create samples from Marshall et al. 2020."""
    # Need AOD and RF seasonal and annual means, as well as an array of equal length
    # with the corresponding time-after-eruption.
    path = (
        core.config.DATA_DIR_ROOT
        / "marshall"
        / "dap.ceda.ac.uk"
        / "badc"
        / "deposited2020"
        / "vol-clim"
        / "data"
        / "UM-UKCA_volcanic_ensemble"
    )
    files = list(path.rglob("UM_UKCA*.nc"))
    data: list[xr.Dataset] = [xr.load_dataset(file.resolve()) for file in files]
    data = core.utils.find_c2w_files.FindFiles().sort("SO2 emission (Tg)", arrays=data)
    # We first move the July eruptions back six months to January, so all have the
    # eruption day as the first element.
    for i, arr in enumerate(data):
        if arr.attrs["Eruption season"] == "Jul":
            data[i] = arr.assign_coords(
                time=arr.time.data - datetime.timedelta(days=180)
            )
    # Check that both seasons do indeed start at the same date.
    # Let us also check that 12 elements in, we are one year ahead.
    first = str(data[0].time.data[0])
    for arr in data[1:]:
        if str(arr.time.data[0]) != first:
            raise ValueError("Seasons do not start at the same date.")
        if f"{str(arr.time.data[12])[:3]}0{str(arr.time.data[12])[3 + 1:]}" != first:
            raise ValueError("This is not same day, next year.")

    weighter = core.utils.time_series.weighted_season_avg
    time, so2, aod, rf, temp = [], [], [], [], []
    if find_all_peaks:
        for arr in data:
            # Find peak using savgol filter, then plot SO2 versus {AOD, ERF, T}.
            rf_arr = scipy.signal.savgol_filter(
                arr["effective_radiative_forcing"], 12, 3
            )
            temp_arr = scipy.signal.savgol_filter(
                arr["surface_temperature_adjustment"], 12, 3
            )
            aod_arr = scipy.signal.savgol_filter(
                arr["stratospheric_aerosol_optical_depth_at_550_nm"], 12, 3
            )
            so2.append(arr.attrs["SO2 emission (Tg)"])
            aod.append(aod_arr.max())
            rf.append(rf_arr.min())
            temp.append(temp_arr.max())
        return np.asarray(so2), np.asarray(aod), -np.asarray(rf), np.asarray(temp)
    tropical_limit = 10
    for arr in data:
        if abs(arr.attrs["Eruption latitude (degrees N)"]) > tropical_limit:
            continue
        time.append(
            core.utils.time_series.dt2float(
                weighter(arr["effective_radiative_forcing"]).time.data,
                days_in_year=360,
            )
        )
        aod.append(weighter(arr["stratospheric_aerosol_optical_depth_at_550_nm"]).data)
        rf.append(weighter(arr["effective_radiative_forcing"]).data)
    # All arrays now have time dimensions in float format, starting at 0.0.
    return np.asarray(time), np.asarray(aod), np.asarray(rf)
