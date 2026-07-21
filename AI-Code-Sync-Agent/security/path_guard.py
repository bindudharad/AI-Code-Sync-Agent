from pathlib import Path


class PathGuard:

    def __init__(self):

        self.blocked = [

            "C:\\Windows",

            "C:\\Program Files",

            "C:\\Program Files (x86)",

            "/etc",

            "/usr",

            "/bin",

            "/boot"

        ]

    def safe(self, filepath):

        target = Path(filepath).resolve()

        for folder in self.blocked:

            try:

                if str(target).startswith(
                    str(Path(folder).resolve())
                ):
                    return False

            except Exception:
                pass

        return True

    def inside(self, root, filepath):

        root = Path(root).resolve()

        target = Path(filepath).resolve()

        return str(target).startswith(str(root))