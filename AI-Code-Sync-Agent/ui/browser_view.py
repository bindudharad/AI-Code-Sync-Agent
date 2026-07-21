
"""
ui/browser_view.py
Embedded browser placeholder for AI Code Sync Agent.

Uses pywebview if installed. Otherwise falls back to opening the
selected URL in the user's default browser.
"""

import webbrowser
import tkinter as tk
from tkinter import ttk


class BrowserView(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, padding=8, **kwargs)

        self.url = tk.StringVar(value="https://kimi.ai")

        ttk.Label(
            self,
            text="Browser View",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", pady=(0, 8))

        bar = ttk.Frame(self)
        bar.pack(fill="x")

        ttk.Entry(
            bar,
            textvariable=self.url
        ).pack(side="left", fill="x", expand=True)

        ttk.Button(
            bar,
            text="Open",
            command=self.open_url
        ).pack(side="left", padx=5)

        ttk.Button(
            bar,
            text="Kimi",
            command=lambda: self.navigate("https://kimi.ai")
        ).pack(side="left")

        ttk.Button(
            bar,
            text="ChatGPT",
            command=lambda: self.navigate("https://chatgpt.com")
        ).pack(side="left", padx=5)

        ttk.Button(
            bar,
            text="Gemini",
            command=lambda: self.navigate("https://gemini.google.com")
        ).pack(side="left")

        self.status = tk.StringVar(value="Ready")

        frame = ttk.LabelFrame(self, text="Preview", padding=10)
        frame.pack(fill="both", expand=True, pady=10)

        self.preview = tk.Text(
            frame,
            wrap="word",
            height=20
        )
        self.preview.pack(fill="both", expand=True)

        self.preview.insert(
            "end",
            "Embedded web rendering is not included in this starter.\n\n"
            "Use Playwright to automate a browser or integrate a webview "
            "library (e.g. pywebview) if you need an embedded browser."
        )
        self.preview.config(state="disabled")

        ttk.Label(
            self,
            textvariable=self.status
        ).pack(anchor="w")

    def navigate(self, url):
        self.url.set(url)
        self.open_url()

    def open_url(self):
        url = self.url.get().strip()
        if not url:
            return

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        webbrowser.open(url)
        self.status.set(f"Opened: {url}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Browser View")
    root.geometry("900x600")

    BrowserView(root).pack(fill="both", expand=True)

    root.mainloop()
