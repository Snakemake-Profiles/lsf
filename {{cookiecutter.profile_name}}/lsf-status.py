#!/usr/bin/env python3

import sys

SUCCESS = "success"
RUNNING = "running"
FAILED = "failed"

def main():
    out_log = sys.argv[1]

    try:
        with open(out_log) as out_log_filehandler:
            lines = [line.strip() for line in out_log_filehandler.readlines()]
        resource_summary_usage_line_index = lines.index("Resource usage summary:")
        status_line = lines[resource_summary_usage_line_index-2]
        assert status_line.startswith("Exited with exit code") or status_line == "Successfully completed."
        if status_line == "Successfully completed.":
            print(SUCCESS)
        else:
            print(FAILED)
    except (FileNotFoundError, ValueError):
        print(RUNNING)



if __name__ == "__main__":
    main()
