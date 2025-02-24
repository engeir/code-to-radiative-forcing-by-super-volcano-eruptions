"""Create SO4 vertical profile."""

import matplotlib.pyplot as plt
import volcano_base.manipulate as vbm
import xarray as xr

import paper1_code as core

SAVE_PATH = core.utils.if_save.create_savedir()
COLOR = core.config._C

ds1 = xr.load_dataset(
    "/media/een023/LaCie/een023/cesm/model-runs/ensemble-simulations/e_fSST1850/e_fSST1850-ens1-strong/aggregate/so4_a1-h0-20230828.nc"
)
ds2 = xr.load_dataset(
    "/media/een023/LaCie/een023/cesm/model-runs/ensemble-simulations/e_fSST1850/e_fSST1850-ens1-strong/aggregate/so4_a2-h0-20230828.nc"
)
ds3 = xr.load_dataset(
    "/media/een023/LaCie/een023/cesm/model-runs/ensemble-simulations/e_fSST1850/e_fSST1850-ens1-strong/aggregate/so4_a3-h0-20230828.nc"
)

# ylim = (0, 70)
ylim = (0, 400)
da1 = ds1.so4_a1
da1 = vbm.mean_flatten(da1, dims=["lon", "lat"])
# da1 = da1.assign_coords(lev=vbm.pressureheight2metricheight(da1.coords["lev"]))
da1.plot(x="time")
plt.xlim((core.utils.misc.d2n("1850-01-01"), core.utils.misc.d2n("1853-01-01")))
plt.ylim(ylim)
plt.savefig(SAVE_PATH / "so4_a1_high")
plt.show()
da2 = ds2.so4_a2
da2 = vbm.mean_flatten(da2, dims=["lon", "lat"])
# da2 = da2.assign_coords(lev=vbm.pressureheight2metricheight(da2.coords["lev"]))
da2.plot(x="time")
plt.xlim((core.utils.misc.d2n("1850-01-01"), core.utils.misc.d2n("1853-01-01")))
plt.ylim(ylim)
plt.savefig(SAVE_PATH / "so4_a2_high")
plt.show()
da3 = ds3.so4_a3
da3 = vbm.mean_flatten(da3, dims=["lon", "lat"])
# da3 = da3.assign_coords(lev=vbm.pressureheight2metricheight(da3.coords["lev"]))
da3.plot(x="time")
plt.xlim((core.utils.misc.d2n("1850-01-01"), core.utils.misc.d2n("1853-01-01")))
plt.ylim(ylim)
plt.savefig(SAVE_PATH / "so4_a3_high")
plt.show()
tot = da1 + da2 + da3
tot.plot(x="time")
plt.xlim((core.utils.misc.d2n("1850-01-01"), core.utils.misc.d2n("1853-01-01")))
plt.ylim(ylim)
plt.savefig(SAVE_PATH / "so4_tot_high")
plt.show()
