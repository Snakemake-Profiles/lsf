#!/usr/bin/env python3

import sys
import time
from typing import List
from .OSLayer import OSLayer
from subprocess import CalledProcessError


class BjobsError(Exception):
    pass


class LSF_Status_Checker:
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

    def __init__(self, jobid: int, outlog: str, WAIT_BETWEEN_TRIES: int = 5, TRY_TIMES: int = 3):
        self._jobid = jobid
        self._outlog = outlog
        self.WAIT_BETWEEN_TRIES = WAIT_BETWEEN_TRIES
        self.TRY_TIMES = TRY_TIMES

    @property
    def jobid(self):
        return self._jobid

    @property
    def outlog(self):
        return self._outlog

    @property
    def bjobs_query_cmd(self) -> str:
        return "bjobs -o 'stat' -noheader {jobid}".format(jobid=self.jobid)

    def _query_status_using_bjobs(self) -> str:
        output_stream, error_stream = OSLayer.run_process_and_get_output_and_error_stream(self.bjobs_query_cmd)

        stdout_is_empty = not output_stream.strip()
        if stdout_is_empty:
            raise BjobsError("bjobs error.\nstdout is empty.\nstderr = {stderr}".format(stderr=error_stream))

        return self.STATUS_TABLE.get(output_stream)

    def _get_lines_of_log_file(self) -> List[str]:
        with open(self.outlog) as out_log_filehandler:
            lines = [line.strip() for line in out_log_filehandler.readlines()]
        return lines

    def _query_status_using_log(self) -> str:
        try:
            log_lines = self._get_lines_of_log_file()
            resource_summary_usage_line_index = log_lines.index("Resource usage summary:")
            status_line = log_lines[resource_summary_usage_line_index - 2]
            assert status_line.startswith("Exited with exit code") or status_line == "Successfully completed."
            if status_line == "Successfully completed.":
                return self.SUCCESS
            else:
                return self.FAILED
        except (FileNotFoundError, ValueError):
            return self.RUNNING

    # NB: only this function is tested - we just want to test the behaviour of get_status()
    # All the other functions are also tested, as we mock the OSLayer
    def get_status(self) -> str:
        status = None
        for _ in range(self.TRY_TIMES):
            try:
                status = self._query_status_using_bjobs()
                break  # succeeded on getting the status
            except BjobsError as error:
                print(error, file=sys.stderr)
                time.sleep(self.WAIT_BETWEEN_TRIES)
            except KeyError as error:
                print("Unknown job status: {error}".format(error=error), file=sys.stderr)
                time.sleep(self.WAIT_BETWEEN_TRIES)
            except CalledProcessError as error:
                print("Error on calling bjobs: {error}".format(error=error), file=sys.stderr)
                time.sleep(self.WAIT_BETWEEN_TRIES)

        bjobs_failed = status is None
        if bjobs_failed:
            status = self._query_status_using_log()

        return status


if __name__ == "__main__":
    jobid = int(sys.argv[1])
    outlog = sys.argv[1]
    lsf_status_checker = LSF_Status_Checker(jobid, outlog)
    print(lsf_status_checker.get_status())
