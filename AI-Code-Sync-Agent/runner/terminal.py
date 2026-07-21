import subprocess
from pathlib import Path


class Terminal:

    def __init__(self, working_dir):

        self.working_dir = Path(working_dir)

    def run(self, command):

        process = subprocess.Popen(
            command,
            cwd=self.working_dir,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = process.communicate()

        return {
            "success": process.returncode == 0,
            "code": process.returncode,
            "stdout": stdout,
            "stderr": stderr
        }