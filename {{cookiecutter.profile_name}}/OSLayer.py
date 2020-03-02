from pathlib import Path
import subprocess
from typing import Tuple


class OSLayer:
    """
    This class provides an abstract layer to communicating with the OS.
    Its main purpose is to enable OS operations mocking, so we don't actually need to make file operations or create
    processes.
    """
    @staticmethod
    def mkdir(directory: Path):
        directory.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def remove_file(file: Path):
        if file.exists():
            file.unlink()

    @staticmethod
    def run_process_and_get_output_and_error_stream(cmd: str) -> Tuple[str, str]:
        completed_process = subprocess.run(
            cmd, check=True, shell=True, capture_output=True
        )
        return completed_process.stdout.decode().strip(), completed_process.stderr.decode().strip()

    @staticmethod
    def print(string: str):
        print(string)

