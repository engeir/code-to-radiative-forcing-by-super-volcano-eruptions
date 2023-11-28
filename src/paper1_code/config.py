"""Configuration file for `ensemble_run_analysis`."""

import pathlib
from typing import Literal

HOME = pathlib.Path().home()
DATA_DIR_ROOT = (
    pathlib.Path("/media") / "een023" / "LaCie" / "een023" / "cesm" / "model-runs"
)

# Means are found by calculating the mean of the control runs:
## TREFHT = era.pre_made.control_trefht()[0].mean()
MEANS: dict[Literal["TREFHT", "AEROD_v"], float] = {
    "TREFHT": 287.37903283,
    "AEROD_v": 0.11947094220873525,
}
DATA_ATTRS = [
    "TREFHT850forcing-control",
    "TREFHTB1850C5CN",
    "TREFHT-full",
    "FSNTOA-full",
    "AODVISstdn",
    "LWCF-full",
    "FLUT-full",
    "SWCF-full",
    "AODDUST",
    "ICEFRAC",
    "AEROD_v",
    "FSNTOA",
    "AODVIS",
    "TREFHT",
    "so4_a1",
    "so4_a2",
    "so4_a3",
    "TROP_P",
    "TMSO2",
    "FLUT",
    "FLNT",
    "FSNT",
    "FLNS",
    "LWCF",
    "SWCF",
    "FUL",
    "FDL",
    "FUS",
    "FDS",
    "SO2",
    "SST",
    "T",
    "U",
]
DATA_ATTRS_EXTRA = {
    "TREFHT850forcing-control": ["Reference height temperature", "K"],
    "TREFHTB1850C5CN": ["Reference height temperature", "K"],
    "TREFHT-full": ["Reference height temperature", "K"],
    "FSNTOA-full": ["Net solar flux at top of atmosphere", "W/m2"],
    "AODVISstdn": ["Stratospheric aerosol optical depth 550 nm day night", "1"],
    "LWCF-full": ["Longwave cloud forcing", "W/m2"],
    "FLUT-full": ["Upwelling longwave flux at top of model", "W/m2"],
    "SWCF-full": ["Shortwave cloud forcing", "W/m2"],
    "AODDUST": ["Aerosol optical depth 550 nm from dust day only", "1"],
    "ICEFRAC": ["Fraction of surface area covered by sea-ice", "fraction"],
    "AEROD_v": ["Total Aerosol Optical Depth in visible band", "1"],
    "FSNTOA": ["Net solar flux at top of atmosphere", "W/m2"],
    "AODVIS": ["Aerosol optical depth 550 nm day only", "1"],
    "TREFHT": ["Reference height temperature", "K"],
    "so4_a1": ["so4_a1 concentration", "kg/kg"],
    "so4_a2": ["so4_a2 concentration", "kg/kg"],
    "so4_a3": ["so4_a3 concentration", "kg/kg"],
    "TROP_P": ["Tropopause Pressure", "Pa"],
    "TMSO2": ["SO2 burden", "Tg"],
    "FLUT": ["Upwelling longwave flux at top of model", "W/m2"],
    "FLNT": ["Net longwave flux at top of model", "W/m2"],
    "FSNT": ["Net solar flux at top of model", "W/m2"],
    "FLNS": ["Net longwave flux at surface", "W/m2"],
    "LWCF": ["Longwave cloud forcing", "W/m2"],
    "SWCF": ["Shortwave cloud forcing", "W/m2"],
    "FUL": ["Longwave upward flux", "W/m2"],
    "FDL": ["Longwave downward flux", "W/m2"],
    "FUS": ["Shortwave upward flux", "W/m2"],
    "FDS": ["Shortwave downward flux", "W/m2"],
    "SO2": ["SO2 concentration", "mol/mol"],
    "SST": ["sea surface temperature", "K"],
    "T": ["Temperature", "K"],
    "U": ["Zonal wind", "m/s"],
}
