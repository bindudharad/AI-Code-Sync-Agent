
"""ui/project_tree.py
Project tree widget using ttk.Treeview.
"""

from pathlib import Path
import tkinter as tk
from tkinter import ttk


class ProjectTree(ttk.Frame):
    def __init__(self, master, on_select=None, **kwargs):
        super().__init__(master, padding=6, **kwargs)
        self.on_select = on_select or (lambda path: None)

        ttk.Label(self, text="Project Explorer",
                  font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0,5))

        self.tree = ttk.Treeview(self, show="tree")
        y = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=y.set)

        self.tree.pack(side="left", fill="both", expand=True)
        y.pack(side="right", fill="y")

        self._node_paths = {}
        self.tree.bind("<<TreeviewSelect>>", self._selected)

    def load_project(self, folder):
        self.clear()
        root = Path(folder)
        if not root.exists():
            return
        root_id = self.tree.insert("", "end", text=root.name, open=True)
        self._node_paths[root_id] = str(root)
        self._populate(root_id, root)

    def _populate(self, parent, path: Path):
        try:
            entries = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        except PermissionError:
            return

        for entry in entries:
            node = self.tree.insert(parent, "end", text=entry.name, open=False)
            self._node_paths[node] = str(entry)
            if entry.is_dir():
                self._populate(node, entry)

    def refresh(self):
        selected = self.current_path()
        if not selected:
            return
        root = Path(selected)
        if root.is_file():
            root = root.parent
        while root.parent != root and root.name:
            if root.exists():
                break
        self.load_project(root)

    def clear(self):
        self.tree.delete(*self.tree.get_children())
        self._node_paths.clear()

    def current_path(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return self._node_paths.get(sel[0])

    def _selected(self, _):
        path = self.current_path()
        if path:
            self.on_select(path)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("350x600")
    tree = ProjectTree(root, on_select=lambda p: print("Selected:", p))
    tree.pack(fill="both", expand=True)
    tree.load_project(".")
    root.mainloop()
