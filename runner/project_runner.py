
"""
runner/project_runner.py

Run generated projects and capture output.
"""

from pathlib import Path
import subprocess
import threading
import queue
import platform


class ProjectRunner:
    def __init__(self, project_root="."):
        self.project_root = Path(project_root).resolve()
        self.process = None
        self.output_queue = queue.Queue()

    def detect_command(self):
        if (self.project_root / "package.json").exists():
            return ["npm", "run", "dev"]

        if (self.project_root / "requirements.txt").exists():
            if (self.project_root / "main.py").exists():
                return ["python", "main.py"]
            if (self.project_root / "app.py").exists():
                return ["python", "app.py"]

        if (self.project_root / "manage.py").exists():
            return ["python", "manage.py", "runserver"]

        return None

    def run(self, command=None):
        if command is None:
            command = self.detect_command()

        if command is None:
            raise RuntimeError("Could not detect how to run the project.")

        self.process = subprocess.Popen(
            command,
            cwd=self.project_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            shell=(platform.system() == "Windows"),
        )

        threading.Thread(target=self._reader, daemon=True).start()
        return self.process

    def _reader(self):
        for line in self.process.stdout:
            self.output_queue.put(line.rstrip())

    def get_output(self):
        lines = []
        while not self.output_queue.empty():
            lines.append(self.output_queue.get())
        return lines

    def is_running(self):
        return self.process is not None and self.process.poll() is None

    def stop(self):
        if self.is_running():
            self.process.terminate()
            self.process.wait(timeout=10)

    def return_code(self):
        if self.process:
            return self.process.poll()
        return None


if __name__ == "__main__":
    runner = ProjectRunner(".")
    try:
        runner.run()
        while runner.is_running():
            for line in runner.get_output():
                print(line)
    except Exception as e:
        print("Error:", e)
