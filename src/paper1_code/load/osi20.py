"""Load Osipov et al. (2020) data.

Notes
-----
See https://doi.org/10.1029/2019JD031726 for the full paper.
"""


def get_so2_osi20() -> tuple[float, float, float, float, float]:
    """Based on the paper by Osipov et al. (2020)."""
    return 2000, 2000, 2000, 2000, 2000


def get_aod_osi20() -> tuple[float, float, float, float, float]:
    """Based on the paper by Osipov et al. (2020)."""
    return 4.2, 5, 4.8, 4.8, 10.5


def get_trefht_osi20() -> tuple[float, float, float, float, float]:
    """Based on the paper by Osipov et al. (2020)."""
    return 5.6, 5.6, 5.6, 5.9, 10.5
