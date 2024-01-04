"""When saving figures, this is how the setup is handled."""

import pathlib

import paper1_code as core


def create_savedir() -> pathlib.Path:
    """Create the directory where the figures will be saved."""
    SAVE_PATH = core.config.DATA_DIR_OUT
    if not SAVE_PATH.exists():
        SAVE_PATH.mkdir(parents=True)
    return SAVE_PATH
