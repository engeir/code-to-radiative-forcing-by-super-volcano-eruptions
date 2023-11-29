"""When saving figures, this is how the setup is handled."""

import pathlib


def create_savedir() -> pathlib.Path:
    """Create the directory where the figures will be saved."""
    HERE = pathlib.Path(__file__)
    next = False
    for parents in HERE.parents:
        if next:
            SAVE_PATH = parents / "generated_files"
            break
        if parents.name == "src":
            next = True
    if not SAVE_PATH.exists():
        SAVE_PATH.mkdir(parents=True)
    return SAVE_PATH
