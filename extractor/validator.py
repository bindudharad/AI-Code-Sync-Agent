
"""
extractor/validator.py

Validation utilities for extracted project files.
"""

import os
import re


class Validator:
    # Common source-code extensions
    VALID_EXTENSIONS = {
        ".py", ".js", ".jsx", ".ts", ".tsx",
        ".java", ".kt", ".cpp", ".cc", ".c",
        ".h", ".hpp", ".cs", ".go", ".rs",
        ".php", ".rb", ".swift", ".dart",
        ".html", ".css", ".scss", ".json",
        ".xml", ".yaml", ".yml", ".toml",
        ".md", ".txt", ".sql", ".sh",
        ".bat", ".env"
    }

    INVALID_PATH_PARTS = {
        "..",
        "~",
    }

    def valid_path(self, path: str) -> bool:
        if not path:
            return False

        path = path.strip().replace("\\", "/")

        if any(part in path for part in self.INVALID_PATH_PARTS):
            return False

        if path.startswith("/"):
            return False

        _, ext = os.path.splitext(path)

        if ext.lower() not in self.VALID_EXTENSIONS:
            return False

        if re.search(r'[<>:"|?*]', path):
            return False

        return True

    def valid_code(self, code: str) -> bool:
        if code is None:
            return False

        if not isinstance(code, str):
            return False

        return len(code.strip()) > 0

    def normalize_path(self, path: str) -> str:
        return path.replace("\\", "/").strip()

    def remove_duplicates(self, files):
        seen = set()
        result = []

        for item in files:
            path = self.normalize_path(item["path"])

            if path in seen:
                continue

            seen.add(path)

            item["path"] = path
            result.append(item)

        return result


if __name__ == "__main__":
    validator = Validator()

    tests = [
        "backend/app.py",
        "frontend/src/App.tsx",
        "../secret.txt",
        "config?.json",
        "README.md",
    ]

    for t in tests:
        print(f"{t:25} -> {validator.valid_path(t)}")
