import json
from pathlib import Path


class BrowserSession:

    FILE = "session.json"

    def save(self, data):

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

    def load(self):

        file = Path(self.FILE)

        if not file.exists():
            return {}

        with open(
            self.FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)