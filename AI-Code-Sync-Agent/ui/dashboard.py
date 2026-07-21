
"""
ui/dashboard.py
Starter dashboard for AI Code Sync Agent using tkinter.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path


class Dashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("AI Code Sync Agent")
        self.geometry("1100x700")
        self.minsize(900, 600)

        self.project_path = tk.StringVar(value="No project selected")
        self.status = tk.StringVar(value="Ready")
        self.progress = tk.DoubleVar(value=0)

        self._build_ui()

    def _build_ui(self):
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="AI Code Sync Agent",
                  font=("Segoe UI", 18, "bold")).pack(side="left")

        ttk.Button(top, text="Open Project",
                   command=self.select_project).pack(side="right")

        info = ttk.LabelFrame(self, text="Project", padding=10)
        info.pack(fill="x", padx=10)

        ttk.Label(info, textvariable=self.project_path).pack(anchor="w")

        center = ttk.PanedWindow(self, orient="horizontal")
        center.pack(fill="both", expand=True, padx=10, pady=10)

        left = ttk.Frame(center)
        right = ttk.Frame(center)

        center.add(left, weight=1)
        center.add(right, weight=3)

        ttk.Label(left, text="Files",
                  font=("Segoe UI", 12, "bold")).pack(anchor="w")

        self.tree = ttk.Treeview(left)
        self.tree.pack(fill="both", expand=True)

        ttk.Label(right, text="Logs",
                  font=("Segoe UI", 12, "bold")).pack(anchor="w")

        self.logs = tk.Text(right, wrap="word")
        self.logs.pack(fill="both", expand=True)

        bottom = ttk.Frame(self, padding=10)
        bottom.pack(fill="x")

        ttk.Progressbar(bottom,
                        variable=self.progress,
                        maximum=100).pack(fill="x")

        ttk.Label(bottom,
                  textvariable=self.status).pack(anchor="w", pady=5)

        buttons = ttk.Frame(bottom)
        buttons.pack(fill="x")

        ttk.Button(buttons,
                   text="Extract",
                   command=lambda: self.log("Extract clicked")).pack(side="left", padx=5)

        ttk.Button(buttons,
                   text="Sync",
                   command=lambda: self.log("Sync clicked")).pack(side="left", padx=5)

        ttk.Button(buttons,
                   text="Run Project",
                   command=lambda: self.log("Run clicked")).pack(side="left", padx=5)

    def select_project(self):
        folder = filedialog.askdirectory()

        if not folder:
            return

        self.project_path.set(folder)

        self.tree.delete(*self.tree.get_children())

        self.insert_folder("", Path(folder))

        self.log(f"Loaded project: {folder}")

    def insert_folder(self, parent, path: Path):
        node = self.tree.insert(parent, "end", text=path.name, open=False)

        try:
            for child in sorted(path.iterdir()):
                if child.is_dir():
                    self.insert_folder(node, child)
                else:
                    self.tree.insert(node, "end", text=child.name)
        except PermissionError:
            pass

    def log(self, message):
        self.logs.insert("end", message + "\n")
        self.logs.see("end")

    def set_progress(self, value):
        self.progress.set(value)

    def set_status(self, text):
        self.status.set(text)


if __name__ == "__main__":
    Dashboard().mainloop()
