"""Calculate the climate resistance, rho."""

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

import paper1_code as core

DATAFILES = core.utils.find_c2w_files.FindFiles()


def _time_from_eruption_start(arrs: list[xr.DataArray], cut: int = 144) -> list:
    for i, arr in enumerate(arrs):
        arr_ = arr.assign_coords(
            time=core.utils.time_series.dt2float(arr.time.data) - 1850
        )
        arrs[i] = arr_[:cut].dropna("time")
    return arrs


def _temp_sub_mean(arrs: list[xr.DataArray]) -> list:
    for i, arr in enumerate(arrs):
        arr.data -= core.config.MEANS["TREFHT"]
        arrs[i] = arr.compute()
    return arrs


def _find_shortest_end_time(arrs: list[xr.DataArray]) -> None:
    end = 100
    for arr in arrs:
        if arr.time.data[-1] < end:
            end = arr.time.data[-1]
        print(arr.time.data[-1])
    print(f"The shortest end time was {end}")


def _compute_integral_ratio(
    *pairs: tuple[list[xr.DataArray], list[xr.DataArray]],
) -> list[float]:
    ratios = []
    pair_length = 2
    for pair in pairs:
        assert len(pair) == pair_length
        for f, t in zip(pair[0], pair[1], strict=True):
            print(f.attrs["sim"], t.attrs["sim"])
            # Integrate and find the ratio
            f_int = np.trapz(f.data, dx=1 / 12)
            t_int = np.trapz(t.data, dx=1 / 12)
            ratios.append(f_int / t_int)
            print(f_int / t_int)
            print("#" * 50)
    return ratios


def _get_temp_arrays(data) -> tuple[list, list, list]:
    temp = data.copy().keep("e_BWma1850", "TREFHT", {"medium", "medium-plus", "strong"})
    temp_ctrl = data.copy().keep("e_BWma1850", "TREFHT", "control")
    temp_s = temp.copy().keep("strong").load()
    temp_m = temp.copy().keep("medium").load()
    temp_mp = temp.copy().keep("medium-plus").load()
    temp_control = temp_ctrl.load()
    temp_s = core.utils.time_series.mean_flatten(temp_s, dims=["lat", "lon"])
    temp_m = core.utils.time_series.mean_flatten(temp_m, dims=["lat", "lon"])
    temp_mp = core.utils.time_series.mean_flatten(temp_mp, dims=["lat", "lon"])
    temp_control = core.utils.time_series.mean_flatten(
        temp_control, dims=["lat", "lon"]
    )
    # Since we are doing an integral over whole years, subtracting the mean value of a
    # control run should suffice..?
    temp_s = _temp_sub_mean(temp_s)
    temp_m = _temp_sub_mean(temp_m)
    temp_mp = _temp_sub_mean(temp_mp)
    temp_s = core.utils.time_series.shift_arrays(temp_s, daily=False)
    temp_m = core.utils.time_series.shift_arrays(temp_m, daily=False)
    temp_mp = core.utils.time_series.shift_arrays(temp_mp, daily=False)
    temp_s = _time_from_eruption_start(temp_s, cut=int(12 * 20))
    temp_m = _time_from_eruption_start(temp_m, cut=int(12 * 20))
    temp_mp = _time_from_eruption_start(temp_mp, cut=int(12 * 20))
    # temp_control = time_from_eruption_start(temp_control, cut=252)
    [a.plot() for a in temp_m + temp_mp + temp_s]
    return temp_m, temp_mp, temp_s


def _get_forcing_arrays(data) -> tuple[list, list, list]:
    frc = data.copy().keep(
        "e_fSST1850", ("FLNT", "FSNT"), {"strong", "medium", "medium-plus"}
    )
    control = (
        data.copy()
        .keep("e_fSST1850", ("FLNT", "FSNT"), "control", "ens1")
        .sort("attr", "ensemble")
        .load()
    )
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
            arrs[i] = flnt.compute()
        return arrs

    def subtract_last_decade_mean(arrs: list) -> list:
        # Subtract the mean of the last decade
        for i, arr in enumerate(arrs):
            arr_ = arr[-120:]
            arr.data = arr.data - arr_.mean().data
            arrs[i] = arr
        return arrs

    s_ = frc.copy().keep("strong").sort("attr", "ensemble").load()
    m_ = frc.copy().keep("medium").sort("attr", "ensemble").load()
    mp_ = frc.copy().keep("medium-plus").sort("attr", "ensemble").load()
    s_ = core.utils.time_series.mean_flatten(s_, dims=["lat", "lon"])
    m_ = core.utils.time_series.mean_flatten(m_, dims=["lat", "lon"])
    mp_ = core.utils.time_series.mean_flatten(mp_, dims=["lat", "lon"])
    # Find difference and subtract control
    s_ = difference_and_remove_control(s_)
    m_ = difference_and_remove_control(m_)
    mp_ = difference_and_remove_control(mp_)
    s_ = subtract_last_decade_mean(s_)
    m_ = subtract_last_decade_mean(m_)
    mp_ = subtract_last_decade_mean(mp_)
    m_ = core.utils.time_series.shift_arrays(m_, daily=False)
    mp_ = core.utils.time_series.shift_arrays(mp_, daily=False)
    s_ = core.utils.time_series.shift_arrays(s_, daily=False)
    m_ = _time_from_eruption_start(m_, cut=int(12 * 20))
    mp_ = _time_from_eruption_start(mp_, cut=int(12 * 20))
    s_ = _time_from_eruption_start(s_, cut=int(12 * 20))
    plt.figure()
    [a.plot() for a in m_ + mp_ + s_]
    return m_, mp_, s_


def plot_evolution(f, t) -> None:
    f_, t_ = np.asarray(f).mean(axis=0), np.asarray(t).mean(axis=0)
    # Calculate the integral up to every point in the arrays
    integral = np.zeros_like(f_, dtype=float)
    for i in range(len(f_)):
        integral[i] = np.trapz(f_[: i + 1]) / np.trapz(t_[: i + 1])
    kappa = integral - integral[-1]
    plt.figure()
    plt.plot(f_, label="F")
    plt.plot(t_, label="T")
    plt.plot(integral, label="Rho")
    plt.plot(kappa, label="Kappa")
    plt.legend()


def main():
    """Run the main function that runs the calculations."""
    data = (
        DATAFILES.find(
            ["e_BWma1850", "e_fSST1850"],
            {f"ens{i}" for i in [0, 1, 2, 3, 4]},
            ("TREFHT", "FLNT", "FSNT"),
            "h0",
            {"strong", "medium", "medium-plus", "control"},
        )
        .sort("attr", "ensemble")
        .keep_most_recent()
    )
    temp_m, temp_mp, temp_s = _get_temp_arrays(data)
    m_, mp_, s_ = _get_forcing_arrays(data)
    plt.show()
    r = np.array(_compute_integral_ratio((m_, temp_m), (mp_, temp_mp), (s_, temp_s)))
    sims = np.array([0] * 4 + [1] * 4 + [2] * 4)
    plt.scatter(sims, r)
    plt.errorbar(
        [0.2, 1.2, 2.2],
        [r[:4].mean(), r[4:8].mean(), r[8:].mean()],
        yerr=[r[:4].std(), r[4:8].std(), r[8:].std()],
        fmt="_",
    )
    plot_evolution(m_, temp_m)
    plot_evolution(mp_, temp_mp)
    plot_evolution(s_, temp_s)
    # fmt: off
    print(f"% C2W^:\t\t{r[8:].mean():.2f}+-{r[8:].std():.2f}\t{(1/r[8:]).mean():.3f}+-{(1/r[8:]).std():.3f}")
    print(f"% C2W-:\t\t{r[4:8].mean():.2f}+-{r[4:8].std():.2f}\t{(1/r[4:8]).mean():.3f}+-{(1/r[4:8]).std():.3f}")
    print(f"% C2W_:\t\t{r[:4].mean():.1f}+-{r[:4].std():.1f}\t\t{(1/r[:4]).mean():.2f}+-{(1/r[:4]).std():.2f}")
    print(f"% C2W_ (1:):\t{r[1:4].mean():.2f}+-{r[1:4].std():.2f}\t{(1/r[1:4]).mean():.3f}+-{(1/r[1:4]).std():.3f}")
    print(f"% Total:\t{r.mean():.1f}+-{r.std():.1f}\t\t{(1/r).mean():.3f}+-{(1/r).std():.3f}")
    print(f"% Total (1:):\t{r[1:].mean():.2f}+-{r[1:].std():.2f}\t{(1/r[1:]).mean():.3f}+-{(1/r[1:]).std():.3f}")
    print(f"% C2W^:\t\t{r[8:].mean():.1f}+-{r[8:].std():.1f}\t{(1/r[8:]).mean():.2f}+-{(1/r[8:]).std():.2f}")
    print(f"% C2W-:\t\t{r[4:8].mean():.1f}+-{r[4:8].std():.1f}\t{(1/r[4:8]).mean():.2f}+-{(1/r[4:8]).std():.2f}")
    print(f"% C2W_:\t\t{r[:4].mean():.0f}+-{r[:4].std():.0f}\t\t{(1/r[:4]).mean():.1f}+-{(1/r[:4]).std():.1f}")
    print(f"% C2W_ (1:):\t{r[1:4].mean():.1f}+-{r[1:4].std():.1f}\t{(1/r[1:4]).mean():.2f}+-{(1/r[1:4]).std():.2f}")
    print(f"% Total:\t{r.mean():.0f}+-{r.std():.0f}\t\t{(1/r).mean():.2f}+-{(1/r).std():.2f}")
    print(f"% Total (1:):\t{r[1:].mean():.1f}+-{r[1:].std():.1f}\t{(1/r[1:]).mean():.2f}+-{(1/r[1:]).std():.2f}")
    # fmt: on
    plt.show()


if __name__ == "__main__":
    main()
