"""Configuration file for `ensemble_run_analysis`."""

import pathlib
import tomllib
from typing import Literal


def create_config() -> pathlib.Path:
    """Create the file where the configuration will be saved."""
    HERE = pathlib.Path(__file__)
    for i, parents in enumerate(HERE.parents):
        if parents.name == "src":
            project_root = HERE.parents[i + 1]
            break
    if not project_root.exists():
        project_root.mkdir(parents=True)
    return project_root


_root = create_config()
_data = _root / "downloaded_files"
_save = _root / "generated_files"
_cfg = _root / "paper1.toml"
if not _cfg.exists():
    with open(_cfg, mode="w") as cfg:
        cfg.write("[paper1-code]\n")
        cfg.write("# Location of the repository\n")
        cfg.write(f'project_root = "{_root}"\n')
        cfg.write("# Location of the data used in analysis scripts\n")
        cfg.write(f'data_path = "{_data}"\n')
        cfg.write("# Location of the saved figures\n")
        cfg.write(f'save_path = "{_save}"')

HOME = pathlib.Path().home()
# https://github.com/python/mypy/issues/16423
with _cfg.open(mode="rb") as cfg:  # type: ignore
    out = tomllib.load(cfg)  # type: ignore
    PROJECT_ROOT = pathlib.Path(out["paper1-code"]["project_root"])
    DATA_DIR_ROOT = pathlib.Path(out["paper1-code"]["data_path"])
    DATA_DIR_OUT = pathlib.Path(out["paper1-code"]["save_path"])
    # data_path = "/media/een023/LaCie/een023/cesm/model-runs"

# Means are found by calculating the mean of the control runs:
## TREFHT = era.pre_made.control_trefht()[0].mean()
MEANS: dict[Literal["TREFHT"], float] = {"TREFHT": 287.37903283}
DATA_ATTRS = {
    "AODVISstdn": ["Stratospheric aerosol optical depth 550 nm day night", "1"],
    "FSNTOA": ["Net solar flux at top of atmosphere", "W/m2"],
    "TREFHT": ["Reference height temperature", "K"],
    "so4_a1": ["so4_a1 concentration", "kg/kg"],
    "so4_a2": ["so4_a2 concentration", "kg/kg"],
    "so4_a3": ["so4_a3 concentration", "kg/kg"],
    "TROP_P": ["Tropopause Pressure", "Pa"],
    "TMSO2": ["SO2 burden", "Tg"],
    "FLUT": ["Upwelling longwave flux at top of model", "W/m2"],
    "FLNT": ["Net longwave flux at top of model", "W/m2"],
    "FSNT": ["Net solar flux at top of model", "W/m2"],
    "FLNS": ["Net longwave flux at surface", "W/m2"],
    "SO2": ["SO2 concentration", "mol/mol"],
    "SST": ["sea surface temperature", "K"],
    "T": ["Temperature", "K"],
    "U": ["Zonal wind", "m/s"],
}

POINTS_DICTS: dict[
    Literal[
        "circle",
        "point",
        "pixel",
        "triangle_down",
        "triangle_up",
        "triangle_left",
        "triangle_right",
        "tri_down",
        "tri_up",
        "tri_left",
        "tri_right",
        "octagon",
        "square",
        "pentagon",
        "plus (filled)",
        "star",
        "hexagon1",
        "hexagon2",
        "plus",
        "x",
        "x (filled)",
        "diamond",
        "thin_diamond",
        "vline",
        "hline",
        "tickleft",
        "tickright",
        "tickup",
        "tickdown",
        "caretleft",
        "caretright",
        "caretup",
        "caretdown",
        "caretleft (centered at base)",
        "caretright (centered at base)",
        "caretup (centered at base)",
        "caretdown (centered at base)",
    ],
    str | int,
] = {
    "point": ".",
    "pixel": ",",
    "circle": "o",
    "triangle_down": "v",
    "triangle_up": "^",
    "triangle_left": "<",
    "triangle_right": ">",
    "tri_down": "1",
    "tri_up": "2",
    "tri_left": "3",
    "tri_right": "4",
    "octagon": "8",
    "square": "s",
    "pentagon": "p",
    "plus (filled)": "P",
    "star": "*",
    "hexagon1": "h",
    "hexagon2": "H",
    "plus": "+",
    "x": "x",
    "x (filled)": "X",
    "diamond": "D",
    "thin_diamond": "d",
    "vline": "|",
    "hline": "_",
    "tickleft": 0,
    "tickright": 1,
    "tickup": 2,
    "tickdown": 3,
    "caretleft": 4,
    "caretright": 5,
    "caretup": 6,
    "caretdown": 7,
    "caretleft (centered at base)": 8,
    "caretright (centered at base)": 9,
    "caretup (centered at base)": 10,
    "caretdown (centered at base)": 11,
}

FONTSIZE = 7
COLOR_DICTS: dict[Literal["accent", "category10", "dark2", "set1"], list] = {
    # Same as palettable.colorbrewer.qualitative.Accent_8.hex_colors
    "accent": [
        "#7fc97f",
        "#beaed4",
        "#fdc086",
        "#ffff99",
        "#386cb0",
        "#f0027f",
        "#bf5b17",
        "#666666",
    ],
    # Same as palettable.tableau.Tableau_10.hex_colors
    "category10": [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
    ],
    # Same as palettable.colorbrewer.qualitative.Dark2_8.hex_colors
    "dark2": [
        "#1b9e77",
        "#d95f02",
        "#7570b3",
        "#e7298a",
        "#66a61e",
        "#e6ab02",
        "#a6761d",
        "#666666",
    ],
    # Same as palettable.colorbrewer.qualitative.Set1_9.hex_colors
    # Also from https://colorbrewer2.org/#type=qualitative&scheme=Set1&n=9
    "set1": [
        "#e41a1c",
        "#377eb8",
        "#4daf4a",
        "#984ea3",
        "#ff7f00",
        "#ffff33",
        "#a65628",
        "#f781bf",
        "#999999",
    ],
}

# fmt: off
_C = COLOR_DICTS["category10"]
_P = POINTS_DICTS
_DATA_TYPES = Literal[
    "P", "P100", "VT", "c2w", "c2wm", "c2wmp", "ob16",
    "c2ws", "c2wss", "c2wn", "greg", "t10", "m20", "m20*"
]
LEGENDS: dict[_DATA_TYPES, dict] = {
    "P": {"c": "#000000", "marker": _P["star"], "s": 35, "zorder": 5, "label": "P"},
    "P100": {"c": _C[6], "marker": _P["square"], "s": 15, "zorder": 5, "label": "J05"},
    "VT": {"c": "#000000", "marker": _P["plus"], "s": 35, "lw":1.5 ,"zorder": 5, "label": "T"},
    "c2w": {"c": _C[0], "marker": _P["diamond"], "ms": 3, "zorder": 4, "label": "C2WTrop"},
    "c2wm": {"c": _C[0], "marker": _P["triangle_down"], "s": 9, "zorder": 3, "label": r"C2W$\downarrow$"},
    "c2wmp": {"c": _C[1], "marker": _P["diamond"], "s": 9, "zorder": 3, "label": r"C2W$-$"},
    "c2ws": {"c": _C[2], "marker": _P["triangle_up"], "s": 9, "zorder": 3, "label": r"C2W$\uparrow$"},
    "c2wss": {"c": _C[6], "marker": _P["caretup"], "s": 9, "zorder": 3, "label": r"C2W$\uparrow\uparrow$"},
    "c2wn": {"c": _C[5], "marker": _P["tri_up"], "s": 35, "zorder": 4, "label": r"C2WN$\uparrow$"},
    "greg": {"c": _C[7], "marker": _P["x"], "s": 9, "zorder": -1, "label": "G16"},
    "t10": {"c": _C[6], "marker": _P["circle"], "s": 15, "zorder": 5, "label": "T10"},
    "m20": {"c": _C[3], "marker": _P["thin_diamond"], "s": 9, "zorder": 6, "label": "M20"},
    "m20*": {"c": _C[3], "marker": _P["thin_diamond"], "s": 15, "zorder": 2, "label": "M20"},
    "ob16": {"c": _C[2], "marker": _P["triangle_down"], "s": 15, "zorder": 4, "label": "OB16"},
}
# fmt: on
