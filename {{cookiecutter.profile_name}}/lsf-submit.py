#!/usr/bin/env python3
"""
lsf-submit.py

Script to wrap bsub sync command for Snakemake. Uses the following job or
cluster parameters:

+ `threads`
+ `resources`
    - `mem_mb`: Expected memory requirements in megabytes. Overrides
      cluster.mem_mb
+ `cluster`
    - `mem_mb`: Memory that will be requested for the cluster for the job.
      Overriden by resources.mem_mb, if present.
      `resources`
    - `queue`: Which queue to run job on
    - `logdir`: Where to log stdout/stderr from cluster command
    - `output`: Name of stdout logfile
    - `error`: Name of stderr logfile
    - `jobname`: Job name (with wildcards)

Author: Michael B Hall
Adapted from: https://github.com/jaicher/snakemake-sync-bq-sub
"""

import sys
import subprocess
from pathlib import Path
from snakemake.utils import read_job_properties
from typing import Tuple


DEFAULT_NAME = "jobname"


def generate_resources_command(job_properties: dict) -> str:
    threads = job_properties.get("threads", int({{cookiecutter.default_threads}}))
    resources = job_properties.get("resources", dict())
    mem_mb = resources.get(
        "mem_mb", cluster.get("mem_mb", int({{cookiecutter.default_mem_mb}}))
    )
    return (
        "-M {mem_mb} -n {threads} "
        "-R 'select[mem>{mem_mb}] rusage[mem={mem_mb}] span[hosts=1]'"
    ).format(mem_mb=mem_mb, threads=threads)


def get_job_name(job_properties: dict) -> str:
    """Get the group or rule name. If neither exists, use the DEFAULT_NAME
    NOTE: if group is present rule is not valid therefore group must come before rule
    """
    if job_properties.get("type", "") == "group":
        groupid = job_properties.get("groupid", "group")
        jobid = job_properties.get("jobid", "").split("-")[0]
        jobname = "{groupid}_{jobid}".format(groupid=groupid, jobid=jobid)
    else:
        wildcards = job_properties.get("wildcards", dict())
        wildcards_str = (
            ".".join("{}={}".format(k, v) for k, v in wildcards.items()) or "unique"
        )
        name = job_properties.get("rule", "") or DEFAULT_NAME
        jobname = cluster.get("jobname", "{0}.{1}".format(name, wildcards_str))

    return jobname


def get_outlog_errorlog_and_jobname (job_properties: dict) -> Tuple[str, str, str]:
    log_dir = Path(cluster.get("logdir", "{{cookiecutter.default_cluster_logdir}}"))
    log_dir.mkdir(parents=True, exist_ok=True)

    jobname = get_job_name(job_properties)
    jobid = job_properties.get("jobid")
   
    out_log = log_dir / "{}.out".format(jobid)
    out_log_parent = out_log.parent
    out_log_parent.mkdir(parents=True, exist_ok=True)
    if out_log.exists():
        out_log.unlink()

    err_log = log_dir / "{}.err".format(jobid)
    err_log_parent = err_log.parent
    err_log_parent.mkdir(parents=True, exist_ok=True)
    if err_log.exists():
        err_log.unlink()

    return out_log, err_log, jobname


jobscript = sys.argv[-1]
job_properties = read_job_properties(jobscript)
cluster = job_properties.get("cluster", dict())

out_log, err_log, jobname = get_outlog_errorlog_and_jobname(job_properties)
jobinfo_cmd = '-o "{out_log}" -e "{err_log}" -J "{jobname}"'.format(out_log=out_log, err_log=err_log, jobname=jobname)

resources_cmd = generate_resources_command(job_properties)

queue = cluster.get("queue", "")
queue_cmd = "-q {}".format(queue) if queue else ""

cluster_cmd = " ".join(sys.argv[1:-1])

# command to submit to cluster
submit_cmd = "bsub {resources} {job_info} {queue} {cluster} {jobscript}".format(
    resources=resources_cmd,
    job_info=jobinfo_cmd,
    queue=queue_cmd,
    cluster=cluster_cmd,
    jobscript=jobscript,
)


try:
    response = subprocess.run(
        submit_cmd, check=True, shell=True, stdout=subprocess.PIPE
    )
except subprocess.CalledProcessError as error:
    raise error

print(out_log)
