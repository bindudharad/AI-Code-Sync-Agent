
"""
writer/overwrite.py

Safe overwrite manager for AI Code Sync Agent.
"""

from pathlib import Path
import hashlib
from datetime import datetime


class OverwriteManager:
    def __init__(self):
        pass

    def file_exists(self, path):
        return Path(path).exists()

    def read(self, path):
        path = Path(path)
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8")

    def write(self, path, content):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def checksum(self, path):
        path = Path(path)
        if not path.exists():
            return ""

        h = hashlib.sha256()
        with open(path, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()

    def is_changed(self, path, new_content):
        path = Path(path)
        if not path.exists():
            return True

        current = path.read_text(encoding="utf-8")
        return current != new_content

    def overwrite(self, path, content):
        """
        Returns:
            created
            updated
            skipped
        """
        path = Path(path)

        if not path.exists():
            self.write(path, content)
            return "created"

        current = path.read_text(encoding="utf-8")

        if current == content:
            return "skipped"

        self.write(path, content)
        return "updated"

    def overwrite_many(self, files):
        report = {
            "created": 0,
            "updated": 0,
            "skipped": 0,
        }

        for item in files:
            status = self.overwrite(
                item["path"],
                item["code"],
            )
            report[status] += 1

        report["timestamp"] = datetime.now().isoformat()

        return report


if __name__ == "__main__":
    manager = OverwriteManager()

    files = [
        {
            "path": "demo/file1.py",
            "code": "print('hello')"
        },
        {
            "path": "demo/file2.txt",
            "code": "sample"
        }
    ]

    print(manager.overwrite_many(files))
