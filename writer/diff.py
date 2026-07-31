
"""
writer/diff.py

Simple file diff utilities for AI Code Sync Agent.
"""

from pathlib import Path
import difflib


class DiffManager:
    def read(self, path):
        p = Path(path)
        if not p.exists():
            return ""
        return p.read_text(encoding="utf-8").splitlines(keepends=True)

    def compare_text(self, old_text: str, new_text: str, from_name="old", to_name="new"):
        return "".join(
            difflib.unified_diff(
                old_text.splitlines(keepends=True),
                new_text.splitlines(keepends=True),
                fromfile=from_name,
                tofile=to_name,
                lineterm=""
            )
        )

    def compare_files(self, old_file, new_file):
        return "".join(
            difflib.unified_diff(
                self.read(old_file),
                self.read(new_file),
                fromfile=str(old_file),
                tofile=str(new_file),
                lineterm=""
            )
        )

    def changed(self, old_text: str, new_text: str) -> bool:
        return old_text != new_text

    def similarity(self, old_text: str, new_text: str) -> float:
        return difflib.SequenceMatcher(None, old_text, new_text).ratio()


if __name__ == "__main__":
    dm = DiffManager()

    before = """print("Hello")
print("World")
"""

    after = """print("Hello")
print("AI Code Sync Agent")
"""

    print(dm.compare_text(before, after))
    print("Similarity:", round(dm.similarity(before, after), 3))
