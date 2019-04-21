# Snakemake sync bsub/qsub profile

Snakemake cookiecutter profile for running jobs on bsub or qsub cluster using
synchronization. Deploy using [cookiecutter][cookiecutter-repo] by running:

   [cookiecutter-repo]: https://github.com/audreyr/cookiecutter

```
# make sure configuration directory snakemake looks for profiles in exists
mkdir -p ~/.config/snakemake
# use cookiecutter to create a profile in the config directory
cookiecutter --output-dir ~/.config/snakemake .
```

This command will prompt for parameters to set. In particular, it will ask a
choice between `bsub` or `qsub`. It will ask to change default snakemake
parameters, log directories. It will ask for a default queue for job
submissions (if left empty, by default it will not add a flag for the queue).
It will finally ask what the desired profile name is.

Once complete, this will allow you to run Snakemake with the cluster
configuration using the `--profile` flag. For example, if the profile name
was `cluster-sync`, then you can run:

```
snakemake --profile cluster-sync {...}
```

## Specification of resources/cluster settings

Individual snakemake rules can have the following parameters specified in the
Snakemake file:
+ `threads`: the number of threads needed for the job. If not specified,
  assumed to be 1.
+ `resources`
    - `mem_mb`: the memory required for the rule in megabytes, which will be
      requested if present

A cluster configuration can be provided to specify additional information:
+ `mem_mb`: the memory that will be requested for the rule in megabytes.
  Overriden by `resources.mem_mb`. If neither provided, use a default value (in
  cookiecutter configuration).
+ `queue`: override the default queue for this job.
+ `logdir`: override the default cluster log directory for this job.
+ `output`: override the default name of stdout logfile
+ `error`: override the default name of stderr logfile
+ `jobname`: override the default name of the job
