"""Data that is used in several figures are loaded here."""

import xarray as xr

import paper1_code as core

FINDER = core.utils.load_auto.FindFiles()


def _set_aod_arrs(shift: int | None = None) -> tuple[list[xr.DataArray], ...]:
    control_match = FINDER.find("e_fSST1850", "control", "AODVISstdn", "h0", "ens0")
    control = control_match.load()
    control = core.utils.time_series.mean_flatten(control, dims=["lat", "lon"])

    def remove_control(arrs: list) -> list:
        # The control is so small it hardly has any effect, but we do it still for
        # consistency
        for i, arr in enumerate(arrs):
            arr_, ctrl = xr.align(arr, control[0])
            arr_.data = arr_.data - ctrl.data
            arrs[i] = arr_
        return arrs

    data = FINDER.find(
        "e_fSST1850",
        {f"ens{i+1}" for i in range(4)},
        {"strong", "medium", "medium-plus", "strong-highlat"},
        "AODVISstdn",
        "h0",
    ).sort("attr", "ensemble")
    m = data.copy().keep("medium").load()
    mp = data.copy().keep("medium-plus").load()
    s = data.copy().keep("strong").load()
    h = data.copy().keep("strong-highlat").load()

    s = core.utils.time_series.mean_flatten(s, dims=["lat", "lon"])
    m = core.utils.time_series.mean_flatten(m, dims=["lat", "lon"])
    mp = core.utils.time_series.mean_flatten(mp, dims=["lat", "lon"])
    h = core.utils.time_series.mean_flatten(h, dims=["lat", "lon"])
    s = remove_control(s)
    m = remove_control(m)
    mp = remove_control(mp)
    h = remove_control(h)
    h_shift = 12 if shift is None else 0
    s = core.utils.time_series.shift_arrays(s, daily=False, custom=shift)
    mp = core.utils.time_series.shift_arrays(mp, daily=False, custom=shift)
    m = core.utils.time_series.shift_arrays(m, daily=False, custom=shift)
    h = core.utils.time_series.shift_arrays(h, custom=h_shift)
    h = core.utils.time_series.shift_arrays(h, daily=False, custom=shift)
    for i, arr in enumerate(s):
        s[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(mp):
        mp[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(m):
        m[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(h):
        h[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    m = list(xr.align(*m))
    mp = list(xr.align(*mp))
    s = list(xr.align(*s))
    h = list(xr.align(*h))
    return m, mp, s, h


def _set_rf_arrs(shift: int | None = None) -> tuple[list[xr.DataArray], ...]:
    control_data = FINDER.find(
        "e_fSST1850", "ens0", "control", "h0", ["FLNT", "FSNT"]
    ).sort("attr", "ensemble")
    control = control_data.load()
    control = core.utils.time_series.mean_flatten(control, dims=["lat", "lon"])

    def difference_and_remove_control(arrs: list) -> list:
        stop = len(arrs) // 2
        for i, arr in enumerate(arrs):
            if i > stop - 1:
                arrs = arrs[:stop]
                break
            fsnt, flnt, ctrl_fsnt, ctrl_flnt = xr.align(
                arrs[i + stop], arr, control[1], control[0]
            )
            flnt.data = fsnt.data - flnt.data - (ctrl_fsnt.data - ctrl_flnt.data)
            flnt = flnt.assign_attrs(attr="RF")
            arrs[i] = flnt
        return arrs

    data = FINDER.find(
        "e_fSST1850",
        {f"ens{i+1}" for i in range(4)},
        {"strong", "medium", "medium-plus", "strong-highlat"},
        {"FLNT", "FSNT"},
        "h0",
    ).sort("attr", "ensemble")
    m_ = data.copy().keep("medium").load()
    mp_ = data.copy().keep("medium-plus").load()
    s_ = data.copy().keep("strong").load()
    h_ = data.copy().keep("strong-highlat").load()
    s_ = core.utils.time_series.mean_flatten(s_, dims=["lat", "lon"])
    m_ = core.utils.time_series.mean_flatten(m_, dims=["lat", "lon"])
    mp_ = core.utils.time_series.mean_flatten(mp_, dims=["lat", "lon"])
    h_ = core.utils.time_series.mean_flatten(h_, dims=["lat", "lon"])
    # Find difference and subtract control
    s_ = difference_and_remove_control(s_)
    m_ = difference_and_remove_control(m_)
    mp_ = difference_and_remove_control(mp_)
    h_ = difference_and_remove_control(h_)
    h_shift = 12 if shift is None else 0
    s_ = core.utils.time_series.shift_arrays(s_, daily=False, custom=shift)
    mp_ = core.utils.time_series.shift_arrays(mp_, daily=False, custom=shift)
    m_ = core.utils.time_series.shift_arrays(m_, daily=False, custom=shift)
    h_ = core.utils.time_series.shift_arrays(h_, custom=h_shift)
    h_ = core.utils.time_series.shift_arrays(h_, daily=False, custom=shift)
    for i, arr in enumerate(s_):
        s_[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(mp_):
        mp_[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(m_):
        m_[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    for i, arr in enumerate(h_):
        h_[i] = arr.assign_coords(time=core.utils.time_series.dt2float(arr.time.data))
    return m_, mp_, s_, h_
