#!/usr/bin/env python3

import sys
import time
from pathlib import Path
from subprocess import CalledProcessError
from typing import List

if not __name__.startswith("tests.src."):
    sys.path.append(str(Path(__file__).parent.absolute()))
    from OSLayer import OSLayer
    from CookieCutter import CookieCutter
else:
    from .OSLayer import OSLayer
    from .CookieCutter import CookieCutter


class BjobsError(Exception):
    pass


class UnknownStatusLine(Exception):
    pass


UNKNOWN = "UNKWN"


class StatusChecker:
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
        "ZOMBI": FAILED,
    }

    def __init__(
        self,
        jobid: int,
        outlog: str,
        wait_between_tries: float = 0.001,
        max_status_checks: int = 1,
        kill_unknown: bool = False,
    ):
        self._jobid = jobid
        self._outlog = outlog
        self.wait_between_tries = wait_between_tries
        self.max_status_checks = max_status_checks
        self.kill_unknown = kill_unknown

    @property
    def jobid(self) -> int:
        return self._jobid

    @property
    def outlog(self) -> str:
        return self._outlog

    @property
    def bjobs_query_cmd(self) -> str:
        return "bjobs -o 'stat' -noheader {jobid}".format(jobid=self.jobid)

    def _query_status_using_bjobs(self) -> str:
        output_stream, error_stream = OSLayer.run_process(self.bjobs_query_cmd)

        stdout_is_empty = not output_stream.strip()
        if stdout_is_empty:
            raise BjobsError(
                "bjobs error.\nstdout is empty.\nstderr = {stderr}".format(
                    stderr=error_stream
                )
            )

        if output_stream == UNKNOWN and self.kill_unknown:
            print(
                "[lsf profile warning] {unknown} job status detected for {jobid}. "
                "Killing job...".format(unknown=UNKNOWN, jobid=self.jobid),
                file=sys.stderr,
            )
            self._kill_unknown_job()
            return self.FAILED
        elif output_stream == UNKNOWN and not self.kill_unknown:  # i.e. wait
            return self.RUNNING

        return self.STATUS_TABLE[output_stream]

    def _get_tail_of_log_file(self) -> List[str]:
        # 30 lines gives us the whole LSF completion summary
        tail = OSLayer.tail(self.outlog, num_lines=30)
        return [line.decode().strip() for line in tail]

    def _kill_unknown_job(self):
        kill_cmd = "bkill -r {}".format(self.jobid)
        _ = OSLayer.run_process(kill_cmd)

    def _query_status_using_log(self) -> str:
        try:
            log_tail = self._get_tail_of_log_file()
            resource_summary_usage_line_index = log_tail.index(
                "Resource usage summary:"
            )
            status_line = log_tail[resource_summary_usage_line_index - 2]

            if status_line == "Successfully completed.":
                return self.SUCCESS
            elif status_line.startswith("Exited with exit code"):
                return self.FAILED
            else:
                raise UnknownStatusLine(status_line)
        except (FileNotFoundError, ValueError):
            return self.RUNNING

    def get_status(self) -> str:
        status = None
        for _ in range(self.max_status_checks):
            try:
                status = self._query_status_using_bjobs()
                break  # succeeded in getting the status
            except BjobsError as error:
                print(
                    "[Predicted exception] BjobsError: {error}".format(error=error),
                    file=sys.stderr,
                )
                print("Resuming...", file=sys.stderr)
                time.sleep(self.wait_between_tries)
            except KeyError as error:
                print(
                    "[Predicted exception] Unknown job status: {error}".format(
                        error=error
                    ),
                    file=sys.stderr,
                )
                print("Resuming...", file=sys.stderr)
                time.sleep(self.wait_between_tries)
            except CalledProcessError as error:
                print(
                    "[Predicted exception] Error calling bjobs: {error}".format(
                        error=error
                    ),
                    file=sys.stderr,
                )
                print("Resuming...", file=sys.stderr)
                time.sleep(self.wait_between_tries)

        bjobs_failed = status is None
        if bjobs_failed:
            print(
                "bjobs failed {try_times} times. Checking log...".format(
                    try_times=self.max_status_checks
                ),
                file=sys.stderr,
            )
            status = self._query_status_using_log()

        return status


if __name__ == "__main__":
    jobid = int(sys.argv[1])
    outlog = sys.argv[2]
    if CookieCutter.get_unknwn_behaviour().lower() == "wait":
        kill_unknown = False
    elif CookieCutter.get_unknwn_behaviour().lower() == "kill":
        kill_unknown = True
    else:
        raise ValueError(
            "Unknown value for {}_behaviour: {}".format(
                UNKNOWN, CookieCutter.get_unknwn_behaviour()
            )
        )
    lsf_status_checker = StatusChecker(jobid, outlog, kill_unknown=kill_unknown)
    print(lsf_status_checker.get_status())
