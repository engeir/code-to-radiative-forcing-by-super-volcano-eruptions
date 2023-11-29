# Accompanying code to parameter scan

<sup>Latest version: v0.3.2</sup> <!-- x-release-please-version -->

> Code to download and analyze data for a paper

## Install

Clone and move into the repository:

```bash
git clone git@github.com:engeir/paper1-code.git
cd paper1-code
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
poetry run generate-fig5
```

or:

```bash
poetry run generate-figs
```
