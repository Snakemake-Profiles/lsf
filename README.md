# Snakemake sync bsub profile

[Snakemake profile][profile] for running jobs on a [bsub][bsub] cluster.
Inspired by [jaicher/snakemake-sync-bq-sub][original].  

Deploy using [cookiecutter][cookiecutter-repo] (easily installed using conda or
pip) by running:

[original]: https://github.com/jaicher/snakemake-sync-bq-sub
[profile]: https://snakemake.readthedocs.io/en/stable/executable.html#profiles
[bsub]: https://www.ibm.com/support/knowledgecenter/en/SSETD4_9.1.2/lsf_command_ref/bsub.1.html
[cookiecutter-repo]: https://github.com/audreyr/cookiecutter

```sh
# make sure configuration directory snakemake looks for profiles in exists
mkdir -p ~/.config/snakemake
# use cookiecutter to create a profile in the config directory
cookiecutter --output-dir ~/.config/snakemake gh:mbhall88/snakemake-bsub
```

This command will prompt for parameters to set. It will ask to change some default snakemake
parameters. For information about the parameters see the [docs][snakemake_params].  
It will ask for a default queue for job submissions (if left empty, by default it will not add a flag for the queue) and the directory to save log files to.
It will finally ask what the desired profile name is.

[snakemake_params]: https://snakemake.readthedocs.io/en/stable/executable.html#all-options

Once complete, this will allow you to run snakemake with the cluster
configuration using the `--profile` flag. For example, if the profile name
was `bsub`, then you can run:

```sh
snakemake --profile bsub {...}
```

and pass any other valid snakemake options.

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
