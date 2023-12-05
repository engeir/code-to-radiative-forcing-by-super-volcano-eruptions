# Changelog

## [0.7.2](https://github.com/engeir/paper1-code/compare/v0.7.1...v0.7.2) (2023-12-05)


### Miscellaneous

* **docs:** add FIXME comments for module docstrings ([9d7d383](https://github.com/engeir/paper1-code/commit/9d7d3839f5313fefbc86e6c628f5558a48752f0d))

## [0.7.1](https://github.com/engeir/paper1-code/compare/v0.7.0...v0.7.1) (2023-12-05)


### Bug Fixes

* **figure:** incorrect time series used in fig5 ([4f9810c](https://github.com/engeir/paper1-code/commit/4f9810c81f9bca1d9982ed2adb5f3f8d2d6728c3))


### Miscellaneous

* **figure:** add old fig2 back in as supplementary ([c80b30e](https://github.com/engeir/paper1-code/commit/c80b30e5e9ac9654e49b3627f0999d9997ba8248))


### Code Refactoring

* **data:** generalize and de-clutter cesm array loading ([c80b30e](https://github.com/engeir/paper1-code/commit/c80b30e5e9ac9654e49b3627f0999d9997ba8248))


### Documentation

* **README:** change to new executable script name ([9ff6d47](https://github.com/engeir/paper1-code/commit/9ff6d477787aa865ecb1e64cc4666a75953d7d81))

## [0.7.0](https://github.com/engeir/paper1-code/compare/v0.6.0...v0.7.0) (2023-12-05)


### ⚠ BREAKING CHANGES

* **figure:** remove previous fig2

### Features

* **figure:** finish new implementation of fig1 (and fig2) ([d975001](https://github.com/engeir/paper1-code/commit/d975001b6d9c33af19f25a001388948b59f89439))
* **figure:** remove previous fig2 ([c5c21b9](https://github.com/engeir/paper1-code/commit/c5c21b9e33cbeadcf23fb66f05442de2102d7f87))


### Miscellaneous

* release 0.7.0 ([2670379](https://github.com/engeir/paper1-code/commit/267037904b22f4d3d97fb4cea03dea9623c27c60))

## [0.6.0](https://github.com/engeir/paper1-code/compare/v0.5.0...v0.6.0) (2023-12-04)


### ⚠ BREAKING CHANGES

* **figure:** change fig1 and soon make fig2 redundant

### Features

* **figure:** change fig1 and soon make fig2 redundant ([e870504](https://github.com/engeir/paper1-code/commit/e870504c02e6019b9d49012e058ac72a89481f4e))


### Miscellaneous

* release 0.5.1 ([f2027f9](https://github.com/engeir/paper1-code/commit/f2027f9290e6e25ed5b8d6463a2a082f202a138d))
* release 0.6.0 ([9d7560c](https://github.com/engeir/paper1-code/commit/9d7560c2166e562c7fbcccfb9567c50b32f4cf37))


### Code Refactoring

* **data:** move load function into designated modules ([#25](https://github.com/engeir/paper1-code/issues/25)) ([e870504](https://github.com/engeir/paper1-code/commit/e870504c02e6019b9d49012e058ac72a89481f4e))

## [0.5.0](https://github.com/engeir/paper1-code/compare/v0.4.1...v0.5.0) (2023-12-04)


### Features

* **figure:** finish implementing figure 5 ([#23](https://github.com/engeir/paper1-code/issues/23)) ([fb13aea](https://github.com/engeir/paper1-code/commit/fb13aea8404a9627489c4ab8b73a5ce81c2b23cb))


### Code Refactoring

* **figure:** move fig1 functions into classes ([fb13aea](https://github.com/engeir/paper1-code/commit/fb13aea8404a9627489c4ab8b73a5ce81c2b23cb))
* **utils:** move normalize_peaks to general figure load module ([fb13aea](https://github.com/engeir/paper1-code/commit/fb13aea8404a9627489c4ab8b73a5ce81c2b23cb))

## [0.4.1](https://github.com/engeir/paper1-code/compare/v0.4.0...v0.4.1) (2023-11-30)


### Documentation

* **README:** add zenodo badge ([#21](https://github.com/engeir/paper1-code/issues/21)) ([678d304](https://github.com/engeir/paper1-code/commit/678d30446d2934f06e7014d76b64513c7a1e70b4))

## [0.4.0](https://github.com/engeir/paper1-code/compare/v0.3.3...v0.4.0) (2023-11-30)


### Features

* **figure:** finish creating figure 4 ([#19](https://github.com/engeir/paper1-code/issues/19)) ([f1f3ca6](https://github.com/engeir/paper1-code/commit/f1f3ca6eec2b4d48d1a558a5d62d98110d329390))
* **figure:** only show output when the scripts are run as __main__ ([f1f3ca6](https://github.com/engeir/paper1-code/commit/f1f3ca6eec2b4d48d1a558a5d62d98110d329390))
* **utils:** add weighted_season_avg function ([f1f3ca6](https://github.com/engeir/paper1-code/commit/f1f3ca6eec2b4d48d1a558a5d62d98110d329390))


### Code Refactoring

* **figure:** move c2w data load to load_data module ([f1f3ca6](https://github.com/engeir/paper1-code/commit/f1f3ca6eec2b4d48d1a558a5d62d98110d329390))
* **figure:** move m20 data load to load_data module ([f1f3ca6](https://github.com/engeir/paper1-code/commit/f1f3ca6eec2b4d48d1a558a5d62d98110d329390))
* **figure:** move plot legends to config ([f1f3ca6](https://github.com/engeir/paper1-code/commit/f1f3ca6eec2b4d48d1a558a5d62d98110d329390))
* **utils:** improve type hint of FindFiles.sort ([f1f3ca6](https://github.com/engeir/paper1-code/commit/f1f3ca6eec2b4d48d1a558a5d62d98110d329390))

## [0.3.3](https://github.com/engeir/paper1-code/compare/v0.3.2...v0.3.3) (2023-11-29)


### Bug Fixes

* **zenodo:** fix the zenodo config, remove empty fields ([#17](https://github.com/engeir/paper1-code/issues/17)) ([ed2c95f](https://github.com/engeir/paper1-code/commit/ed2c95fa0b8e6480d31a5ec30427279369d9275b))

## [0.3.2](https://github.com/engeir/paper1-code/compare/v0.3.1...v0.3.2) (2023-11-29)


### Documentation

* **zenodo:** create .zenodo.json ([#15](https://github.com/engeir/paper1-code/issues/15)) ([0dcef0c](https://github.com/engeir/paper1-code/commit/0dcef0ca48b6134ac397bb081cee4525101cd0f8))

## [0.3.1](https://github.com/engeir/paper1-code/compare/v0.3.0...v0.3.1) (2023-11-29)


### Bug Fixes

* **docs:** incorrect function call used in docstring example ([b49832d](https://github.com/engeir/paper1-code/commit/b49832d2bfb0e1f59bd4ec405a72a62bae8ceaa8))
* **tests:** xdoctest was not running on the files ([#13](https://github.com/engeir/paper1-code/issues/13)) ([b49832d](https://github.com/engeir/paper1-code/commit/b49832d2bfb0e1f59bd4ec405a72a62bae8ceaa8))

## [0.3.0](https://github.com/engeir/paper1-code/compare/v0.2.0...v0.3.0) (2023-11-29)


### Features

* **figure:** finish creating figure 3 ([#11](https://github.com/engeir/paper1-code/issues/11)) ([a2b19bc](https://github.com/engeir/paper1-code/commit/a2b19bca651a9560919a649578f2875a1b676441))
* **figure:** move general data load code out from fig2 ([a2b19bc](https://github.com/engeir/paper1-code/commit/a2b19bca651a9560919a649578f2875a1b676441))
* **utils:** add weighted_year_avg function ([a2b19bc](https://github.com/engeir/paper1-code/commit/a2b19bca651a9560919a649578f2875a1b676441))


### Code Refactoring

* **figure:** use RF instead of TOA, more accurate ([a2b19bc](https://github.com/engeir/paper1-code/commit/a2b19bca651a9560919a649578f2875a1b676441))


## [0.2.0](https://github.com/engeir/paper1-code/compare/v0.1.1...v0.2.0) (2023-11-29)


### Features

* **figure:** finish creating figure 2 ([#7](https://github.com/engeir/paper1-code/issues/7)) ([fb17cb1](https://github.com/engeir/paper1-code/commit/fb17cb13572c60f254664a86316a7084b104b4a1))
* **utils:** add dt2float and float2dt functions ([fb17cb1](https://github.com/engeir/paper1-code/commit/fb17cb13572c60f254664a86316a7084b104b4a1))
* **utils:** add get_median function ([fb17cb1](https://github.com/engeir/paper1-code/commit/fb17cb13572c60f254664a86316a7084b104b4a1))
* **utils:** add keep_whole_year function ([fb17cb1](https://github.com/engeir/paper1-code/commit/fb17cb13572c60f254664a86316a7084b104b4a1))


### Code Refactoring

* **figure:** generalize figure 1 code ([fb17cb1](https://github.com/engeir/paper1-code/commit/fb17cb13572c60f254664a86316a7084b104b4a1))


### Continuous Integration

* **pre-commit:** add pydoclint ([fb17cb1](https://github.com/engeir/paper1-code/commit/fb17cb13572c60f254664a86316a7084b104b4a1))

## [0.1.1](https://github.com/engeir/paper1-code/compare/v0.1.0...v0.1.1) (2023-11-28)


### Documentation

* **README:** set up structure ([#5](https://github.com/engeir/paper1-code/issues/5)) ([8cfbcf8](https://github.com/engeir/paper1-code/commit/8cfbcf85623022dc6b650f130205b17f821c19ea))

## 0.1.0 (2023-11-28)


### Features

* **figure:** finish creating fig1 from CESM2 data ([#1](https://github.com/engeir/paper1-code/issues/1)) ([bcb7b6e](https://github.com/engeir/paper1-code/commit/bcb7b6e110f954fd713b8c3e7f383b05c1a0e8d8))


### Continuous Integration

* **github:** workflow cannot depend on non-existing job ([#3](https://github.com/engeir/paper1-code/issues/3)) ([2d92134](https://github.com/engeir/paper1-code/commit/2d92134934352fa61fd202d9ffe944ef922d1db8))
* **release:** set up releases with release-please ([#2](https://github.com/engeir/paper1-code/issues/2)) ([4d86c60](https://github.com/engeir/paper1-code/commit/4d86c60d638fe850a629980b48fd38d7b6c5b8fe))
