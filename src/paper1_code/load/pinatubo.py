"""Load Mt. Pinatubo data.

Notes
-----
See the individual functions for sources.
"""


def get_so2_pinatubo() -> float:
    """Get SO2 injected values based on observational data.

    This range between 10 to 17 Tg (Sukhodolov, 2018) (values used in models that
    capture well the temperature response), but others report about 18 Tg (Guo et
    al., 2004; Toohey and Sigl, 2017) (value obtained from observational analysis).
    """
    return 18


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


def get_trefht_pinatubo() -> float:
    """Based on the paper by Hansen et al. (1999).

    The GISS paper is an analysis of surface temperature between 1880 and 1999 based
    on observational data, primarily based on meteorological station measurements.
    See for example figure 7.

    Notes
    -----
    DOI: 10.1029/1999JD900835
    """
    return 0.5
