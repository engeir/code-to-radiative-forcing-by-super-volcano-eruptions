"""Handy functions that don't have a natural home."""

import datetime
import warnings

import cftime
import matplotlib as mpl
from matplotlib.patches import ConnectionPatch


def d2n(date: datetime.datetime | str) -> float:
    """Convert a datetime to a number, using 2000-01-01 as the reference date.

    Parameters
    ----------
    date : datetime.datetime | str
        If a string, it must be on the format `YYYY-MM-DD`, otherwise use a
        `datetime.datetime` object.

    Returns
    -------
    float
        The float representation of the date.

    Raises
    ------
    ValueError
        If the string representation is in an unknown format.
    """
    if isinstance(date, str):
        date_fmt = 3
        if len(out := date.split("-")) != date_fmt:
            msg = "The datetime to float function expect strings as YYYY-MM-DD."
            raise ValueError(msg)
        y, m, d = int(out[0]), int(out[1]), int(out[2])
        date = datetime.datetime(y, m, d, 0, 0, tzinfo=datetime.UTC)
    unit = "days since 2000-01-01"
    return cftime.date2num(date, units=unit, calendar="noleap", has_year_zero=True)


def n_significant(number: float | str, significance: int) -> str:
    """Return the number to `n` significant digits."""
    number = str(number)
    if "." not in number:
        warnings.warn("This function is only meant for decimal numbers.", stacklevel=2)
        return number
    if number.startswith("-"):
        sign = "-"
        number = number[1:]
    else:
        sign = ""
    decimals = significance + 1 if number.startswith("0.") else significance
    while (
        len(number.replace(".", "")) > significance
        and len(number.replace("0.", "")) > significance
    ):
        number = f"{float(number):.{decimals}f}"
        decimals -= 1
    return sign + number


def create_axes_inset(
    ax: mpl.axes.Axes,
    data_enclosed: tuple[float, float, float, float],
    inset_placement: tuple[float, float, float, float],
    *connecting_edges: str,
) -> mpl.axes.Axes:
    """Create an inset axes object, with optional arbitrary connection lines.

    Parameters
    ----------
    ax : mpl.axes.Axes
        The main axes to create an inset inside.
    data_enclosed : tuple[float, float, float, float]
        The data that should be included in the new inset, in data point units. The
        positions are given as ``x1``, ``x2``, ``y1``, ``y2``.
    inset_placement : tuple[float, float, float, float]
        The placement of the inset axes within ``ax``, in relative units [0, 1]. The
        positions are given as ``x1``, ``y1``, ``width``, ``height``.
    *connecting_edges : str
        Any number of lines specified by the corners they should connect. The
        strings must be composed on the form ``START->END``, where both START and
        END can be any of "ll" (lower left), "lr" (lower right), "ul" (upper left)
        or "ur" (upper right), for example ``lr->lr`` or ``lr->ul``.

    Returns
    -------
    mpl.axes.Axes
        The new inset axes object.
    """
    x0, y0, width, height = inset_placement
    x1, x2, y1, y2 = data_enclosed
    rect = (x1, y1, x2 - x1, y2 - y1)
    ax1 = ax.inset_axes((x0, y0, width, height), xlim=(x1, x2), ylim=(y1, y2))
    ax.indicate_inset(rect, edgecolor="grey", alpha=0.5, lw=0.7)
    for edge in connecting_edges:
        start, end = edge.split("->")
        match start:
            case "ll":
                start_ = (x1, y1)
            case "lr":
                start_ = (x2, y1)
            case "ul":
                start_ = (x1, y2)
            case "ur":
                start_ = (x2, y2)
        match end:
            case "ll":
                end_ = (0, 0)
            case "lr":
                end_ = (1, 0)
            case "ul":
                end_ = (0, 1)
            case "ur":
                end_ = (1, 1)
        cp = ConnectionPatch(
            xyA=start_,
            xyB=end_,
            axesA=ax,
            axesB=ax1,
            coordsA="data",
            coordsB="axes fraction",
            color="grey",
            lw=0.7,
            alpha=0.5,
        )
        ax.add_patch(cp)
    return ax1
