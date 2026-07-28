from pathlib import Path
import shutil


class Sandbox:

    def __init__(self):

        self.root = Path("sandbox")

        self.root.mkdir(
            parents=True,
            exist_ok=True
        )

    def path(self):

        return self.root

    def clear(self):

        if self.root.exists():

            shutil.rmtree(self.root)

        self.root.mkdir(
            parents=True,
            exist_ok=True
        )

    def create_project(self, name):

        project = self.root / name

        project.mkdir(
            parents=True,
            exist_ok=True
        )

        return project