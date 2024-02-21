"""Load Otto-Bliesner et al. 2016 data.

Notes
-----
See https://doi.org/10.1175/BAMS-D-14-00233.1 for the full paper and link to where the
datasets are stored.
"""

import datetime
import itertools
import re
import subprocess
from typing import Literal

import numpy as np
import requests
import rich.progress
import scipy
import xarray as xr

import paper1_code as core


def save_to_npz() -> None:
    """Save the OB16 data to .npz files."""
    # Download OB16 output datasets.
    _download_ob16_output_files()
    # Combine and convert the datasets and save to compressed .npz files.
    path = core.config.DATA_DIR_ROOT / "cesm-lme"
    if not path.exists():
        path.mkdir(parents=False)
    _save_output_files_to_npz(path)
    # Input file with injected SO2.
    _download_so2_file(path)
    print(f"You might want to clean up the .nc files in {core.config.PROJECT_ROOT}.")


def _download_ob16_output_files() -> None:
    script_path = core.config.PROJECT_ROOT / "src" / "paper1_code" / "load"
    script = "python-ucar.cgd.ccsm4.cesmLME.atm.proc.daily_ave."
    subprocess.call(["python", script_path / f"{script}FSNTOA-20240103T0650.py"])
    subprocess.call(["python", script_path / f"{script}TREFHT-20240103T0651.py"])


def _save_output_files_to_npz(path) -> None:
    file0 = "b.e11.BLMTRC5CN.f19_g16.VOLC_GRA.00"
    file1 = ".cam.h0."
    file2_0 = ".08500101-18491231.nc"
    file2_1 = ".18500101-20051231.nc"
    # Temperature.
    for i in range(5):
        file_0 = file0 + str(i + 1) + file1 + "TREFHT" + file2_0
        file_1 = file0 + str(i + 1) + file1 + "TREFHT" + file2_1
        data = xr.open_mfdataset([file_0, file_1])
        array = core.utils.time_series.mean_flatten(data["TREFHT"], dims=["lat", "lon"])
        np.savez(path / f"TREFHT-00{i+1}", data=array.data, times=array.time.data)
    # RF forcing
    for i in range(5):
        file_0 = file0 + str(i + 1) + file1 + "FSNTOA" + file2_0
        file_1 = file0 + str(i + 1) + file1 + "FSNTOA" + file2_1
        data = xr.open_mfdataset([file_0, file_1])
        array = core.utils.time_series.mean_flatten(data["FSNTOA"], dims=["lat", "lon"])
        np.savez(path / f"FSNTOA-00{i+1}", data=array.data, times=array.time.data)
    # Control run for temperature.
    data = xr.open_mfdataset(
        [
            "b.e11.BLMTRC5CN.f19_g16.850forcing.003.cam.h0.TREFHT.08500101-18491231.nc",
            "b.e11.BLMTRC5CN.f19_g16.850forcing.003.cam.h0.TREFHT.18500101-20051231.nc",
        ]
    )
    array = core.utils.time_series.mean_flatten(data["TREFHT"], dims=["lat", "lon"])
    np.savez(
        path / "TREFHT850forcing-control-003.npz",
        data=array.data,
        times=array.time.data,
    )


def _download_so2_file(path) -> None:
    name = "IVI2LoadingLatHeight501-2000_L18_c20100518.nc"
    if (path / name).exists():
        print(
            f"{path/name} already exists, so I skip this. Delete it first if you are"
            " sure you want to download it again."
        )
        return
    url = f"https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/cam/volc/{name}"
    progress = rich.progress.Progress(
        rich.progress.TextColumn("[progress.description]{task.description}"),
        rich.progress.SpinnerColumn(),
        rich.progress.BarColumn(),
        rich.progress.TaskProgressColumn(),
        rich.progress.MofNCompleteColumn(),
        rich.progress.TimeRemainingColumn(elapsed_when_finished=True),
    )
    with requests.get(url, stream=True, verify=False) as r:
        r.raise_for_status()
        with open(path / name, "wb") as f:
            with progress:
                for chunk in progress.track(
                    r.iter_content(chunk_size=8192),
                    total=20851,
                    description="[cyan]Downloading file...",
                ):
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    # if chunk:
                    f.write(chunk)


def _get_ob16_rf_temp_arrays() -> tuple[list[xr.DataArray], list[xr.DataArray]]:
    """Create samples from Otto-Bliesner et al. 2016.

    Returns
    -------
    tuple[list[xr.DataArray], list[xr.DataArray]]
        The AOD and RF arrays in two lists

    Raises
    ------
    FileNotFoundError
        If the directory where all the files is not found.
    """
    # Need AOD and RF seasonal and annual means, as well as an array of equal length
    # with the corresponding time-after-eruption.
    path = core.config.DATA_DIR_ROOT / "cesm-lme"
    if not path.exists():
        raise FileNotFoundError(
            "Cannot find CESM-LME files. You may try to run the `save_to_npz` function"
            f" within {__name__}."
        )
    pattern = re.compile("([A-Z]+)-00[1-5]\\.npz$", re.X)
    files_ = list(path.rglob("*00[1-5].npz"))
    rf, temp = [], []
    for file in files_:
        if isinstance(search := pattern.search(str(file)), re.Match):
            array = _load_numpy(file.resolve())
            s = "0850-01-01"
            t = xr.cftime_range(
                start=s, periods=len(array.data), calendar="noleap", freq="D"
            )
            if search.groups()[0] == "TREFHT":
                temp.append(array.assign_coords({"time": t}))
            elif search.groups()[0] == "FSNTOA":
                rf.append(array.assign_coords({"time": t}))
    return rf, temp


def _load_numpy(np_file) -> xr.DataArray:
    """Load the content of an npz file as an xarray DataArray."""
    with np.load(np_file, allow_pickle=True) as data:
        two_dim_data = 2
        if data["data"].ndim == two_dim_data:
            if "lev" in data.files and data["lev"].shape != ():
                lev_str = "lev"
            elif "ilev" in data.files and data["ilev"].shape != ():
                lev_str = "ilev"
            else:
                raise KeyError(f"There is no level information in the file {np_file}")
            coords = {"time": data["times"], lev_str: data[lev_str]}
            dims = ["time", lev_str]
        else:
            coords = {"time": data["times"]}
            dims = ["time"]
        xarr = xr.DataArray(data["data"], dims=dims, coords=coords)
    return xarr


def _remove_seasonality_ob16(arr: xr.DataArray, monthly: bool = False) -> xr.DataArray:
    """Remove seasonality by subtracting CESM LME control run."""
    file_name = (
        core.config.DATA_DIR_ROOT / "cesm-lme" / "TREFHT850forcing-control-003.npz"
    )
    if file_name.exists():
        array = _load_numpy(file_name.resolve())
        s = "0850-01-01"
        t = xr.cftime_range(
            start=s, periods=len(array.data), calendar="noleap", freq="D"
        )
        raw_temp = array.assign_coords({"time": t})
    if monthly:
        raw_temp = raw_temp.resample(time="MS").mean()
        raw_temp, arr = xr.align(raw_temp, arr)
        month_mean = raw_temp.groupby("time.month").mean("time")
        return arr.groupby("time.month") - month_mean + core.config.MEANS["TREFHT"]
    day_mean = raw_temp.groupby("time.dayofyear").mean()
    raw_temp, arr = xr.align(raw_temp, arr)
    return arr.groupby("time.dayofyear") - day_mean + core.config.MEANS["TREFHT"]


def _gao_remove_decay_in_forcing(
    frc: np.ndarray, y: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    new_frc = np.zeros_like(frc)
    limit = 2e-6
    place_here = 1
    for i, v in enumerate(frc[1:]):
        if frc[i - 1] < v and v > limit and frc[i - 1] < limit:
            new_frc[i + place_here] = v
        if new_frc[i + place_here - 1] > limit and v > new_frc[i + place_here - 1]:
            new_frc[i + place_here - 1] = 0
            new_frc[i + place_here] = v
    # Go from monthly to daily (this is fine as long as we use a spiky forcing). We
    # start in December.
    new_frc = _month2day(new_frc, start=12)
    # The new time axis now goes down to one day
    y = np.linspace(501, 2002, (2002 - 501) * 365 + 1)
    y = y[: len(new_frc)]
    return new_frc, y


def _month2day(
    arr: np.ndarray,
    start: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] = 1,
) -> np.ndarray:
    # Go from monthly to daily
    newest = np.array([])
    # Add 30, 29 or 27 elements between all elements: months -> days
    days_ = (30, 27, 30, 29, 30, 29, 30, 30, 29, 30, 29, 30)
    days = itertools.cycle(days_)
    for _ in range(start - 1):
        next(days)
    for month in arr:
        insert_ = np.zeros(next(days))
        newest = np.r_[newest, np.array([month])]
        newest = np.r_[newest, insert_]
    # The new time axis now goes down to one day
    return newest


def _get_so2_ob16_full_timeseries() -> tuple[np.ndarray, np.ndarray]:
    """Load the npz file with volcanic injection.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Arrays containing time and value of SO2 peaks

    Raises
    ------
    FileNotFoundError
        If the volcanic forcing file is not found.
    """
    file = "IVI2LoadingLatHeight501-2000_L18_c20100518.nc"
    if not (fn := core.config.DATA_DIR_ROOT / "cesm-lme" / file).exists():
        raise FileNotFoundError(
            f"Cannot find {fn.resolve()}. Try running the `save_to_npz` function inside"
            f" {__name__}."
        )
    ds = xr.open_dataset(core.config.DATA_DIR_ROOT / "cesm-lme" / file)
    da: xr.DataArray = ds.colmass
    year = ds.time.data
    avgs_list = core.utils.time_series.mean_flatten(da, dims=["lat"], operation="mean")
    avgs = avgs_list.data
    # Scale so that the unit is now in Tg (Otto-Bliesner et al. (2016)). (Tg of what?
    # Volcanic sulfate aerosol (H2SO4), which has atomic mass of 4+32+16*4 = 100,
    # whereas SO2 has atomic mass of 32+16*2 = 64. So we divide by 100/64 = 1.5625.)
    avgs = avgs / avgs.max() * 257.9 / 50 * 32
    return year, avgs


def _get_so2_ob16() -> xr.DataArray:
    """Load in mean stratospheric volcanic sulfate aerosol injections.

    Returns
    -------
    xr.DataArray
        The stratospheric sulfate injections used as forcing in the CESM LME
        simulations.

    Notes
    -----
    The data is from Gao et al. (2008) `data
    <http://climate.envsci.rutgers.edu/IVI2/>`_, and was used as input to the model
    simulations by Otto-Bliesner et al. (2017).
    """
    y, g = _get_so2_ob16_full_timeseries()
    y = y - y[0] + 501
    g, y = _gao_remove_decay_in_forcing(g, y)
    freq = "D"
    da = xr.DataArray(
        g,
        dims=["time"],
        coords={"time": core.utils.time_series.float2dt(y, freq)},
        name="Mean stratospheric volcanic sulfate aerosol injections [Tg]",
    )
    da = da.assign_coords(time=da.time.data + datetime.timedelta(days=14))
    return da


def get_ob16() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return Otto-Bliesner et al. 2016 SO2, RF and temperature peaks.

    The peaks are best estimates from the full time series.

    Returns
    -------
    tuple[np.ndarray, np.ndarray, np.ndarray]
        SO2 peaks, RF peaks and temperature peaks
    """
    # Temperature
    ds, temp_ = _get_ob16_rf_temp_arrays()
    temp_xr = core.utils.time_series.get_median(temp_, xarray=True)
    # Seasonality is removed by use of a control run temperature time series, where we
    # compute a climatology mean for each day of the year which is subtracted from the
    # time series.
    # temp_xr = temp_xr.assign_coords(time=core.utils.time_series.float2dt(temp_xr.time.data))
    temp_xr = _remove_seasonality_ob16(temp_xr)
    # Adjust the temperature so its mean is at zero, and fluctuations are positive. We
    # also remove a slight drift by means of a linear regression fit.
    temp_xr *= -1
    x_ax = core.utils.time_series.dt2float(temp_xr.time.data)
    temp_lin_reg = scipy.stats.linregress(x_ax, temp_xr.data)
    temp_xr.data -= x_ax * temp_lin_reg.slope + temp_lin_reg.intercept

    # Add RF from the FSNTOA variable (daily) ---------------------------------------- #
    # We load in the original FSNTOA 5 member ensemble and compute the ensemble mean.
    rf = core.utils.time_series.get_median(ds, xarray=True)
    # Remove noise in Fourier domain (seasonal and 6-month cycles)
    rf_fr = core.utils.time_series.remove_seasonality([rf.copy()])[0]
    rf_fr = core.utils.time_series.remove_seasonality([rf_fr], freq=2)[0]
    # Subtract the mean and flip
    rf_fr.data -= rf_fr.data.mean()
    rf_fr.data *= -1

    so2_start = _get_so2_ob16()
    # A 210 days shift forward give the best timing of the temperature peak and 150
    # days forward give the timing for the radiative forcing peak. A 190 days shift
    # back give the best timing for when the temperature and radiative forcing
    # perturbations start (eruption day). Done by eye measure.
    d1, d2, d3 = 190, 150, 210
    so2_start = so2_start.assign_coords(
        time=so2_start.time.data - datetime.timedelta(days=d1)
    )
    so2_rf_peak = so2_start.assign_coords(
        time=so2_start.time.data + datetime.timedelta(days=d2)
    )
    so2_temp_peak = so2_start.assign_coords(
        time=so2_start.time.data + datetime.timedelta(days=d3)
    )

    so2_start, so2_rf_peak, so2_temp_peak, rf_fr, temp = xr.align(
        so2_start, so2_rf_peak, so2_temp_peak, rf_fr, temp_xr
    )

    if not len(so2_start) % 2:
        so2_start = so2_start[:-1]
        so2_rf_peak = so2_rf_peak[:-1]
        so2_temp_peak = so2_rf_peak[:-1]
        rf_fr = rf_fr[:-1]
        temp = temp[:-1]
    _cesm_lme_so2_start = so2_start
    _cesm_lme_so2_rf_peak = so2_rf_peak
    _cesm_lme_so2_temp_peak = so2_temp_peak
    _cesm_lme_rf = rf_fr
    _cesm_lme_temp = temp
    # Mask out all non-zero forcing values, and the corresponding temperature values.
    _idx_rf = np.argwhere(so2_rf_peak.data > 0)
    _idx_temp = np.argwhere(so2_temp_peak.data > 0)
    so2 = so2_rf_peak.data[_idx_rf].flatten()
    rf_v = rf_fr.data[_idx_rf].flatten()
    temp_v = temp.data[_idx_temp].flatten()
    _ids = so2.argsort()
    return so2[_ids], rf_v[_ids], temp_v[_ids]


if __name__ == "__main__":
    save_to_npz()
