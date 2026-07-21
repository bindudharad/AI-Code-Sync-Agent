
"""ui/notifications.py
Notification widget for AI Code Sync Agent.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class NotificationCenter(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, padding=8, **kwargs)

        ttk.Label(
            self,
            text="Notifications",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", pady=(0, 8))

        toolbar = ttk.Frame(self)
        toolbar.pack(fill="x")

        ttk.Button(toolbar, text="Clear", command=self.clear).pack(side="left")

        self.count = tk.StringVar(value="0 notifications")
        ttk.Label(toolbar, textvariable=self.count).pack(side="right")

        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True)

        self.listbox = tk.Listbox(frame)
        scroll = ttk.Scrollbar(frame, orient="vertical",
                               command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scroll.set)

        self.listbox.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self._items = []

    def _add(self, level, message):
        ts = datetime.now().strftime("%H:%M:%S")
        text = f"[{ts}] [{level}] {message}"
        self._items.append(text)
        self.listbox.insert("end", text)
        self.count.set(f"{len(self._items)} notifications")

    def info(self, message):
        self._add("INFO", message)

    def success(self, message):
        self._add("SUCCESS", message)

    def warning(self, message):
        self._add("WARNING", message)

    def error(self, message):
        self._add("ERROR", message)

    def popup_info(self, title, message):
        self.info(message)
        messagebox.showinfo(title, message)

    def popup_warning(self, title, message):
        self.warning(message)
        messagebox.showwarning(title, message)

    def popup_error(self, title, message):
        self.error(message)
        messagebox.showerror(title, message)

    def clear(self):
        self._items.clear()
        self.listbox.delete(0, "end")
        self.count.set("0 notifications")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Notifications")
    root.geometry("600x400")

    center = NotificationCenter(root)
    center.pack(fill="both", expand=True)

    center.info("Application started")
    center.success("Project synchronized")
    center.warning("1 file skipped")
    center.error("Build failed")

    root.mainloop()
