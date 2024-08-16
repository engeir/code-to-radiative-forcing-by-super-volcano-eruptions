"""Init file for the main package."""

import matplotlib as mpl
from importlib_metadata import version

from paper1_code import config, load, scripts, utils

__all__ = ["utils", "config", "scripts", "load"]

__version__ = version(__package__)

mpl.style.use(
    [
        "https://raw.githubusercontent.com/uit-cosmo/cosmoplots/main/cosmoplots/default.mplstyle",
        "paper1_code.extra",
        "paper1_code.jgr",
    ],
)
mpl.rc("text.latex", preamble=r"\usepackage{amsmath}")
