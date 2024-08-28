# Accompanying code to "Radiative forcing by super-volcano eruptions"

[![DOI](https://zenodo.org/badge/724130844.svg)](https://zenodo.org/badge/latestdoi/724130844)

<sup>Latest version: v0.11.0</sup> <!-- x-release-please-version -->

> Code to download and analyse data for a paper

## Install

Clone and move into the repository:

```bash
git clone https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions.git
cd code-to-radiative-forcing-by-super-volcano-eruptions || exit
```

[uv](https://docs.astral.sh/uv/) is used to install the dependencies, with installation
instructions provided [here](https://docs.astral.sh/uv/getting-started/installation/).

Provided uv is available, the project can be installed with:

```bash
uv sync
```

## Usage

Every figure has its own executable. Figures are created by running:

```bash
uv run generate-fig1
uv run generate-fig2
uv run generate-fig3
uv run generate-fig4
```

or:

```bash
uv run generate-figs
```
