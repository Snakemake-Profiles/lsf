#!/usr/bin/env python3

import subprocess
import sys
import time
from typing import Tuple

WAIT_BETWEEN_TRIES = 5
TRY_TIMES = 3
SUCCESS = "success"
RUNNING = "running"
FAILED = "failed"
STATUS_TABLE = {
    "PEND": RUNNING,
    "RUN": RUNNING,
    "DONE": SUCCESS,
    "PSUSP": RUNNING,
    "USUSP": RUNNING,
    "SSUSP": RUNNING,
    "WAIT": RUNNING,
    "EXIT": FAILED,
    "POST_DONE": SUCCESS,
    "POST_ERR": FAILED,
    "UNKWN": RUNNING,
}


def get_status_for_snakemake(job_status: str) -> str:
    status = STATUS_TABLE.get(job_status, "unknown")

    if status == "unknown":
        print(
            "Got an unknown job status: {} \nDefaulting to '{}'...".format(
                job_status, FAILED
            ),
            file=sys.stderr,
        )
        status = FAILED

    return status


def query_status(jobid: int) -> Tuple[str, str]:
    cmd = "bjobs -o 'stat' -noheader {}".format(jobid)
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    out, err = proc.communicate()

    return out.decode().strip(), err.decode().strip()


def query_status_failed(stderr: str, jobid: int) -> bool:
    return stderr.startswith("Job <{}> is not found".format(jobid))


def main():
    jobid = int(sys.argv[1])

    stdout, stderr = query_status(jobid)
    stdout_is_empty = not stdout.strip()

    tries = 0
    while (query_status_failed(stderr, jobid) or stdout_is_empty) and tries < TRY_TIMES:
        time.sleep(WAIT_BETWEEN_TRIES)
        stdout, stderr = query_status(jobid)
        stdout_is_empty = not stdout.strip()
        tries += 1

    job_status = stdout
    status_for_snakemake = get_status_for_snakemake(job_status)

    print(status_for_snakemake)


if __name__ == "__main__":
    main()
