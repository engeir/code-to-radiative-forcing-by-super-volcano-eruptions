"""Load McGraw et al. (2024) data.

Notes
-----
See https://doi.org/10.1175/JCLI-D-23-0116.1 for the full paper. Data can be downloaded
at a TXT-file.
"""


def get_so2_mcg24() -> tuple[float, float, float, float, float, float]:
    """Based on the paper by McGraw et al. (2024)."""
    return (
        18,
        100,
        200,
        400,
        1000,
        2000,
    )


def get_rf_mcg24() -> tuple[float, float, float, float, float, float]:
    """Based on the paper by McGraw et al. (2024)."""
    return (
        2.17,
        10.69,
        19.5,
        32.97,
        51.51,
        61.53,
    )


def get_trefht_mcg24() -> tuple[float, float, float, float, float, float]:
    """Based on the paper by McGraw et al. (2024)."""
    return (
        0.47,
        1.37,
        2.61,
        4.59,
        7.46,
        9.63,
    )
