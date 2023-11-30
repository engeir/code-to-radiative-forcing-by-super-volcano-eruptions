# Changelog

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
