#!/usr/bin/env python3
import re
import shlex
import sys
from pathlib import Path
from typing import List

if not __name__.startswith("tests.src."):
    sys.path.append(str(Path(__file__).parent.absolute()))
    from OSLayer import OSLayer
else:
    from .OSLayer import OSLayer

KILL = "bkill"


def kill_jobs(ids_to_kill: List[str]):
    # we don't want to run bkill with no argument as this will kill the last job
    if any(ids_to_kill):
        cmd = "{} {}".format(KILL, " ".join(ids_to_kill))
        _ = OSLayer.run_process(cmd)


def parse_input() -> List[str]:
    # need to support quoted and unquoted jobid
    # see https://github.com/Snakemake-Profiles/lsf/issues/45
    split_args = shlex.split(" ".join(sys.argv[1:]))
    valid_ids = []
    for arg in map(str.strip, split_args):
        if re.fullmatch(r"\d+", arg):
            valid_ids.append(arg)

    return valid_ids


if __name__ == "__main__":
    jobids = parse_input()

    if jobids:
        kill_jobs(jobids)
    else:
        OSLayer.eprint(
            "[cluster-cancel error] Did not get any valid jobids to cancel..."
        )
