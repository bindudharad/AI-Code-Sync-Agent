from pathlib import Path
from datetime import datetime


class LogManager:

    LOG_DIR = Path("storage/logs")

    def __init__(self):

        self.LOG_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

    def write(self, filename, message):

        file = self.LOG_DIR / filename

        with open(
            file,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(

                f"[{datetime.now()}] {message}\n"

            )