from pathlib import Path


class ProjectAnalyzer:

    def analyze(self, root):

        root = Path(root)

        stats = {
            "files": 0,
            "folders": 0,
            "size_mb": 0
        }

        for item in root.rglob("*"):

            if item.is_file():

                stats["files"] += 1

                stats["size_mb"] += item.stat().st_size

            elif item.is_dir():

                stats["folders"] += 1

        stats["size_mb"] = round(
            stats["size_mb"] / (1024 * 1024),
            2
        )

        return stats