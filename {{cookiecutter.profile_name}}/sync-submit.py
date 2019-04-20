#!/usr/bin/env python
"""
sync-submit.py

Script to wrap bsub/qsub sync command for Snakemake. Uses the following job or
cluster parameters:

+ `threads`
+ `resources`
    - `mem_mb`: Expected memory requirements in megabytes
+ `cluster`
    - `mem_mb`: Expected memory requirements in megabytes. Overrides
      `resources`
    - `queue`: Which queue to run job on
    - `logdir`: Where to log stdout/stderr from cluster command
    - `output`: Name of stdout logfile
    - `error`: Name of stderr logfile
    - `jobname`: Job name (with wildcards)

Author: Joseph K Aicher
"""

import sys  # for command-line arguments (get jobscript)
from pathlib import Path  # for path manipulation
from snakemake.utils import read_job_properties  # get info from jobscript
from snakemake.shell import shell  # to run shell command nicely

# get the jobscript (last argument)
jobscript = sys.argv[-1]
# read the jobscript and get job properties
job = read_job_properties(jobscript)

# get the cluster properties
cluster = job.get("cluster", dict())

# get job information
# get the rule
rule = job.get("rule", "jobname")
# get the wildcards
wildcards = job.get("wildcards", dict())
wildcards_str = ",".join("{}={}".format(k, v) for k, v in wildcards.items())
if not wildcards_str:
    # if there aren't wildcards, this is a unique rule
    wildcards_str = "unique"

# get resources information
# get the number of threads the job wants
threads = job.get("threads", 1)
# get the resource properties
resources = job.get("resources", dict())
# get the memory usage in megabytes that we will request
mem_mb = cluster.get(
    "mem_mb",  # first see if it's in the cluster configuration
    # if not, check if the job itself gave its expected use
    resources.get(
        "mem_mb",  # request what the job says, if it says anything
        int({{cookiecutter.default_mem_mb}})  # otherwise, use default value
    )
)
mem_per_thread = round(mem_mb / threads, 2)  # per thread...

# determine names to pass through for job name, logfiles
log_dir = cluster.get("logdir", "{{cookiecutter.default_cluster_logdir}}")
# get the name of the job
jobname = cluster.get("jobname", "{0}.{1}".format(rule, wildcards_str))
# get the output file name
out_log = cluster.get("output", "{}.out".format(jobname))
err_log = cluster.get("error", "{}.err".format(jobname))
# get logfile paths
out_log_path = str(Path(log_dir).joinpath(out_log))
err_log_path = str(Path(log_dir).joinpath(err_log))

# get the queue to run the job on
queue = cluster.get("queue", "{{cookiecutter.default_queue}}")

# set name/log information
jobinfo_cmd = {
    "bsub": (
        "-o {out_log_path:q} -e {err_log_path:q}"
        " -J {jobname:q}"
    ),
    "qsub": (
        "-o {out_log_path:q} -e {err_log_path:q}"
        " -N {jobname:q}"
    )
}["{{cookiecutter.cluster}}"]


# set up resources part of command
resources_cmd = {
    "bsub": (
        "-M {mem_mb} -n {threads}"
        " -R 'span[hosts=1] rusage [mem={mem_mb}]'"
    ),
    "qsub": (
        # shared memory processes, preferentially on consecutive cores
        "-pe smp {threads} -binding linear:{threads}"
        # memory limit and memory request
        " -l h_vmem={mem_per_thread}M"
        " -l m_mem_free={mem_per_thread}M"
    )
}["{{cookiecutter.cluster}}"]

# get queue part of command (if empty, don't put in anything)
queue_cmd = "-q {queue}" if queue else ""

# get cluster commands to pass through, if any
cluster_cmd = " ".join(sys.argv[1:-1])

# get command to do cluster sync
sync_cmd = {
    "bsub": "bsub -K",
    "qsub": "qsub -terse -cwd -sync y"
}["{{cookiecutter.cluster}}"]

# run commands
shell(
    # sync command (bsub/qsub)
    sync_cmd
    # specify required threads/resources
    + " " + resources_cmd
    # specify job name, output/error logfiles
    + " " + jobinfo_cmd
    # specify queue
    + " " + queue_cmd
    # put in pass-through commands
    + " " + cluster_cmd
    # finally, the jobscript
    + " {jobscript}"
)
