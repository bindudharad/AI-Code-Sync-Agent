from pathlib import Path


class TreeBuilder:

    def build(self, root):

        root = Path(root)

        tree = []

        for path in sorted(root.rglob("*")):

            level = len(path.relative_to(root).parts)

            indent = "    " * (level - 1)

            icon = "📁" if path.is_dir() else "📄"

            tree.append(
                f"{indent}{icon} {path.name}"
            )

        return "\n".join(tree)