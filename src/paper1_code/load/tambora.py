"""Load Mt. Tambora data."""


def get_so2_tambora() -> float:
    """Get the SO2 injection used in VolMIP volc-long-eq for the Tambora eruption.

    See
    https://view.es-doc.org/index.html?renderMethod=id&project=cmip6&id=fc04f8eb-feff-4fa4-ba91-41cf9041a2ef&version=1
    """
    return 56.2


def get_aod_tambora() -> float:
    """From EVAv1.2(eVolv2k), Tambora 1815, Toohey and Sigl (2017).

    Notes
    -----
    Download data from https://www.wdc-climate.de/ui/entry?acronym=eVolv2k_v3.
    """
    return 0.355


def get_rf_tambora() -> float:
    """From Raible et al. (2016), p. 573.

    Notes
    -----
    https://doi.org/10.1002/wcc.407
    """
    return 5


def get_trefht_tambora() -> float:
    """From Raible et al. (2016) or Marshall et al. (2018).

    Notes
    -----
    Based on two simulations from the VolMIP ensemble, 1.5 K is also realistic.
    """
    return 1
