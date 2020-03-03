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
from typing import List
from .CookieCutter import CookieCutter
from .OSLayer import OSLayer

# TODO: add a random string to the out/error log to avoid two different runs having the same jobid for different jobs (not sure jobs have always the same id)
# TODO: test trivial methods with a jobscript
# TODO: test the other methods with mock
# TODO: use https://stackoverflow.com/questions/22677280/checking-call-order-across-multiple-mocks


class LSF_Submit:
    def __init__(self, argv: List[str]):
        self._jobscript = argv[-1]
        self._cluster_cmd = " ".join(argv[1:-1])
        self._job_properties = read_job_properties(self._jobscript)

    @property
    def jobscript(self):
        return self._jobscript

    @property
    def job_properties(self):
        return self._job_properties

    @property
    def cluster(self):
        return self.job_properties.get("cluster", dict())

    @property
    def threads(self):
        return self.job_properties.get("threads", CookieCutter.get_default_threads())

    @property
    def resources(self):
        return self.job_properties.get("resources", dict())

    @property
    def mem_mb(self):
        return self.resources.get("mem_mb", self.cluster.get("mem_mb", CookieCutter.get_default_mem_mb()))

    @property
    def resources_cmd(self) -> str:
        return (
            "-M {mem_mb} -n {threads} "
            "-R 'select[mem>{mem_mb}] rusage[mem={mem_mb}] span[hosts=1]'"
        ).format(mem_mb=self.mem_mb, threads=self.threads)

    @property
    def wildcards(self):
        return self.job_properties.get("wildcards", dict())

    @property
    def wildcards_str(self):
        return ".".join("{}={}".format(k, v) for k, v in self.wildcards.items()) or "unique"

    @property
    def rule_name(self):
        return self.job_properties.get("rule", "rule_name")

    @property
    def groupid(self):
        return self.job_properties.get("groupid", "group")

    @property
    def is_group_jobtype(self):
        return self.job_properties.get("type", "") == "group"

    @property
    def jobname(self) -> str:
        if self.is_group_jobtype:
            return "{groupid}_{jobid}".format(groupid=self.groupid, jobid=self.jobid)
        else:
            return self.cluster.get("jobname",
                                    "{rule_name}.{wildcards_str}".format(rule_name=self.rule_name,
                                                                         wildcards_str=self.wildcards_str))

    @property
    def jobid(self):
        if self.is_group_jobtype:
            return self.job_properties.get("jobid", "").split("-")[0]
        else:
            return self.job_properties.get("jobid")

    @property
    def logdir(self):
        return Path(self.cluster.get("logdir", CookieCutter.get_log_dir()))

    @property
    def outlog(self):
        return self.logdir / "cluster_checkpoints/{jobid}.out".format(jobid=self.jobid)

    @property
    def errlog(self):
        return self.logdir / "cluster_checkpoints/{jobid}.err".format(jobid=self.jobid)

    @property
    def jobinfo_cmd(self):
        return '-o "{out_log}" -e "{err_log}" -J "{jobname}"'.format(out_log=self.outlog, err_log=self.errlog, jobname=self.jobname)

    @property
    def queue(self):
        return self.cluster.get("queue", "")

    @property
    def queue_cmd(self):
        return "-q {}".format(self.queue) if self.queue else ""

    @property
    def cluster_cmd(self):
        return self._cluster_cmd

    @property
    def submit_cmd(self):
        return "bsub {resources} {job_info} {queue} {cluster} {jobscript}".format(
                    resources=self.resources_cmd,
                    job_info=self.jobinfo_cmd,
                    queue=self.queue_cmd,
                    cluster=self.cluster_cmd,
                    jobscript=self.jobscript,
        )

    def _create_logdir(self):
        OSLayer.mkdir(self.logdir)

    def _remove_previous_logs(self):
        # TODO: might be interesting to keep the previous logs...
        OSLayer.remove_file(self.outlog)
        OSLayer.remove_file(self.errlog)

    def _submit_cmd_and_get_external_job_id(self):
        output_stream, error_stream = OSLayer.run_process_and_get_output_and_error_stream(self.submit_cmd)
        return output_stream

    def _get_information_to_status_script(self, external_job_id):
        return "{external_job_id} {outlog}".format(
            external_job_id=external_job_id,
            outlog=self.outlog
        )

    def submit(self):
        self._create_logdir()
        self._remove_previous_logs()
        try:
            external_job_id = self._submit_cmd_and_get_external_job_id()
            information_to_status_script = self._get_information_to_status_script(external_job_id)
            OSLayer.print(information_to_status_script)
        except subprocess.CalledProcessError as error:
            raise error


if __name__ == "__main__":
    lsf_submit = LSF_Submit(sys.argv)
    lsf_submit.submit()