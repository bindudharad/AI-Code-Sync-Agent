
"""
runner/terminal.py

Terminal output manager for AI Code Sync Agent.
"""

import queue
import threading
import subprocess
import platform
from pathlib import Path


class TerminalManager:
    def __init__(self, cwd="."):
        self.cwd = Path(cwd).resolve()
        self.process = None
        self._queue = queue.Queue()

    def execute(self, command):
        if isinstance(command, str):
            shell = True
            cmd = command
        else:
            shell = (platform.system() == "Windows")
            cmd = command

        self.process = subprocess.Popen(
            cmd,
            cwd=self.cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            shell=shell,
        )

        threading.Thread(target=self._reader, daemon=True).start()

    def _reader(self):
        if not self.process or not self.process.stdout:
            return
        for line in self.process.stdout:
            self._queue.put(line.rstrip())

    def read_lines(self):
        lines = []
        while not self._queue.empty():
            lines.append(self._queue.get())
        return lines

    def wait(self):
        if self.process:
            return self.process.wait()
        return None

    def is_running(self):
        return self.process is not None and self.process.poll() is None

    def terminate(self):
        if self.is_running():
            self.process.terminate()

    def kill(self):
        if self.is_running():
            self.process.kill()

    @property
    def return_code(self):
        if self.process:
            return self.process.poll()
        return None


if __name__ == "__main__":
    tm = TerminalManager()
    tm.execute("python --version")

    while tm.is_running():
        for line in tm.read_lines():
            print(line)

    for line in tm.read_lines():
        print(line)

    print("Exit code:", tm.return_code)
