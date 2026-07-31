
"""
writer/backup.py

Backup manager for AI Code Sync Agent.
"""

from pathlib import Path
from datetime import datetime
import shutil


class BackupManager:
    def __init__(self, backup_root=".backups"):
        self.backup_root = Path(backup_root)
        self.backup_root.mkdir(parents=True, exist_ok=True)

    def backup_file(self, file_path):
        src = Path(file_path)
        if not src.exists():
            return None

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = self.backup_root / f"{src.name}.{stamp}.bak"
        shutil.copy2(src, dest)
        return dest

    def backup_project(self, project_root):
        root = Path(project_root)
        if not root.exists():
            raise FileNotFoundError(project_root)

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = self.backup_root / f"project_{stamp}"
        shutil.copytree(root, dest, dirs_exist_ok=True)
        return dest

    def restore_file(self, backup_path, target_path):
        backup = Path(backup_path)
        target = Path(target_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(backup, target)

    def list_backups(self):
        return sorted(self.backup_root.glob("*"), key=lambda p: p.stat().st_mtime, reverse=True)

    def delete_backup(self, backup_path):
        p = Path(backup_path)
        if p.is_dir():
            shutil.rmtree(p)
        elif p.exists():
            p.unlink()

    def cleanup(self, keep=10):
        items = self.list_backups()
        for old in items[keep:]:
            self.delete_backup(old)


if __name__ == "__main__":
    manager = BackupManager()
    print("Backup folder:", manager.backup_root.resolve())
    print("Existing backups:")
    for item in manager.list_backups():
        print(" -", item.name)
