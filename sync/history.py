import json
from pathlib import Path
from datetime import datetime


class History:

    FILE = Path("storage/history/sync_history.json")

    def __init__(self):

        self.FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def load(self):

        if not self.FILE.exists():
            return []

        with open(
            self.FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    def add(self, filepath):

        data = self.load()

        data.append({

            "file": filepath,

            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        })

        with open(
            self.FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )