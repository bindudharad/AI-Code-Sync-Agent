import shutil
from pathlib import Path


class Backup:

    BACKUP_FOLDER = Path("storage/backups")

    @classmethod
    def create(cls, filepath):

        source = Path(filepath)

        if not source.exists():
            return

        destination = cls.BACKUP_FOLDER / filepath

        destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        shutil.copy2(
            source,
            destination
        )

        print(f"Backup Created -> {destination}")