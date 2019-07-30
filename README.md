# Snakemake LSF profile

[Snakemake profile][profile] for running jobs on a [LSF][lsf] cluster.
Inspired by [jaicher/snakemake-sync-bq-sub][original].  

Deploy using [cookiecutter][cookiecutter-repo] (easily installed using conda or
pip) by running:

[original]: https://github.com/jaicher/snakemake-sync-bq-sub
[profile]: https://snakemake.readthedocs.io/en/stable/executable.html#profiles
[lsf]: https://www.ibm.com/support/knowledgecenter/en/SSETD4_9.1.2/lsf_command_ref/bsub.1.html
[cookiecutter-repo]: https://github.com/audreyr/cookiecutter

```sh
# make sure configuration directory snakemake looks for profiles in exists
mkdir -p ~/.config/snakemake
# use cookiecutter to create a profile in the config directory
cookiecutter --output-dir ~/.config/snakemake gh:mbhall88/snakemake-lsf
```

This command will prompt for some default snakemake
parameters. For information about the parameters see the [docs][snakemake_params].  
**Ensure the default cluster log directory you set exists before running the pipeline**.  


[snakemake_params]: https://snakemake.readthedocs.io/en/stable/executable.html#all-options

Once complete, this will allow you to run snakemake with the cluster
profile using the `--profile` flag. For example, if the profile name
was `lsf`, then you can run:

```sh
snakemake --profile lsf [options]
```

and pass any other valid snakemake options.

## Specification of resources/cluster settings

Individual snakemake rules can have the following parameters specified in the
Snakemake file:

-   `threads`: the number of threads needed for the job. If not specified, will 
    default to the amount you set when initialising from `cookiecutter`.
-   `resources`
    -   `mem_mb`: the memory required for the rule in megabytes. If not specified, will 
    default to the amount you set when initialising from `cookiecutter`.

A cluster configuration can be provided to specify additional information that overrides 
the profile defaults:

-   `queue`: override the default queue for this job.
-   `logdir`: override the default cluster log directory for this job.
-   `output`: override the default name of stdout logfile
-   `error`: override the default name of stderr logfile
-   `jobname`: override the default name of the job
