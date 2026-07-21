"""
Common Helper Functions
"""

import os
import uuid
from datetime import datetime


class Helpers:

    @staticmethod
    def timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def unique_id():
        return str(uuid.uuid4())

    @staticmethod
    def filesize(path):

        if not os.path.exists(path):
            return 0

        return os.path.getsize(path)

    @staticmethod
    def exists(path):

        return os.path.exists(path)

    @staticmethod
    def read(path):

        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def write(path, text):

        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

    @staticmethod
    def append(path, text):

        with open(path, "a", encoding="utf-8") as f:
            f.write(text)