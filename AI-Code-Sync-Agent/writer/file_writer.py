from pathlib import Path

from writer.folder_creator import FolderCreator


class FileWriter:

    def write(self, filepath, code):

        FolderCreator.create(filepath)

        file = Path(filepath)

        with open(
            file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(code)

        print(f"✓ Saved {filepath}")