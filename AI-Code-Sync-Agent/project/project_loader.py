from pathlib import Path


class ProjectLoader:

    def __init__(self, root):

        self.root = Path(root)

    def exists(self):

        return self.root.exists()

    def root_path(self):

        return str(self.root.resolve())

    def files(self):

        result = []

        for file in self.root.rglob("*"):

            if file.is_file():

                result.append(str(file))

        return result

    def folders(self):

        result = []

        for folder in self.root.rglob("*"):

            if folder.is_dir():

                result.append(str(folder))

        return result