import json
from pathlib import Path


class DependencyChecker:

    def node_dependencies(self, root):

        package = Path(root) / "package.json"

        if not package.exists():
            return {}

        with open(package, encoding="utf-8") as f:

            data = json.load(f)

        deps = {}

        deps.update(data.get("dependencies", {}))

        deps.update(data.get("devDependencies", {}))

        return deps

    def python_dependencies(self, root):

        req = Path(root) / "requirements.txt"

        if not req.exists():
            return []

        with open(req, encoding="utf-8") as f:

            return [
                line.strip()
                for line in f.readlines()
                if line.strip()
            ]