# Snakemake sync bsub profile

[Snakemake profile](https://snakemake.readthedocs.io/en/stable/executable.html#profiles) for running jobs on bsub cluster using synchronisation.
Inspired by [jaicher/snakemake-sync-bq-sub][original].  

Deploy using [cookiecutter][cookiecutter-repo] (easily installed using conda or
pip) by running:

[original]: https://github.com/jaicher/snakemake-sync-bq-sub

[cookiecutter-repo]: https://github.com/audreyr/cookiecutter

```sh
# make sure configuration directory snakemake looks for profiles in exists
mkdir -p ~/.config/snakemake
# use cookiecutter to create a profile in the config directory
cookiecutter --output-dir ~/.config/snakemake gh:mbhall88/snakemake-bsub
```

This command will prompt for parameters to set. It will ask to change default snakemake
parameters, log directories. It will ask for a default queue for job
submissions (if left empty, by default it will not add a flag for the queue).
It will finally ask what the desired profile name is.

Once complete, this will allow you to run Snakemake with the cluster
configuration using the `--profile` flag. For example, if the profile name
was `bsub`, then you can run:

```sh
snakemake --profile bsub {...}
```

## Specification of resources/cluster settings

Individual snakemake rules can have the following parameters specified in the
Snakemake file:

-   `threads`: the number of threads needed for the job. If not specified,
    assumed to be 1.
-   `resources`
    -   `mem_mb`: the memory required for the rule in megabytes, which will be
        requested if present

A cluster configuration can be provided to specify additional information:

-   `mem_mb`: the memory that will be requested for the rule in megabytes.
    Overridden by `resources.mem_mb`. If neither provided, use a default value (in
    cookiecutter configuration).
-   `queue`: override the default queue for this job.
-   `logdir`: override the default cluster log directory for this job.
-   `output`: override the default name of stdout logfile
-   `error`: override the default name of stderr logfile
-   `jobname`: override the default name of the job
