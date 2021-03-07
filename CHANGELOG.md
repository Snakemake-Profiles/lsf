# CHANGELOG

<!--- Please follow these guidelines https://keepachangelog.com/en/1.0.0/ --->

This document tracks changes to the `master` branch of the profile.

## [unreleased]

## Added

- Support for complex quote-expansion via `shlex` [[#39]][39]]
- Function docstrings in `lsf_config.py` for documentation

## [0.1.0] - 18/01/2021

### Added

- Version tagging to allow for user notification of changes to functionality

### Changed

- Parameters given in the config file are now deduplicated. For instance, if a default
  for `-q` is given, and a rule specifies `-q` also, the rule's value for `-q` is chosen.
  Previously, parameters were just concatenated [[#36][36]]

## 23/10/2020

### Changed

- When log file is not found, we now return failed instead of running. Returning running
  was effectively causing an infinite loop.
- Unknown line status now also returns failed instead of raising an error. Raising
  errors without returning a status causes problems with the snakemake master process.

## 09/04/2020

**Added:**
- Look at the log file if `bsub` returns an empty job status. See [#5][5] for more
  information.
- Allow specifying per-rule cluster resource settings (similar to deprecated cluster
  config). See [#15][15] and [#7][7] for more information.
- Added a `CONTRIBUTING.md` document [#15][15]
- TESTS!! A big thanks to [@leoisl](https://github.com/leoisl) for getting this off the
  ground. See [#12][12] for a request to add him to the repository as a contributor.
- Add CHANGELOG to track major changes.

**Changed:**
- The naming of log files. See [#14][14] and [#15][15] for more information.
- Robust memory handling [#18][18] and [#20][20]
- README is now much more thorough [#15][15]

[12]: https://github.com/Snakemake-Profiles/lsf/issues/12
[14]: https://github.com/Snakemake-Profiles/lsf/issues/14
[15]: https://github.com/Snakemake-Profiles/lsf/pull/15
[18]: https://github.com/Snakemake-Profiles/lsf/issues/18
[20]: https://github.com/Snakemake-Profiles/lsf/pull/20
[5]: https://github.com/Snakemake-Profiles/lsf/pull/5
[7]: https://github.com/Snakemake-Profiles/lsf/issues/7
[11]: https://github.com/Snakemake-Profiles/lsf/pull/11
[9]: https://github.com/Snakemake-Profiles/lsf/pull/9
[36]: https://github.com/Snakemake-Profiles/lsf/issues/36
[39]: https://github.com/Snakemake-Profiles/lsf/issues/39
[0.1.0]: https://github.com/Snakemake-Profiles/lsf/releases/tag/0.1.0
