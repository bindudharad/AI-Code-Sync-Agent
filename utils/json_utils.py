"""
JSON Utilities
"""

import json
from pathlib import Path


class JSONUtils:

    @staticmethod
    def load(path):

        file = Path(path)

        if not file.exists():
            return {}

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    @staticmethod
    def save(path, data):

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )

    @staticmethod
    def pretty(data):

        return json.dumps(
            data,
            indent=4
        )