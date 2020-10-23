# CHANGELOG

<!--- Please follow these guidelines https://keepachangelog.com/en/1.0.0/ --->

This document tracks changes to the `master` branch of the profile.

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

[12]: https://github.com/Snakemake-Profiles/snakemake-lsf/issues/12
[14]: https://github.com/Snakemake-Profiles/snakemake-lsf/issues/14
[15]: https://github.com/Snakemake-Profiles/snakemake-lsf/pull/15
[18]: https://github.com/Snakemake-Profiles/snakemake-lsf/issues/18
[20]: https://github.com/Snakemake-Profiles/snakemake-lsf/pull/20
[5]: https://github.com/Snakemake-Profiles/snakemake-lsf/pull/5
[7]: https://github.com/Snakemake-Profiles/snakemake-lsf/issues/7
[11]: https://github.com/Snakemake-Profiles/snakemake-lsf/pull/11
[9]: https://github.com/Snakemake-Profiles/snakemake-lsf/pull/9

