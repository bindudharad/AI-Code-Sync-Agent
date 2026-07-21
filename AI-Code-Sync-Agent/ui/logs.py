
"""ui/logs.py
Log viewer widget for AI Code Sync Agent.
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime


class LogViewer(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, padding=6, **kwargs)

        ttk.Label(
            self,
            text="Application Logs",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", pady=(0, 5))

        toolbar = ttk.Frame(self)
        toolbar.pack(fill="x", pady=(0, 5))

        ttk.Button(toolbar, text="Clear", command=self.clear).pack(side="left")
        ttk.Button(toolbar, text="Copy", command=self.copy).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Save", command=self.save).pack(side="left")

        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True)

        self.text = tk.Text(
            frame,
            wrap="word",
            state="normal",
            font=("Consolas", 10)
        )

        scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=self.text.yview
        )

        self.text.configure(
            yscrollcommand=scrollbar.set
        )

        self.text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def log(self, message, level="INFO"):
        now = datetime.now().strftime("%H:%M:%S")
        line = f"[{now}] [{level}] {message}\n"

        self.text.insert("end", line)
        self.text.see("end")

    def info(self, message):
        self.log(message, "INFO")

    def success(self, message):
        self.log(message, "SUCCESS")

    def warning(self, message):
        self.log(message, "WARNING")

    def error(self, message):
        self.log(message, "ERROR")

    def clear(self):
        self.text.delete("1.0", "end")

    def copy(self):
        content = self.text.get("1.0", "end")

        self.clipboard_clear()
        self.clipboard_append(content)

    def save(self, filename="logs.txt"):
        content = self.text.get("1.0", "end")

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:
            f.write(content)

    def load(self, filename):
        try:
            with open(
                filename,
                "r",
                encoding="utf-8"
            ) as f:

                self.clear()

                self.text.insert(
                    "end",
                    f.read()
                )

        except FileNotFoundError:

            self.error(f"{filename} not found.")


if __name__ == "__main__":

    root = tk.Tk()
    root.title("Log Viewer")
    root.geometry("800x500")

    viewer = LogViewer(root)
    viewer.pack(fill="both", expand=True)

    viewer.info("Application started")
    viewer.success("Connected successfully")
    viewer.warning("Low disk space")
    viewer.error("Unable to locate file")

    root.mainloop()
