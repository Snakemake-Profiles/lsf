# CHANGELOG

<!--- Please follow these guidelines https://keepachangelog.com/en/1.0.0/ --->

This document tracks changes to the `master` branch of the profile.

## 09/04/2020



**Added:**  
- Look at the log file if `bsub` returns an empty job status. See [#5][5] for more information.
- Allow specifying per-rule cluster resource settings (similar to deprecated cluster config). See [#15][15] and [#7][7] for more information.
- Added a `CONTRIBUTING.md` document [#15][15]
- TESTS!! A big thanks to [@leoisl](https://github.com/leoisl) for getting this off the ground. See [#12][12] for a request to add him to the repository as a contributor.
- Add CHANGELOG to track major changes.

**Changed:**
- The naming of log files. See [#14][14] and [#15][15] for more information.
- Explicitly set memory units when submitting as some clusters have different defaults [#9][9]  and [#11][11]
- README is now much more thorough [#15][15]

[5]: https://github.com/Snakemake-Profiles/snakemake-lsf/pull/5
[7]: https://github.com/Snakemake-Profiles/snakemake-lsf/issues/7
[9]: https://github.com/Snakemake-Profiles/snakemake-lsf/pull/9
[11]: https://github.com/Snakemake-Profiles/snakemake-lsf/pull/11
[12]: https://github.com/Snakemake-Profiles/snakemake-lsf/issues/12
[14]: https://github.com/Snakemake-Profiles/snakemake-lsf/issues/14
[15]: https://github.com/Snakemake-Profiles/snakemake-lsf/pull/15
