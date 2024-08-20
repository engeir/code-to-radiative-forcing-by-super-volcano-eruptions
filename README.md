# Accompanying code to "Radiative forcing by super-volcano eruptions"

[![DOI](https://zenodo.org/badge/724130844.svg)](https://zenodo.org/badge/latestdoi/724130844)

<sup>Latest version: v0.10.6</sup> <!-- x-release-please-version -->

> Code to download and analyse data for a paper

## Install

Clone and move into the repository:

```bash
git clone https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions.git
cd code-to-radiative-forcing-by-super-volcano-eruptions || exit
```

[Rye](rye.astral.sh) is used to install the dependencies, with installation instructions
provided [here](https://rye.astral.sh/guide/installation/).

Provided Rye is available, the project can be installed with:

```bash
rye sync
```

## Usage

Every figure has its own executable. Figures are created by running: (see
`grep "generate" <(rye run)` for a list of available commands)

```bash
rye run generate-fig1
rye run generate-fig2
rye run generate-fig3
rye run generate-fig4
```

or:

```bash
rye run generate-figs
```
