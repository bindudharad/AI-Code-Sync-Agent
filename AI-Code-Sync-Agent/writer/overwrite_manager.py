from pathlib import Path

from writer.backup import Backup


class OverwriteManager:

    def save(self, filepath, code):

        file = Path(filepath)

        if file.exists():

            Backup.create(filepath)

        with open(
            file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(code)

        print(f"Updated {filepath}")