# Snakemake LSF profile

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/Snakemake-Profiles/lsf/Python_package)](https://github.com/Snakemake-Profiles/lsf/actions)
[![Code coverage](https://codecov.io/gh/Snakemake-Profiles/lsf/branch/master/graph/badge.svg)](https://codecov.io/gh/Snakemake-Profiles/lsf)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Python versions](https://img.shields.io/badge/Python%20versions->=3.5-blue)
![License](https://img.shields.io/github/license/Snakemake-Profiles/lsf)

> 📢**NOTICE: We are seeking volunteers to maintain this repository as the current maintainers no longer use LSF. See [this issue](https://github.com/Snakemake-Profiles/lsf/issues/57).**📢

[Snakemake profile][profile] for running jobs on an [LSF][lsf] cluster.

[TOC]: #

## Table of Contents
- [Install](#install)
  - [Dependencies](#dependencies)
  - [Profile](#profile)
- [Usage](#usage)
  - [Standard rule-specific cluster resource settings](#standard-rule-specific-cluster-resource-settings)
  - [Non-standard rule-specific cluster resource settings](#non-standard-rule-specific-cluster-resource-settings)
- [Known Issues](#known-issues)
- [Contributing](#contributing)

## Install

### Dependencies

This profile is deployed using [Cookiecutter][cookiecutter-repo]. If you do not have
`cookiecutter` installed it can be easily installed using `conda` or `pip` by running:

```bash
pip install --user cookiecutter
# or
conda install -c conda-forge cookiecutter
```

If neither of these methods suits you, then visit the [installation
documentation][cc-install] for other options.

### Profile

Download and set up the profile on your cluster

```bash
# create configuration directory that snakemake searches for profiles
profile_dir="${HOME}/.config/snakemake"
mkdir -p "$profile_dir"
# use cookiecutter to create the profile in the config directory
template="gh:Snakemake-Profiles/lsf"
cookiecutter --output-dir "$profile_dir" "$template"
```

You will then be prompted to set some default parameters.

#### `LSF_UNIT_FOR_LIMITS`

**Default**: `KB`  
**Valid options:** `KB`, `MB`, `GB`, `TB`, `PB`, `EB`, `ZB`

**⚠️IMPORTANT⚠️**: This **must** be set to the same as [`LSF_UNIT_FOR_LIMITS`][limits] on
your cluster. This value is stored in your cluster's [`lsf.conf`][lsf-conf] file. In
general, this file is located at `${LSF_ENVDIR}/lsf.conf`. So the easiest way to get
this value is to run the following:

```shell
grep '^LSF_UNIT_FOR_LIMITS' ${LSF_ENVDIR}/lsf.conf
```

You should get something along the lines of `LSF_UNIT_FOR_LIMITS=MB`. If this command
doesn't work, get in touch with your cluster administrator to find out the value.

As mentioned above, this is a very important parameter. It sets the scaling units to use
for resource limits. So, if this value is `MB` on your cluster, then when setting the
memory limit with `-M 1000` the value is taken as megabytes. As `snakemake` allows you
to set the memory for a rule with the `resources: mem_mb` parameter, it is important for
this profile to know whether this then needs to be converted into other units when
submitting jobs. See [here][18] for further information.

#### `UNKWN_behaviour`

**Default**: `wait`  
**Valid options**: `wait`, `kill`

When LSF returns a job status of `UNKWN` do you want to wait for the host the job is
running on to be contactable again - i.e. consider the job running - or kill it as
outlined [here][job_kill]?

#### `ZOMBI_behaviour`

**Default**: `ignore`  
**Valid options**: `ignore`, `kill`

When LSF returns a job status of `ZOMBI` do you want to ignore this (not clean it up) or
kill it as outlined [here][job_kill]? Regardless of the option chosen, the job is
considered failed.

#### `latency_wait`

**Default:** `5`

This sets the default `--latency-wait/--output-wait/-w` parameter in `snakemake`.  
From the `snakemake --help` menu

```text
  --latency-wait SECONDS, --output-wait SECONDS, -w SECONDS
                        Wait given seconds if an output file of a job is not
                        present after the job finished. This helps if your
                        filesystem suffers from latency (default 5).
```

#### `use_conda`

**Default**: `False`  
**Valid options:** `False`, `True`

This sets the default `--use-conda` parameter in `snakemake`.  
From the `snakemake --help` menu

```text
  --use-conda           If defined in the rule, run job in a conda
                        environment. If this flag is not set, the conda
                        directive is ignored.
```

#### `use_singularity`

**Default**: `False`  
**Valid options:** `False`, `True`

This sets the default `--use-singularity` parameter in `snakemake`.  
From the `snakemake --help` menu

```text
  --use-singularity     If defined in the rule, run job within a singularity
                        container. If this flag is not set, the singularity
                        directive is ignored.
```

#### `restart_times`

**Default**: `0`

This sets the default `--restart-times` parameter in `snakemake`.  
From the `snakemake --help` menu

```text
  --restart-times RESTART_TIMES
                        Number of times to restart failing jobs (defaults to
                        0).
```

#### `print_shell_commands`

**Default**: `False`  
**Valid options:** `False`, `True`

This sets the default ` --printshellcmds/-p` parameter in `snakemake`.  
From the `snakemake --help` menu

```text
  --printshellcmds, -p  Print out the shell commands that will be executed.
```

#### `jobs`

**Default**: `500`

This sets the default `--cores/--jobs/-j` parameter in `snakemake`.  
From the `snakemake --help` menu

```text
  --cores [N], --jobs [N], -j [N]
                        Use at most N cores in parallel. If N is omitted or
                        'all', the limit is set to the number of available
                        cores.
```

In the context of a cluster, `-j` denotes the number of jobs submitted to the cluster at
the same time<sup>[1][1]</sup>.

#### `default_mem_mb`

**Default**: `1024`

This sets the default memory, in megabytes, for a `rule` being submitted to the cluster
without `mem_mb` set under `resources`.

See [below](#standard-rule-specific-cluster-resource-settings) for how to overwrite this
in a `rule`.

#### `default_cluster_logdir`

**Default**: `"logs/cluster"`

This sets the directory under which cluster log files are written. The path is relative
to the working directory of the pipeline. If it does not exist, it will be created.

The log files for a given rule are organised into sub-directories. This is to avoid
having potentially thousands of files in one directory, as this can cause file system
issues.  
If you want to find the log files for a rule called `foo`, with wildcards
`sample=a,ext=fq` then this would be located at
`logs/cluster/foo/sample=a,ext=fq/jobid<jobid>-<uuid>.out` for the [standard
output][bsub-o] and with extension `.err` for the [standard error][bsub-e].  
`<jobid>` is the internal jobid used by `snakemake` and is the same across multiple
attempts at running the same rule.  
[`<uuid>`][uuid] is a random 28-digit, separated by `-`, and is specific to each attempt
at running a rule. So if a rule fails, and is restarted, the uuid will be different.

The reason for such a seemingly complex log-naming scheme is explained in
[Known Issues](#known-issues). However, you can override the name of the log files for a
specific rule by following the instructions
[below](#non-standard-rule-specific-cluster-resource-settings).

#### `default_queue`

**Default**: None

The default queue on the cluster to submit jobs to. If left unset, then the default on
your cluster will be used.  
The `bsub` parameter that this controls is [`-q`][bsub-q].

#### `default_project`

**Default**: None

The default project on the cluster to submit jobs with. If left unset, then the default on
your cluster will be used.

The `bsub` parameter that this controls is [`-P`][bsub-P].

#### `max_status_checks_per_second`

**Default**: `10`

This sets the default `--max-status-checks-per-second` parameter in `snakemake`.  
From the `snakemake --help` menu

```text
  --max-status-checks-per-second MAX_STATUS_CHECKS_PER_SECOND
                        Maximal number of job status checks per second,
                        default is 10, fractions allowed.
```

#### `max_jobs_per_second`

**Default**: `10`

This sets the default `--max-jobs-per-second` parameter in `snakemake`.  
From the `snakemake --help` menu

```text
  --max-jobs-per-second MAX_JOBS_PER_SECOND
                        Maximal number of cluster/drmaa jobs per second,
                        default is 10, fractions allowed.
```

#### `profile_name`

**Default**: `lsf`

The name to use for this profile. The directory for the profile is created as this name
i.e. `$HOME/.config/snakemake/<profile_name>`.  
This is also the value you pass to `snakemake --profile <profile_name>`.

## Usage

Once set up is complete, this will allow you to run snakemake with the cluster profile
using the `--profile` flag. For example, if the profile name was `lsf`, then you can
run:

```bash
snakemake --profile lsf [snakemake options]
```

and pass any other valid snakemake options.

### Standard rule-specific cluster resource settings

The following resources can be specified within a `rule`:

- `threads: <INT>` the number of threads needed for the job. If not specified, will
  [default to the amount you set when initialising](#default-threads) the profile.
- `resources:`
  - `mem_mb = <INT>`: the memory required for the rule, in megabytes. If not specified,
    will [default to the amount you set when initialising](#default-mem-mb) the profile.
  - `time_min: <INT>`: the runtime limit required for the rule, in minutes.

*NOTE: these settings will override the profile defaults.*

### Non-standard rule-specific cluster resource settings

Since the [deprecation of cluster configuration files][config-deprecate] the ability to
specify per-rule cluster settings is snakemake-profile-specific.

Per-rule configuration must be placed in a file called `lsf.yaml` and **must** be
located in the working directory for the pipeline. If you set `workdir` manually within
your workflow, the config file has to be in there.

***NOTE:** these settings are only valid for this profile and are not guaranteed to be
valid on non-LSF cluster systems.*

All settings are given with the `rule` name as the key, and the additional cluster
settings as a string ([scalar][yaml-collections]) or list
([sequence][yaml-collections]).

#### Examples

`Snakefile`

```python
rule foo:
    input: "foo.txt"
    output: "bar.txt"
    shell:
        "grep 'bar' {input} > {output}"

rule bar:
    input: "bar.txt"
    output: "file.out"
    shell:
        "echo blah > {output}"
```

`lsf.yaml`

```yaml
__default__:
  - "-P project2"
  - "-W 1:05"

foo:
  - "-P gpu"
  - "-gpu 'gpu resources'"
```

In this example, we specify a default (`__default__`) [project][bsub-P] (`-P`) and
[runtime limit][bsub-W] (`-W`) that will apply to all rules.  
We then override the project and, additionally, specify [GPU resources][bsub-gpu] for
the rule `foo`.

For those interested in the details, this will lead to a submission command, for `foo`
that looks something like

```
$ bsub [options] -P project2 -W 1:05 -P gpu -gpu 'gpu resources' ...
```

Although `-P` is provided twice, LSF uses the last instance.

```yaml
__default__: "-P project2 -W 1:05"

foo: "-P gpu -gpu 'gpu resources'"
```

The above is also a valid form of the previous example but **not recommended**.

#### Quote-escaping

Some LSF commands require multiple levels of quote-escaping.  
For example, to exclude a node from job submission which has non-alphabetic characters
in its name ([docs](https://www.ibm.com/support/knowledgecenter/SSWRJV_10.1.0/lsf_command_ref/bsub.__r.1.html?view=embed)): `bsub -R "select[hname!='node-name']"`.

You can specify this in `lsf.yaml` as:

```yaml
__default__:
    - "-R \"select[hname!='node-name']\""
```

## Known Issues

If running very large `snakemake` pipelines, or there are many workflow management
systems submitting and checking jobs at the same time on the same cluster, we have seen
examples where retrieval of the job state from LSF returns an empty status. This causes
problems as we do not know whether or not the job has passed/failed. In these
circumstances, the [status-checker][status-checker] will look at the log file for the
job to see if it is complete or still running. Thus, the reason for the seemingly
complex log file naming scheme. As the status-checker uses `tail` to get the status, if
the standard output log file of the job is very large, then status checking will be
slowed down as a result. If you run into these problems and the `tail` solution is no
feasible, the first suggestion would be to reduce `--max_status_checks_per_second` and
see if this helps.  
Please raise an issue if you experience this, and the log file check doesn't seem to
work.

## Contributing

Please refer to [`CONTRIBUTING.md`](CONTRIBUTING.md).

<!--Link References-->

[1]: https://snakemake.readthedocs.io/en/stable/executing/cluster-cloud.html#cluster-execution
[18]: https://github.com/Snakemake-Profiles/lsf/issues/18
[bsub-P]: https://www.ibm.com/support/knowledgecenter/en/SSWRJV_10.1.0/lsf_command_ref/bsub.__p.1.html
[bsub-W]: https://www.ibm.com/support/knowledgecenter/en/SSWRJV_10.1.0/lsf_command_ref/bsub.__w.1.html
[bsub-e]: https://www.ibm.com/support/knowledgecenter/en/SSWRJV_10.1.0/lsf_command_ref/bsub.e.1.html
[bsub-gpu]: https://www.ibm.com/support/knowledgecenter/en/SSWRJV_10.1.0/lsf_command_ref/bsub.gpu.1.html
[bsub-o]: https://www.ibm.com/support/knowledgecenter/en/SSWRJV_10.1.0/lsf_command_ref/bsub.o.1.html
[bsub-q]: https://www.ibm.com/support/knowledgecenter/en/SSWRJV_10.1.0/lsf_command_ref/bsub.q.1.html
[cc-install]: https://cookiecutter.readthedocs.io/en/1.7.0/installation.html
[config-deprecate]: https://snakemake.readthedocs.io/en/stable/snakefiles/configuration.html#cluster-configuration-deprecated
[cookiecutter-repo]: https://github.com/audreyr/cookiecutter
[job_kill]: https://www.ibm.com/support/knowledgecenter/SSWRJV_10.1.0/lsf_admin/job_kill_force.html
[limits]: https://www.ibm.com/support/knowledgecenter/en/SSWRJV_10.1.0/lsf_config_ref/lsf.conf.lsf_unit_for_limits.5.html
[lsf]: https://www.ibm.com/support/knowledgecenter/en/SSWRJV_10.1.0/lsf_welcome/lsf_welcome.html
[lsf-conf]: https://www.ibm.com/support/knowledgecenter/en/SSETD4_9.1.2/lsf_config_ref/lsf.conf.5.html
[profile]: https://snakemake.readthedocs.io/en/stable/executing/cli.html#profiles
[status-checker]: https://github.com/Snakemake-Profiles/lsf/blob/master/%7B%7Bcookiecutter.profile_name%7D%7D/lsf_status.py
[uuid]: https://docs.python.org/3.6/library/uuid.html
[yaml-collections]: https://yaml.org/spec/1.2/spec.html#id2759963
[leandro]: https://github.com/leoisl
[snakemake_params]: https://snakemake.readthedocs.io/en/stable/executable.html#all-options
