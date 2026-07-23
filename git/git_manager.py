import subprocess
from pathlib import Path


class GitManager:

    def __init__(self, project):

        self.project = Path(project)

    def run(self, command):

        process = subprocess.Popen(
            command,
            cwd=self.project,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = process.communicate()

        return {
            "success": process.returncode == 0,
            "stdout": stdout,
            "stderr": stderr,
            "code": process.returncode
        }

    def init(self):

        return self.run("git init")

    def add_all(self):

        return self.run("git add .")