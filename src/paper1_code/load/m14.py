"""Load Load Metzner et al. (2014) data.

Notes
-----
See the individual functions for sources.
"""

import matplotlib.pyplot as plt
import numpy as np

# fmt: off
cava = {
  "SMT*": {"age": 0.1, "so2": 3.07, "msl": 4.70, "md": 5.87, "aod": 0.039, "rf": -0.94},
  "1835": {"age": 0.17, "so2": 0.64, "msl": 0.98, "md": 1.22, "aod": 0.008, "rf": -0.20},
  "TBJ": {"age": 1.55, "so2": 15.65, "msl": 23.94, "md": 29.93, "aod": 0.165, "rf": -3.96},
  "MT": {"age": 1.8, "so2": 9.36, "msl": 14.32, "md": 17.90, "aod": 0.109, "rf": -2.61},
  "CT": {"age": 1.9, "so2": 35.33, "msl": 54.05, "md": 67.57, "aod": 0.304, "rf": -7.29},
  "MTL": {"age": 2.1, "so2": 6.54, "msl": 10.01, "md": 12.51, "aod": 0.080, "rf": -1.91},
  "RBT": {"age": 3.5, "so2": 1.75, "msl": 2.68, "md": 3.35, "aod": 0.022, "rf": -0.54},
  "MAT": {"age": 4, "so2": 2.36, "msl": 3.61, "md": 4.51, "aod": 0.030, "rf": -0.72},
  "SAT": {"age": 6, "so2": 43.74, "msl": 66.92, "md": 83.65, "aod": 0.355, "rf": -8.51},
  "XT": {"age": 6.1, "so2": 0.46, "msl": 0.70, "md": 0.88, "aod": 0.006, "rf": -0.14},
  "LHP": {"age": 10, "so2": 0.36, "msl": 0.55, "md": 0.69, "aod": 0.005, "rf": -0.11},
  "UAQ*": {"age": 12.4, "so2": 1.46, "msl": 2.23, "md": 2.79, "aod": 0.019, "rf": -0.45},
  "UCT": {"age": 15, "so2": 1.29, "msl": 1.97, "md": 2.47, "aod": 0.017, "rf": -0.39},
  "LAQ": {"age": 17, "so2": 1.99, "msl": 3.04, "md": 3.81, "aod": 0.025, "rf": -0.61},
  "UOT": {"age": 19, "so2": 4.30, "msl": 6.58, "md": 8.22, "aod": 0.053, "rf": -1.28},
  "LCT": {"age": 20, "so2": 0.75, "msl": 1.15, "md": 1.43, "aod": 0.010, "rf": -0.23},
  "PAT": {"age": 23, "so2": 2.01, "msl": 3.08, "md": 3.84, "aod": 0.026, "rf": -0.62},
  "UAT*": {"age": 24.5, "so2": 44.56, "msl": 68.18, "md": 85.22, "aod": 0.359, "rf": -8.62},
  "LAT": {"age": 24.8, "so2": 2.15, "msl": 3.29, "md": 4.11, "aod": 0.028, "rf": -0.66},
  "TB4": {"age": 36, "so2": 7.15, "msl": 10.94, "md": 13.67, "aod": 0.086, "rf": -2.07},
  "MXT": {"age": 39, "so2": 1.70, "msl": 2.60, "md": 3.25, "aod": 0.022, "rf": -0.52},
  "IFT*": {"age": 40, "so2": 0.42, "msl": 0.64, "md": 0.80, "aod": 0.005, "rf": -0.13},
  "PY1": {"age": 50, "so2": 0.19, "msl": 0.29, "md": 0.36, "aod": 0.002, "rf": -0.06},
  "CFT": {"age": 50, "so2": 0.35, "msl": 0.54, "md": 0.67, "aod": 0.004, "rf": -0.11},
  "CCT": {"age": 51, "so2": 4.1, "msl": 6.27, "md": 7.84, "aod": 0.051, "rf": -1.22},
  "EFT*": {"age": 51, "so2": 18.35, "msl": 28.08, "md": 35.09, "aod": 0.186, "rf": -4.47},
  "CGT": {"age": 53, "so2": 39.71, "msl": 60.76, "md": 75.95, "aod": 0.331, "rf": -7.94},
  "FT": {"age": 60, "so2": 2.88, "msl": 4.41, "md": 5.51, "aod": 0.037, "rf": -0.88},
  "TTA": {"age": 61, "so2": 3.92, "msl": 6.00, "md": 7.50, "aod": 0.050, "rf": -1.20},
  "UT": {"age": 70, "so2": 0.21, "msl": 0.32, "md": 0.40, "aod": 0.003, "rf": -0.06},
  "ACT": {"age": 72, "so2": 19.41, "msl": 29.70, "md": 37.12, "aod": 0.195, "rf": -4.67},
  "BRT": {"age": 75, "so2": 2.36, "msl": 3.61, "md": 4.51, "aod": 0.030, "rf": -0.72},
  "LCY*": {"age": 84, "so2": 686.59, "msl": 1050.48, "md": 1313.10, "aod": 2.370, "rf": -56.89},
  "TFT": {"age": 119, "so2": 49.54, "msl": 75.80, "md": 94.75, "aod": 0.388, "rf": -9.30},
  "WFT": {"age": 158, "so2": 14.81, "msl": 22.66, "md": 28.32, "aod": 0.158, "rf": -3.79},
  "LFT": {"age": 191, "so2": 46.78, "msl": 71.57, "md": 89.47, "aod": 0.372, "rf": -8.93},
}
# fmt: on
simulated: dict[str, dict[str, float | str | list[float]]] = {
    "I-Tephra": {
        "acronym": "IFT",
        "so2": 0.42,
        "aod": 0.0058,
        "rf_p": [5.43e-02, 5.76e-02, 1.93e-02],
        "rf_m": [6.83e-02, 1.22e-01, 7.31e-02],
        "gmst": 0.013,
    },
    "U. Apoyeque Pumice": {
        "acronym": "UAQ",
        "so2": 1.46,
        "aod": 0.02,
        "rf_p": [1.88e-01, 1.99e-01, 6.69e-02],
        "rf_m": [2.36e-01, 3.86e-01, 1.66e-01],
        "gmst": 0.04,
    },
    "Santa Maria": {
        "acronym": "SMT",
        "so2": 3.07,
        "aod": 0.042,
        "rf_p": [3.92e-01, 4.16e-01, 1.40e-01],
        "rf_m": [5.08e-01, 7.86e-01, 2.84e-01],
        "gmst": 0.08,
    },
    "E-Fall": {
        "acronym": "EFT",
        "so2": 18.35,
        "aod": 0.21,
        "rf_p": [1.87e00, 1.98e00, 6.65e-01],
        "rf_m": [2.50e00, 3.36e00, 8.99e-01],
        "gmst": 0.38,
    },
    "U. Apoyo Tephra": {
        "acronym": "UAT",
        "so2": 44.56,
        "aod": 0.4,
        "rf_p": [3.60e00, 3.82e00, 1.28e00],
        "rf_m": [4.70e00, 5.40e00, 1.36e00],
        "gmst": 0.63,
    },
    "hypothetical": {
        "acronym": "170 Mt",
        "so2": 170.00,
        "aod": 0.8,
        "rf_p": [9.19e00, 9.75e00, 3.27e00],
        "rf_m": [9.62e00, 7.11e00, 1.70e00],
        "gmst": 1.0,
    },
    "Los Chocoyos": {
        "acronym": "LCY",
        "so2": 686.59,
        "aod": 2.1,
        "rf_p": [2.37e01, 2.52e01, 8.46e00],
        "rf_m": [2.76e01, 1.05e01, 1.80e00],
        "gmst": 2.1,
    },
}


def get_so2_m14() -> tuple[float, ...]:
    """Based on the paper by Metzner et al. (2014).

    The SO2 is described to last over some time, thus the value set here might be
    too low when compared to a "total SO2 injected" value. (Bottom of page 726,
    section 3 Validity of approach).

    Notes
    -----
    DOI: 10.1007/s00531-012-0814-z
    """
    return tuple(f["so2"] for f in simulated.values() if isinstance(f["so2"], float))


def _get_cava_so2() -> list[float]:
    return [f["so2"] for f in cava.values()]


def get_aod_m14() -> tuple[float, ...]:
    """Based on the paper by Metzner et al. (2014).

    Notes
    -----
    DOI: 10.1007/s00531-012-0814-z
    """
    return tuple(f["aod"] for f in simulated.values() if isinstance(f["aod"], float))


def _get_cava_aod() -> list[float]:
    return [f["aod"] for f in cava.values()]


def get_rf_m14() -> tuple[float, ...]:
    """Top-of-atmosphere radiative imbalance due to Mount Pinatubo, times 100.

    See Metzner et al. (2014).
    """
    return tuple(
        max(f["rf_m"]) for f in simulated.values() if isinstance(f["rf_m"], list)
    )


def _get_cava_rf() -> list[float]:
    return [f["rf"] for f in cava.values()]


def get_trefht_m14() -> tuple[float, ...]:
    """Based on the paper by Metzner et al. (2014).

    Notes
    -----
    DOI: 10.1007/s00531-012-0814-z
    """
    return tuple(f["gmst"] for f in simulated.values() if isinstance(f["gmst"], float))


def _view_cava() -> None:
    plt.figure()
    plt.suptitle("SO2-AOD")
    plt.scatter(
        ((1.91 * np.asarray(_get_cava_so2())) ** (2 / 3) * 0.02 - 0.028)
        / np.asarray(_get_cava_aod()),
        _get_cava_aod(),
    )
    plt.figure()
    plt.suptitle("SO2-RF")
    plt.scatter(_get_cava_so2(), np.asarray(_get_cava_aod()))
    plt.figure()
    plt.suptitle("AOD-RF")
    plt.scatter(
        _get_cava_aod(), np.asarray(_get_cava_rf()) / -24 / np.asarray(_get_cava_aod())
    )
    plt.show()


if __name__ == "__main__":
    _view_cava()
