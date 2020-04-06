#!/usr/bin/env python3
import re
import subprocess
import sys
from enum import Enum
from pathlib import Path
from typing import List

from snakemake.utils import read_job_properties

if not __name__.startswith("tests.src."):
    sys.path.append(str(Path(__file__).parent.absolute()))
    from OSLayer import OSLayer
    from CookieCutter import CookieCutter
else:
    from .OSLayer import OSLayer
    from .CookieCutter import CookieCutter


class BsubInvocationError(Exception):
    pass


class JobidNotFoundError(Exception):
    pass


class MemoryUnits(Enum):
    """See https://www.ibm.com/support/knowledgecenter/en/SSWRJV_10.1.0/lsf_command_ref/bsub.__r.1.html
    for valid units.
    """

    KB = "KB"
    MB = "MB"
    GB = "GB"
    TB = "TB"
    PB = "PB"
    EB = "EB"
    ZB = "ZB"


class Submitter:
    def __init__(self, argv: List[str], memory_units: MemoryUnits = MemoryUnits.KB):
        self._jobscript = argv[-1]
        self._cluster_cmd = " ".join(argv[1:-1])
        self._job_properties = read_job_properties(self._jobscript)
        self.random_string = OSLayer.get_uuid4_string()
        self._memory_units = memory_units

    @property
    def jobscript(self) -> str:
        return self._jobscript

    @property
    def job_properties(self) -> dict:
        return self._job_properties

    @property
    def cluster(self) -> dict:
        return self.job_properties.get("cluster", dict())

    @property
    def threads(self) -> int:
        return self.job_properties.get("threads", CookieCutter.get_default_threads())

    @property
    def resources(self) -> dict:
        return self.job_properties.get("resources", dict())

    @property
    def mem_mb(self) -> int:
        return self.resources.get(
            "mem_mb", self.cluster.get("mem_mb", CookieCutter.get_default_mem_mb())
        )

    @property
    def memory_units(self) -> str:
        return self._memory_units.value

    @property
    def resources_cmd(self) -> str:
        return (
            "-M {mem_mb}{units} -n {threads} "
            "-R 'select[mem>{mem_mb}{units}] rusage[mem={mem_mb}{units}] span[hosts=1]'"
        ).format(mem_mb=self.mem_mb, threads=self.threads, units=self.memory_units)

    @property
    def wildcards(self) -> dict:
        return self.job_properties.get("wildcards", dict())

    @property
    def wildcards_str(self) -> str:
        return (
            ".".join("{}={}".format(k, v) for k, v in self.wildcards.items())
            or "unique"
        )

    @property
    def rule_name(self) -> str:
        return self.job_properties.get("rule", "rule_name")

    @property
    def groupid(self) -> str:
        return self.job_properties.get("groupid", "group")

    @property
    def is_group_jobtype(self) -> bool:
        return self.job_properties.get("type", "") == "group"

    @property
    def jobname(self) -> str:
        if self.is_group_jobtype:
            return "{groupid}_{jobid}".format(groupid=self.groupid, jobid=self.jobid)
        return self.cluster.get(
            "jobname",
            "{rule_name}.{wildcards_str}".format(
                rule_name=self.rule_name, wildcards_str=self.wildcards_str
            ),
        )

    @property
    def jobid(self) -> int:
        if self.is_group_jobtype:
            return int(self.job_properties.get("jobid", "").split("-")[0])
        return int(self.job_properties.get("jobid"))

    @property
    def logdir(self) -> Path:
        return Path(self.cluster.get("logdir", CookieCutter.get_log_dir()))

    @property
    def outlog(self) -> Path:
        return self.logdir / "{jobid}_{random_string}.out".format(
            jobid=self.jobid, random_string=self.random_string
        )

    @property
    def errlog(self) -> Path:
        return self.logdir / "{jobid}_{random_string}.err".format(
            jobid=self.jobid, random_string=self.random_string
        )

    @property
    def jobinfo_cmd(self) -> str:
        return '-o "{out_log}" -e "{err_log}" -J "{jobname}"'.format(
            out_log=self.outlog, err_log=self.errlog, jobname=self.jobname
        )

    @property
    def queue(self) -> str:
        return self.cluster.get("queue", "")

    @property
    def queue_cmd(self) -> str:
        return "-q {}".format(self.queue) if self.queue else ""

    @property
    def cluster_cmd(self) -> str:
        return self._cluster_cmd

    @property
    def submit_cmd(self) -> str:
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
        OSLayer.remove_file(self.outlog)
        OSLayer.remove_file(self.errlog)

    def _submit_cmd_and_get_external_job_id(self) -> int:
        output_stream, error_stream = OSLayer.run_process(self.submit_cmd)
        match = re.search(r"Job <(\d+)> is submitted", output_stream)
        jobid = match.group(1)
        return int(jobid)

    def _get_parameters_to_status_script(self, external_job_id: int) -> str:
        return "{external_job_id} {outlog}".format(
            external_job_id=external_job_id, outlog=self.outlog
        )

    def submit(self):
        self._create_logdir()
        self._remove_previous_logs()  # we could be very unlucky of having the same 64-length random string with the same jobid
        try:
            external_job_id = self._submit_cmd_and_get_external_job_id()
            parameters_to_status_script = self._get_parameters_to_status_script(
                external_job_id
            )
            OSLayer.print(parameters_to_status_script)
        except subprocess.CalledProcessError as error:
            raise BsubInvocationError(error)
        except AttributeError as error:
            raise JobidNotFoundError(error)


if __name__ == "__main__":
    memory_units = MemoryUnits.MB
    lsf_submit = Submitter(sys.argv, memory_units=memory_units)
    lsf_submit.submit()
