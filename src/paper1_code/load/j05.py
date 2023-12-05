"""Load Jones et al. (2005) data."""

# FIXME: add doi.


def get_so2_j05() -> float:
    """Based on the paper by Jones et al. (2005).

    The SO2 is described to last over some time, thus the value set here might be
    too low when compared to a "total SO2 injected" value. (Bottom of page 726,
    section 3 Validity of approach).

    Notes
    -----
    DOI: 10.1007/s00382-005-0066-8
    """
    return 1400


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


def get_trefht_j05() -> float:
    """Based on the paper by Jones et al. (2005).

    Notes
    -----
    DOI: 10.1007/s00382-005-0066-8
    """
    return 10.7
