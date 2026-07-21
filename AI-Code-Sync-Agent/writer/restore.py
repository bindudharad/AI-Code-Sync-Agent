import shutil
from pathlib import Path


class Restore:

    BACKUP_FOLDER = Path("storage/backups")

    @classmethod
    def restore(cls, filepath):

        backup = cls.BACKUP_FOLDER / filepath

        target = Path(filepath)

        if not backup.exists():

            print("Backup Not Found")

            return

        target.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        shutil.copy2(
            backup,
            target
        )

        print(f"Restored {filepath}")