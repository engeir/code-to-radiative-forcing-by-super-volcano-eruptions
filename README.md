# Accompanying code to "Radiative forcing by super-volcano eruptions"

[![DOI](https://zenodo.org/badge/724130844.svg)](https://zenodo.org/badge/latestdoi/724130844)

<sup>Latest version: v0.10.5</sup> <!-- x-release-please-version -->

> Code to download and analyze data for a paper

## Install

Clone and move into the repository:

```bash
git clone git@github.com:engeir/code-to-radiative-forcing-by-super-volcano-eruptions.git
cd code-to-radiative-forcing-by-super-volcano-eruptions
```

[Poetry](python-poetry.org) is used to install the dependencies, which itself is
recommended to be installed
[via pipx](https://python-poetry.org/docs/#installing-with-pipx).

Provided Poetry is available, the project can be installed with:

```bash
poetry install
```

## Usage

Every figure has its own executable. Figures are created by running:

```bash
poetry run generate-fig1
poetry run generate-fig2
poetry run generate-fig3
poetry run generate-fig4
```

or:

```bash
poetry run generate-figs
```
