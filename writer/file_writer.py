
"""
writer/file_writer.py

Writes extracted project files safely to disk.
"""

from pathlib import Path
from datetime import datetime
import shutil


class FileWriter:
    def __init__(self, project_root="."):
        self.project_root = Path(project_root).resolve()
        self.project_root.mkdir(parents=True, exist_ok=True)

    def write_file(self, relative_path: str, content: str, backup=True):
        target = self.project_root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)

        if backup and target.exists():
            self._backup(target)

        target.write_text(content, encoding="utf-8")
        return target

    def write_files(self, files, backup=True):
        written = []
        failed = []

        for item in files:
            try:
                path = item["path"]
                code = item["code"]
                result = self.write_file(path, code, backup)
                written.append(str(result))
            except Exception as exc:
                failed.append({
                    "path": item.get("path", ""),
                    "error": str(exc)
                })

        return {
            "written": written,
            "failed": failed,
            "total": len(files),
            "success": len(written),
        }

    def delete_file(self, relative_path: str):
        target = self.project_root / relative_path
        if target.exists():
            target.unlink()

    def file_exists(self, relative_path: str):
        return (self.project_root / relative_path).exists()

    def _backup(self, path: Path):
        backup_dir = self.project_root / ".backups"
        backup_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{path.name}.{timestamp}.bak"

        shutil.copy2(path, backup_dir / backup_name)


if __name__ == "__main__":
    writer = FileWriter("demo_project")

    files = [
        {
            "path": "backend/app.py",
            "code": 'print("Hello World")'
        },
        {
            "path": "frontend/src/App.tsx",
            "code": "export default function App(){ return null; }"
        }
    ]

    result = writer.write_files(files)
    print(result)
