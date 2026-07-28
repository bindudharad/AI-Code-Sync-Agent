from pathlib import Path
import os


class Permission:

    @staticmethod
    def readable(path):

        return os.access(
            Path(path),
            os.R_OK
        )

    @staticmethod
    def writable(path):

        return os.access(
            Path(path),
            os.W_OK
        )

    @staticmethod
    def executable(path):

        return os.access(
            Path(path),
            os.X_OK
        )

    @staticmethod
    def exists(path):

        return Path(path).exists()