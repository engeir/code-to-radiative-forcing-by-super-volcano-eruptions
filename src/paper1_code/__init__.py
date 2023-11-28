"""Init file for the main package."""

import matplotlib as mpl
from importlib_metadata import version

from paper1_code import config, utils

__all__ = ["utils", "config"]

__version__ = version(__package__)

mpl.style.use("cosmoplots.default")
