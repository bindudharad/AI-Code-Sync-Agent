
"""ui/settings.py
Settings panel for AI Code Sync Agent.
"""

import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox


class SettingsPanel(ttk.Frame):
    SETTINGS_FILE = Path("settings.json")

    def __init__(self, master, **kwargs):
        super().__init__(master, padding=10, **kwargs)

        self.project = tk.StringVar()
        self.provider = tk.StringVar(value="Kimi")
        self.headless = tk.BooleanVar(value=False)
        self.auto_backup = tk.BooleanVar(value=True)
        self.auto_run = tk.BooleanVar(value=True)

        ttk.Label(self, text="Settings",
                  font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0,10))

        form = ttk.Frame(self)
        form.pack(fill="x")

        self._row_entry(form, 0, "Project Folder", self.project)

        ttk.Label(form, text="AI Provider").grid(row=1, column=0, sticky="w", pady=5)
        combo = ttk.Combobox(
            form,
            textvariable=self.provider,
            state="readonly",
            values=["ChatGPT","Kimi","Claude","Gemini","DeepSeek"]
        )
        combo.grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Checkbutton(form, text="Headless Browser",
                        variable=self.headless).grid(row=2, column=0, columnspan=2, sticky="w")

        ttk.Checkbutton(form, text="Auto Backup",
                        variable=self.auto_backup).grid(row=3, column=0, columnspan=2, sticky="w")

        ttk.Checkbutton(form, text="Auto Run Project",
                        variable=self.auto_run).grid(row=4, column=0, columnspan=2, sticky="w")

        form.columnconfigure(1, weight=1)

        btns = ttk.Frame(self)
        btns.pack(fill="x", pady=15)

        ttk.Button(btns, text="Load", command=self.load).pack(side="left")
        ttk.Button(btns, text="Save", command=self.save).pack(side="left", padx=5)
        ttk.Button(btns, text="Reset", command=self.reset).pack(side="left")

    def _row_entry(self, parent, row, label, variable):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=5)
        ttk.Entry(parent, textvariable=variable).grid(row=row, column=1, sticky="ew", pady=5)

    def to_dict(self):
        return {
            "project": self.project.get(),
            "provider": self.provider.get(),
            "headless": self.headless.get(),
            "auto_backup": self.auto_backup.get(),
            "auto_run": self.auto_run.get()
        }

    def save(self):
        with open(self.SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=4)
        messagebox.showinfo("Settings", "Settings saved.")

    def load(self):
        if not self.SETTINGS_FILE.exists():
            messagebox.showwarning("Settings", "No settings file found.")
            return

        with open(self.SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.project.set(data.get("project",""))
        self.provider.set(data.get("provider","Kimi"))
        self.headless.set(data.get("headless",False))
        self.auto_backup.set(data.get("auto_backup",True))
        self.auto_run.set(data.get("auto_run",True))

        messagebox.showinfo("Settings", "Settings loaded.")

    def reset(self):
        self.project.set("")
        self.provider.set("Kimi")
        self.headless.set(False)
        self.auto_backup.set(True)
        self.auto_run.set(True)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Settings")
    root.geometry("500x320")
    panel = SettingsPanel(root)
    panel.pack(fill="both", expand=True)
    root.mainloop()
