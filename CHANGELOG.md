# Changelog

## [1.0.0](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/compare/v0.13.0...v1.0.0) (2025-02-24)


### ⚠ BREAKING CHANGES

* **main:** update to reflect the latest submitted manuscript

### Features

* big update for review 2 of the ms ([f002891](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/f002891e8b27f560e517bbd44f17bb72d2a50dd3))
* **figure:** add colour indicating model family similarities ([177e12e](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/177e12ef0d523bbeb99d51b46c2ad42943ce7369))


### Bug Fixes

* **figures:** use the same normalisation in M20 as in STrop ([5b564bb](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/5b564bb6cbc10ee10ceb423e103391bf6e8f5611))


### Miscellaneous

* **unit:** adjust unit in figures ([7c68690](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/7c6869008f9605186f6416d5e61157f08a279f21))
* upload small scripts to git ([70fd224](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/70fd224ee9f41efff39b534a6ed0304cb1e57a05))


### Code Refactoring

* **figure:** rename AOD to SAOD ([81d33e1](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/81d33e173791c62447f95da1ccd6f44fa4b5ee59))


### Documentation

* **main:** update to reflect the latest submitted manuscript ([062e53b](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/062e53b399a3caae7034bd2023047ce9c2cb329f))

## [0.13.0](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/compare/v0.12.1...v0.13.0) (2024-08-31)


### Features

* **figure:** add evaluation of the Pearson coeff for figure 4 ([3b71c2d](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/3b71c2d882621c83781d3552780c19c5ab3adae8))


### Styles

* format files and fix permissions ([c896258](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/c896258a9769a1b33d6612951ae5e793acd6f8ba))

## [0.12.1](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/compare/v0.12.0...v0.12.1) (2024-08-29)


### Code Refactoring

* **lint:** apply linter auto fixes ([680cd72](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/680cd723591be6f7c8ef847ed9892497bc125565))


### Build System

* **uv:** update old toml specifications for linters ([3b2f342](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/3b2f342acbb9d53443c7c5068570acabcebfd13d))

## [0.12.0](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/compare/v0.11.0...v0.12.0) (2024-08-28)


### Features

* **figure:** re-write figure 1 with `figure_grid` and as PDF ([75b731b](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/75b731bcb676b667b11c18da9126a5c8f913c831))
* **figure:** re-write figure 2 with `figure_grid` and as PDF ([79cf091](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/79cf09166687362e3cd8735ef5cfe8f3cb39cb34))
* **figure:** re-write figure 3 with `figure_grid` and as PDF ([c84661b](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/c84661bb3be9260b0123f280e5220c2bc77b89cb))
* **figure:** re-write figure 4 with `figure_grid` and as PDF ([c557130](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/c5571304c28dca48250c6a7efe54ac2584a481b3))


### Miscellaneous

* **core:** update labels and add optional aod conversion ([9c2f405](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/9c2f40526f82065e1991017bb561c06ca783d098))
* **figure:** add plots of Reff, OH and SO2 burden ([0a8dd52](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/0a8dd52a64932a3ee3a9562ba547350230fff141))
* fix empty lines and label names ([d4997a0](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/d4997a06ab46b929c3522a1ecaf429dae2c0bafa))


### Build System

* move from rye to uv and update deps ([5b5c2f0](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/5b5c2f0055c6a9bdeb88f5b47277d5859e79f678))


### Documentation

* uv doesn't provide a list scripts command like rye does... ([17b07a6](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/17b07a6e852d459427f963f443de35462afc15af))

## [0.11.0](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/compare/v0.10.6...v0.11.0) (2024-08-20)


### Features

* **plotting:** add Reff, OH and SO2 burden plots ([388bf98](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/388bf986b29d41ef3c574dbc643eb33a81a0daf1))


### Bug Fixes

* **xarray:** roll back version to 2024.2.0 ([3890d4f](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/3890d4f64dd30b7fc27b699ddb90baf77b01ed26))


### Styles

* format file ([7666bd3](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/7666bd3a338e4fd0ccd66ab323c776abe45f3c67))


### Code Refactoring

* move from poetry to rye and fix minor style issues ([aef3111](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/aef3111806662db9b716267fd06b86bdaeb46aee))


### Build System

* **deps-dev:** bump setuptools from 69.0.2 to 70.0.0 ([#47](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/issues/47)) ([baa4f41](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/baa4f41221493ec9f665b14481fc6819fc0cb7a2))
* **deps:** bump urllib3 from 2.1.0 to 2.2.2 ([#48](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/issues/48)) ([8b4765d](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/8b4765d78394323d02ad2f15cb5b02afc7552660))
* **deps:** bump zipp from 3.17.0 to 3.19.1 ([#49](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/issues/49)) ([62ffef6](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/62ffef6a67f31fe93f526b265ca3bb9a88341367))
* **rye:** resolve deps universially ([a4ac5de](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/a4ac5de94e487bb25fe228afe28b2c87a1c05caf))


### Documentation

* update instructions to use Rye instead of Poetry ([cdff6b4](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/cdff6b41bcfd69fdacf5b1fe018b344b8843fd10))

## [0.10.6](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/compare/v0.10.5...v0.10.6) (2024-06-04)


### Continuous Integration

* **workflow:** update release-please to v4 ([c8b2c9e](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/c8b2c9e25fad6fded36e99ca72b8196ec43af1e8))


### Build System

* **deps:** bump idna from 3.6 to 3.7 ([#44](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/issues/44)) ([0c2b622](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/0c2b622a304c57da390268eaad6d4b1a685d31f0))
* **deps:** bump pillow from 10.2.0 to 10.3.0 ([#41](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/issues/41)) ([22d87a1](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/22d87a1e0c74658d986ff1f5b0ab092a41eb719a))
* **deps:** bump requests from 2.31.0 to 2.32.2 ([#45](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/issues/45)) ([5318f2c](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/5318f2c861e3e54d5501520b20bfbb16840086fe))

## [0.10.5](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/compare/v0.10.4...v0.10.5) (2024-06-03)


### Bug Fixes

* **zenodo:** correctly specify zenodo metadata ([1810e16](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/1810e16c143ab1104c95b5bec701c07ac6df41ec))


### Miscellaneous

* **plotting:** update font size to latest cosmoplots defaults ([1810e16](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/1810e16c143ab1104c95b5bec701c07ac6df41ec))


### Tests

* **zenodo:** test that the zenodo json schema is correct ([1810e16](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/1810e16c143ab1104c95b5bec701c07ac6df41ec))


### Build System

* **deps:** update dependencies ([1810e16](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/1810e16c143ab1104c95b5bec701c07ac6df41ec))

## [0.10.4](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/compare/v0.10.3...v0.10.4) (2024-06-03)


### Bug Fixes

* **zenodo:** update creator metadata ([0985746](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/098574666e19d05d89c7cc743936d90247166160))

## [0.10.3](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/compare/v0.10.2...v0.10.3) (2024-06-03)


### Bug Fixes

* **zenodo:** fix creators metadata ([7819822](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/78198224bf953cee4f8b673b9d3f9f385275328f))

## [0.10.2](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/compare/v0.10.1...v0.10.2) (2024-06-03)


### Bug Fixes

* **zenodo:** only use the name field ([3a10910](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/3a109109975be28050d48e3bb9267db9eeb39a87))

## [0.10.1](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/compare/v0.10.0...v0.10.1) (2024-06-03)


### Miscellaneous

* maintenance ([13041ea](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/13041ea7364fb64618f8b707e3bd4e8e00bee682))


### Documentation

* **zenodo:** better specification of metadata name and affiliation ([35b977c](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/35b977ccaa45eb0cc9a31be895336e78ebd18431))

## [0.10.0](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/compare/v0.9.1...v0.10.0) (2024-02-28)


### Features

* **figure:** add 3000 Tg runs to figures ([55bbd30](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/55bbd309b64c764e398a215a606015210510fec4))


### Bug Fixes

* **figure:** keep ens1 for the highlat case ([6436261](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/643626179b9658c9d47877fa463202f1c37e8f8f))
* **ob16:** small bug in the peak finding strategy ([e1680ef](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/e1680effdba03df3a8a29e489928678dd737b745))


### Miscellaneous

* **docs:** change repo name ([32d74a8](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/32d74a8286fe796bc69b5d77e289835f35c2cfb4))
* **figure:** small adjustment to fig4 ([29316de](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/29316de46ba9ac56933f49477927a96968b08e3c))


### Styles

* format ([637e654](https://github.com/engeir/code-to-radiative-forcing-by-super-volcano-eruptions/commit/637e6547718fcf80ef9a12b4e31a94b42a234c23))

## [0.9.1](https://github.com/engeir/paper1-code/compare/v0.9.0...v0.9.1) (2024-01-31)


### Bug Fixes

* **cesm:** use ens5 instead of ens1, which had erroneous temperature ([bc89e8c](https://github.com/engeir/paper1-code/commit/bc89e8c66addfce38ddf0b8b1e9db7d74ded600b))

## [0.9.0](https://github.com/engeir/paper1-code/compare/v0.8.2...v0.9.0) (2024-01-29)


### Features

* **plot:** add climate resistance ([#34](https://github.com/engeir/paper1-code/issues/34)) ([2b61bb9](https://github.com/engeir/paper1-code/commit/2b61bb9861c4308a6df6f2f5027ec665905cd7fe))


### Build System

* **deps:** bump pillow from 10.1.0 to 10.2.0 ([#33](https://github.com/engeir/paper1-code/issues/33)) ([6b30f32](https://github.com/engeir/paper1-code/commit/6b30f326b7292d495482e37c530587b739de9fbc))

## [0.8.2](https://github.com/engeir/paper1-code/compare/v0.8.1...v0.8.2) (2024-01-22)


### Bug Fixes

* **figure:** use most recent data ([876d8f4](https://github.com/engeir/paper1-code/commit/876d8f410effde59d99256b087f217b14f54ce18))
* **font:** specify matplotlib preamble ([574a454](https://github.com/engeir/paper1-code/commit/574a4549591d18fbc194a3acc9d7fcd40fb7b7e4))
* **namespace:** do not overwrite `next` to local variable ([9f7f07b](https://github.com/engeir/paper1-code/commit/9f7f07bbdd792b9512fa51ca22bf535782eff620))


### Miscellaneous

* **figure:** remove grey box indicating small view ([628f4d8](https://github.com/engeir/paper1-code/commit/628f4d87dbe7e29f951e93d324fb98f7b8270d76))
* **load:** remove ucar scritps from git tracking ([c767a4a](https://github.com/engeir/paper1-code/commit/c767a4a2b8caa10f2dd49f201abc4920470589fc))
* write 'Warning' instead of 'WARNING' ([83b2906](https://github.com/engeir/paper1-code/commit/83b290645fd6bf1484835094d5d33981fcfe119b))


### Code Refactoring

* **lint:** fix lint warning, overwrite built-in function "format" ([45dd383](https://github.com/engeir/paper1-code/commit/45dd38361bd996dff46d7d2872cc5ebfb5309969))


### Continuous Integration

* **github:** use bot account to generate releases ([9984854](https://github.com/engeir/paper1-code/commit/9984854117bda1f461454c52b7391e1b7d78b6f5))


### Build System

* **mise:** move python venv setup to development config file ([9f47af1](https://github.com/engeir/paper1-code/commit/9f47af1d75c4feb8fab6d37f1c338e9d22e6ea51))


### Documentation

* **docstring:** add DOI to all load scripts ([6eb0bfd](https://github.com/engeir/paper1-code/commit/6eb0bfd51f092269be982bdbe8a341495720ec4f))

## [0.8.1](https://github.com/engeir/paper1-code/compare/v0.8.0...v0.8.1) (2024-01-11)


### Bug Fixes

* **build:** update name to mise from rtx ([434ef6f](https://github.com/engeir/paper1-code/commit/434ef6ff2d7e623f2c3a0dd884c02e62ca3972ba))
* **security:** updates gitpython as described by https://github.com/engeir/paper1-code/security/dependabot/1 ([08944a4](https://github.com/engeir/paper1-code/commit/08944a4b7dee9f7adf9f95f1365cbfee340d2640))


### Miscellaneous

* **climate resistance:** use 20 years of mp and s ([3277561](https://github.com/engeir/paper1-code/commit/327756103df0e0724b07b936150ab10998410d95))


### Styles

* **supp:** update formatting of supplementary fig script ([f5ba8a7](https://github.com/engeir/paper1-code/commit/f5ba8a73d5cfcdd7764572ac331aaaf954b32127))


### Documentation

* **M20:** add DOI to Marshall data module ([8977881](https://github.com/engeir/paper1-code/commit/89778815460c0f574542284a7bf8bf78d2469e9d))

## [0.8.0](https://github.com/engeir/paper1-code/compare/v0.7.2...v0.8.0) (2024-01-04)


### Features

* **climate resistance:** implement initial calculation script ([134de41](https://github.com/engeir/paper1-code/commit/134de41d027126b3107e3e9d84a8ed88471352d7))
* **data:** add download and install instructions for OB16 ([3bc73d9](https://github.com/engeir/paper1-code/commit/3bc73d98d8c673d3884b612371c600157cf3d147))
* **figure:** merge figs 1 and 2, removes int normalization ([ce8e605](https://github.com/engeir/paper1-code/commit/ce8e605aee11253f476c0046dc5d1cd48bbec209))


### Miscellaneous

* **config:** create toml simple toml file ([455e732](https://github.com/engeir/paper1-code/commit/455e7322a4804cff7c8b8d6e0bfe738a752281a2))


### Code Refactoring

* **find-files:** use the returns library ([a824081](https://github.com/engeir/paper1-code/commit/a824081adef5d41e6653f1790f6a1a3445fe660d))

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
