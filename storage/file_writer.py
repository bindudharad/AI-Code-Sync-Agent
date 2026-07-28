from pathlib import Path


class FileWriter:
    def __init__(self, project_root):
        self.project_root = Path(project_root)

    def save(self, relative_path, content):
        """
        Save a file inside the project folder.
        """

        if not relative_path:
            return None

        relative_path = relative_path.replace("\\", "/").strip()

        if not content:
            print(f"[SKIPPED EMPTY] {relative_path}")
            return None

        content = content.strip()

        # Skip filename-only blocks
        if content == relative_path:
            print(f"[SKIPPED NAME ONLY] {relative_path}")
            return None

        # Skip directory names
        if relative_path.endswith("/"):
            return None

        file_path = self.project_root / relative_path

        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_path.write_text(content, encoding="utf-8")

        if file_path.exists():

            old = file_path.read_text(
                encoding="utf-8",
                errors="ignore"
            )
        
            if old == content:
        
                print(f"[SKIP] {relative_path}")
        
                return file_path
        
        file_path.write_text(content, encoding="utf-8")
        
        print(f"[SAVED] {relative_path} ({len(content)} chars)")
        

        return file_path