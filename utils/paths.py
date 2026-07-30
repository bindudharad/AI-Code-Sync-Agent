"""
Path Utilities
"""

from pathlib import Path


class Paths:

    @staticmethod
    def join(*parts):

        return str(Path(*parts))

    @staticmethod
    def filename(path):

        return Path(path).name

    @staticmethod
    def extension(path):

        return Path(path).suffix

    @staticmethod
    def parent(path):

        return str(Path(path).parent)

    @staticmethod
    def absolute(path):

        return str(Path(path).resolve())

    @staticmethod
    def mkdir(path):

        Path(path).mkdir(
            parents=True,
            exist_ok=True
        )

    @staticmethod
    def is_file(path):

        return Path(path).is_file()

    @staticmethod
    def is_folder(path):

        return Path(path).is_dir()