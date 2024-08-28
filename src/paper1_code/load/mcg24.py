"""Load McGraw et al. (2024) data.

Notes
-----
See https://doi.org/10.1175/JCLI-D-23-0116.1 for the full paper.
"""


# finder = volcano_base.load.load_mcg24_files.find_mcg24_files().find("tsurf").copy
# finder().avail()
# e1_jan = finder().find("e1", "janeruption").sort("reff")
# e1_jul = finder().find("e1", {"juneruption", "juleruption"}).sort("reff")
# e2_jan = finder().find("e2", "janeruption").sort("reff")
# e2_jul = finder().find("e2", {"juneruption", "juleruption"}).sort("reff")
# e3_jan = finder().find("e3", "janeruption").sort("reff")
# e3_jul = finder().find("e3", {"juneruption", "juleruption"}).sort("reff")
# flat = volcano_base.manipulate.mean_flatten
# ens = ""
# eruption = ""
# reff = ""
# for x_l in [
#     flat(ens.load(), dims=["lat", "lon"])
#     for ens in [e1_jan, e1_jul, e2_jan, e2_jul, e3_jan, e3_jul]
# ]:
#     for x_ in x_l[:-1]:
#         temp = x_.data  # - x_l[-1].data
#         if ens != x_.attrs["ensemble"]:
#             ens = x_.attrs["ensemble"]
#             ens_ = f"{ens}, "
#         else:
#             ens_ = "    "
#         if eruption != x_.attrs["eruption"][:3]:
#             eruption = x_.attrs["eruption"][:3]
#             eruption_ = f"{eruption}, "
#         else:
#             eruption_ = "     "
#         print(f"{ens_}{eruption_}{x_.attrs["reff"]}:\t {temp}")

# reader = csv.DictReader(open("txt.csv"))
# for row in reader:
#     if float(row["Reff_peak_um"]) == 0.6:
#         print(row["dTsurf_peak_degC"], ",")


def get_so2_mcg24() -> tuple[float, float, float, float, float, float]:
    """Based on the paper by McGraw et al. (2024)."""
    return (
        18,
        100,
        200,
        400,
        1000,
        2000,
    )


def get_rf_mcg24() -> tuple[float, float, float, float, float, float]:
    """Based on the paper by McGraw et al. (2024)."""
    return (
        2.17,
        10.69,
        19.5,
        32.97,
        51.51,
        61.53,
    )


def get_trefht_mcg24() -> tuple[float, float, float, float, float, float]:
    """Based on the paper by McGraw et al. (2024)."""
    return (
        0.47,
        1.37,
        2.61,
        4.59,
        7.46,
        9.63,
    )
