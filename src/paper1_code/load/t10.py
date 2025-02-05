"""Load Timmreck et al. 2010 data.

Notes
-----
See https://doi.org/10.1029/2010GL045464 for the full paper.
"""


def get_so2_t10() -> float:
    """Based on the paper by Timmreck et al. (2010).

    Actually, it is the YTT (Young Toba Tuff).

    Notes
    -----
    DOI: 10.1029/2010GL045464
    """
    return 850 * 2


def get_aod_t10() -> float:
    """Based on the paper by Timmreck et al. (2010).

    Actually, it is the YTT (Young Toba Tuff).

    Notes
    -----
    DOI: 10.1029/2010GL045464
    """
    # A factor of 3-5 smaller than the Jones et al. 2005 SAOD peak
    # 15 / 3.5 = 4.2857142857143
    return 4.286


def get_rf_t10() -> float:
    """Top-of-atmosphere radiative imbalance due to Mount Pinatubo, times 100.

    Actually, it is the YTT (Young Toba Tuff).

    See Timmreck et al. (2010).
    """
    return 18


def get_trefht_t10() -> float:
    """Based on the paper by Jones et al. (2005).

    Notes
    -----
    DOI: 10.1007/s00382-005-0066-8
    """
    return 3.5
