"""Test the config module."""


import paper1_code as core


def test_means() -> None:
    """Test config constants."""
    finder = core.utils.find_c2w_files.FindFiles()
    # finder.avail()
    finder.find("e_BWma1850", "control", "TREFHT")
    if len(finder) != 1:
        raise ValueError(
            "The number of matched files is not 1, making this test ambiguous."
        )
    arr = finder.load()[0]
    arr_ = core.utils.time_series.mean_flatten(arr, dims=["lat", "lon"]).compute()
    assert f"{arr_.mean().data:.8f}" == f'{core.config.MEANS["TREFHT"]:.8f}'


if __name__ == "__main__":
    test_means()
