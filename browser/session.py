"""
browser/session.py
Session manager for AI Code Sync Agent.
"""

from pathlib import Path
from playwright.sync_api import sync_playwright


class BrowserSession:
    def __init__(self, user_data_dir="browser_profile", headless=False, channel="chrome"):
        self.user_data_dir = Path(user_data_dir)
        self.headless = headless
        self.channel = channel
        self._pw = None
        self.browser = None
        self.page = None

    def start(self):
        if self.page:
            return self.page

        self.user_data_dir.mkdir(parents=True, exist_ok=True)

        self._pw = sync_playwright().start()

        self.browser = self._pw.chromium.launch_persistent_context(
            user_data_dir=str(self.user_data_dir),
            channel=self.channel,
            headless=self.headless,
        )

        pages = self.browser.pages
        self.page = pages[0] if pages else self.browser.new_page()
        return self.page

    def open(self, url):
        if not self.page:
            self.start()
        self.page.goto(url, wait_until="networkidle")

    def save_storage_state(self, path="storage_state.json"):
        if self.browser:
            self.browser.storage_state(path=path)

    def load_storage_state(self, path="storage_state.json"):
        # Persistent context automatically reuses the profile.
        return Path(path).exists()

    def cookies(self):
        return self.browser.cookies() if self.browser else []

    def clear_cookies(self):
        if self.browser:
            self.browser.clear_cookies()

    def close(self):
        try:
            if self.browser:
                self.browser.close()
            if self._pw:
                self._pw.stop()
        finally:
            self.browser = None
            self.page = None
            self._pw = None


if __name__ == "__main__":
    session = BrowserSession(headless=False)
    session.start()
    session.open("https://example.com")
    print(session.page.title())
    session.save_storage_state()
    session.close()
