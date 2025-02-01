"""Load Robock et al. (2009) data.

Notes
-----
See https://doi.org/10.1029/2008JD011652 for the full paper.
"""


def get_so2_r09() -> tuple[float, float, float, float]:
    """Based on the paper by Robock et al. (2009).

    Notes
    -----
    DOI: 10.1029/2008JD011652
    """
    pinatubo = 20
    return 33 * pinatubo, 100 * pinatubo, 300 * pinatubo, 900 * pinatubo


def get_rf_r09() -> tuple[float, float, float, float]:
    """Based on the paper by Robock et al. (2009).

    Notes
    -----
    DOI: 10.1029/2008JD011652
    """
    return 70 - 40, 100 - 70, 130 - 80, 140 - 80


def get_trefht_r09() -> tuple[float, float, float, float]:
    """Based on the paper by Robock et al. (2009).

    Notes
    -----
    DOI: 10.1029/2008JD011652
    """
    return 8, 13.5, 15, 17
