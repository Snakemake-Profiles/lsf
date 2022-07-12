# CHANGELOG

<!--- Please follow these guidelines https://keepachangelog.com/en/1.0.0/ --->

This document tracks changes to the `master` branch of the profile.

## [Unreleased]

## [0.3.0] - 13/07/2022

### Added
- Exposed `max_status_check` and `wait_between_tries` for status checker [[#48][48]]

### Changed
- Cluster cancel is now a script instead of the `bkill` command in order to handle the log file paths that come with the job ID [[#55][55]]

## [0.2.0] - 28/05/2022

### Added

- Default project in cookiecutter
- Cluster cancel (`--cluster-cancel`) command (`bkill`)

### Removed

- Default threads in cookiecutter

### Changed

- Default project and queue will be removed from the submission command if they are present in the `lsf.yaml`

### Fixed

- Support quoted jobid from `snakemake>=v7.1.1` [[#45][45]]

## [0.1.2] - 01/04/2021

### Added

- Support for runtime resources [[#38][38]]

## [0.1.1] - 16/03/2021

### Added


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
[38]: https://github.com/Snakemake-Profiles/lsf/pull/38
[5]: https://github.com/Snakemake-Profiles/lsf/pull/5
[7]: https://github.com/Snakemake-Profiles/lsf/issues/7
[11]: https://github.com/Snakemake-Profiles/lsf/pull/11
[9]: https://github.com/Snakemake-Profiles/lsf/pull/9
[36]: https://github.com/Snakemake-Profiles/lsf/issues/36
[39]: https://github.com/Snakemake-Profiles/lsf/issues/39
[45]: https://github.com/Snakemake-Profiles/lsf/issues/45
[48]: https://github.com/Snakemake-Profiles/lsf/issues/48
[55]: https://github.com/Snakemake-Profiles/lsf/issues/55
[0.1.0]: https://github.com/Snakemake-Profiles/lsf/releases/tag/0.1.0
[0.1.1]: https://github.com/Snakemake-Profiles/lsf/releases/tag/0.1.1
[0.1.2]: https://github.com/Snakemake-Profiles/lsf/releases/tag/0.1.2
[0.2.0]: https://github.com/Snakemake-Profiles/lsf/releases/tag/0.2.0
[0.3.0]: https://github.com/Snakemake-Profiles/lsf/compare/0.2.0...0.3.0
[Unreleased]: https://github.com/Snakemake-Profiles/lsf/compare/0.3.0...HEAD

