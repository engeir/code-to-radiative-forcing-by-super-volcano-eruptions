"""Init file for the main package."""

from importlib_metadata import version

from paper1_code import config, utils

__all__ = ["utils", "config"]

__version__ = version(__package__)
