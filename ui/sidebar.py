
"""
ui/sidebar.py
Sidebar widget for AI Code Sync Agent (Tkinter)
"""

import tkinter as tk
from tkinter import ttk


class Sidebar(ttk.Frame):
    def __init__(self, master, on_action=None, **kwargs):
        super().__init__(master, padding=8, **kwargs)
        self.on_action = on_action or (lambda action: None)

        ttk.Label(
            self,
            text="AI Code Sync Agent",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(0, 10))

        self._add_button("🏠 Dashboard", "dashboard")
        self._add_button("📂 Open Project", "open_project")
        self._add_button("📥 Extract Files", "extract")
        self._add_button("🔄 Sync Project", "sync")
        self._add_button("▶ Run Project", "run")
        self._add_button("🛠 Repair", "repair")
        self._add_button("📜 Logs", "logs")
        self._add_button("⚙ Settings", "settings")

        ttk.Separator(self).pack(fill="x", pady=10)

        ttk.Label(self, text="Status").pack(anchor="w")

        self.status_var = tk.StringVar(value="Ready")

        ttk.Label(
            self,
            textvariable=self.status_var,
            foreground="green"
        ).pack(anchor="w")

        ttk.Label(self, text="Provider").pack(anchor="w", pady=(10, 0))

        self.provider = ttk.Combobox(
            self,
            state="readonly",
            values=[
                "ChatGPT",
                "Kimi",
                "Claude",
                "Gemini",
                "DeepSeek"
            ]
        )
        self.provider.current(1)
        self.provider.pack(fill="x")

        ttk.Label(self, text="Progress").pack(anchor="w", pady=(10, 0))

        self.progress = ttk.Progressbar(
            self,
            maximum=100
        )
        self.progress.pack(fill="x")

    def _add_button(self, text, action):
        ttk.Button(
            self,
            text=text,
            command=lambda: self.on_action(action)
        ).pack(fill="x", pady=3)

    def set_status(self, text):
        self.status_var.set(text)

    def set_progress(self, value):
        self.progress["value"] = value

    def get_provider(self):
        return self.provider.get()


if __name__ == "__main__":

    root = tk.Tk()
    root.title("Sidebar Demo")
    root.geometry("260x520")

    def clicked(action):
        print("Action:", action)

    sidebar = Sidebar(root, on_action=clicked)
    sidebar.pack(fill="both", expand=True)

    root.mainloop()
