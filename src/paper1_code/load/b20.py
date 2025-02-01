"""Load Brenna et al. (2020) data.

Notes
-----
See https://doi.org/10.5194/acp-20-6521-2020 for the full paper.
"""


def get_so2_b20() -> tuple[float, float]:
    """Based on the paper by Brenna et al. (2020).

    Returns
    -------
    tuple[float, float]
        The LCY_full, LCY_sulf experiments.
    """
    return 1046, 1046


def get_aod_b20() -> tuple[float, float]:
    """Based on the paper by Brenna et al. (2020).

    Returns
    -------
    tuple[float, float]
        The LCY_full, LCY_sulf experiments.
    """
    return 6.3, 8


def get_rf_b20() -> tuple[float, float]:
    """Based on the paper by Brenna et al. (2020).

    Returns
    -------
    tuple[float, float]
        The LCY_full, LCY_sulf experiments.
    """
    return 40, 50


def get_trefht_b20() -> tuple[float, float]:
    """Based on the paper by Brenna et al. (2020).

    Returns
    -------
    tuple[float, float]
        The LCY_full, LCY_sulf experiments.
    """
    return 6.1, 7
