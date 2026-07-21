
"""ui/progress.py
Progress panel widget for AI Code Sync Agent.
"""

import tkinter as tk
from tkinter import ttk


class ProgressPanel(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, padding=8, **kwargs)

        self.percent = tk.DoubleVar(value=0)
        self.status = tk.StringVar(value="Ready")
        self.current_file = tk.StringVar(value="-")
        self.stats = {
            "created": tk.IntVar(value=0),
            "updated": tk.IntVar(value=0),
            "skipped": tk.IntVar(value=0),
            "errors": tk.IntVar(value=0),
        }

        ttk.Label(
            self,
            text="Progress",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")

        self.bar = ttk.Progressbar(
            self,
            maximum=100,
            variable=self.percent
        )
        self.bar.pack(fill="x", pady=8)

        ttk.Label(self, textvariable=self.status).pack(anchor="w")

        ttk.Label(
            self,
            textvariable=self.current_file,
            foreground="blue"
        ).pack(anchor="w", pady=(5, 10))

        grid = ttk.Frame(self)
        grid.pack(fill="x")

        self._row(grid, "Created", self.stats["created"], 0)
        self._row(grid, "Updated", self.stats["updated"], 1)
        self._row(grid, "Skipped", self.stats["skipped"], 2)
        self._row(grid, "Errors", self.stats["errors"], 3)

        ttk.Button(self, text="Reset", command=self.reset).pack(
            anchor="e", pady=10
        )

    def _row(self, parent, title, var, row):
        ttk.Label(parent, text=title + ":").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(parent, textvariable=var).grid(row=row, column=1, sticky="e", padx=5)

    def set_progress(self, value):
        value = max(0, min(100, value))
        self.percent.set(value)

    def set_status(self, text):
        self.status.set(text)

    def set_current_file(self, filepath):
        self.current_file.set(f"Current: {filepath}")

    def increment(self, key, amount=1):
        if key in self.stats:
            self.stats[key].set(self.stats[key].get() + amount)

    def reset(self):
        self.percent.set(0)
        self.status.set("Ready")
        self.current_file.set("-")
        for var in self.stats.values():
            var.set(0)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Progress Demo")
    root.geometry("420x280")

    panel = ProgressPanel(root)
    panel.pack(fill="both", expand=True)

    panel.set_status("Extracting project...")
    panel.set_progress(35)
    panel.set_current_file("src/App.tsx")
    panel.increment("created", 12)
    panel.increment("updated", 4)
    panel.increment("skipped", 2)

    root.mainloop()
