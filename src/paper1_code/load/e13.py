"""Load English et al. (2013) data.

Notes
-----
See https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1002/jgrd.50196 for the full
paper.
"""


def get_so2_e13() -> tuple[float, float, float]:
    """Based on the paper by English et al. (2013)."""
    return 20, 200, 2000


def get_aod_e13() -> tuple[float, float, float]:
    """Based on the paper by English et al. (2013)."""
    return 0.13, 0.6, 2.6
