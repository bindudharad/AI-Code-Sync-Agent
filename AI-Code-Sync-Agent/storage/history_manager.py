import json
from pathlib import Path
from datetime import datetime


class HistoryManager:

    FILE = Path(
        "storage/history/sync_history.json"
    )

    def add(self, filepath):

        self.FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if self.FILE.exists():

            with open(
                self.FILE,
                "r",
                encoding="utf-8"
            ) as f:

                history = json.load(f)

        else:

            history = []

        history.append({

            "file": filepath,

            "time": str(datetime.now())

        })

        with open(
            self.FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                history,
                f,
                indent=4
            )