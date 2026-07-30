
"""
ui/project_tree.py

Project Tree widget for AI Code Sync Agent.
Requires: PySide6
"""

import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTreeWidget,
    QTreeWidgetItem,
    QPushButton,
    QHBoxLayout,
)


class ProjectTree(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Project Tree")

        layout = QVBoxLayout(self)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Project Files")
        layout.addWidget(self.tree)

        buttons = QHBoxLayout()

        self.expand_btn = QPushButton("Expand All")
        self.collapse_btn = QPushButton("Collapse All")
        self.clear_btn = QPushButton("Clear")

        buttons.addWidget(self.expand_btn)
        buttons.addWidget(self.collapse_btn)
        buttons.addStretch()
        buttons.addWidget(self.clear_btn)

        layout.addLayout(buttons)

        self.expand_btn.clicked.connect(self.tree.expandAll)
        self.collapse_btn.clicked.connect(self.tree.collapseAll)
        self.clear_btn.clicked.connect(self.tree.clear)

    def add_file(self, path: str):
        parts = path.replace("\\", "/").split("/")
        parent = self.tree.invisibleRootItem()

        for part in parts:
            node = None

            for i in range(parent.childCount()):
                child = parent.child(i)
                if child.text(0) == part:
                    node = child
                    break

            if node is None:
                node = QTreeWidgetItem([part])
                parent.addChild(node)

            parent = node


if __name__ == "__main__":
    app = QApplication(sys.argv)

    tree = ProjectTree()

    tree.add_file("backend/app.py")
    tree.add_file("backend/routes/api.py")
    tree.add_file("frontend/src/App.tsx")
    tree.add_file("frontend/src/components/Navbar.tsx")

    tree.resize(500, 700)
    tree.show()

    sys.exit(app.exec())
