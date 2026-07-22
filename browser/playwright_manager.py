"""
browser/playwright_manager.py
Playwright helper for AI Code Sync Agent.
"""

from playwright.sync_api import sync_playwright


class PlaywrightManager:
    def __init__(self, headless=False, channel="chrome"):
        self.headless = headless
        self.channel = channel
        self._pw = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self):
        if self.page:
            return self.page
        self._pw = sync_playwright().start()
        self.browser = self._pw.chromium.launch(
            channel=self.channel,
            headless=self.headless
        )
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        return self.page

    def goto(self, url, wait_until="networkidle"):
        if not self.page:
            self.start()
        self.page.goto(url, wait_until=wait_until)

    def html(self):
        if not self.page:
            return ""
        return self.page.content()

    def title(self):
        return self.page.title() if self.page else ""

    def url(self):
        return self.page.url if self.page else ""

    def click(self, selector):
        self.page.locator(selector).click()

    def fill(self, selector, text):
        self.page.locator(selector).fill(text)

    def text(self, selector):
        return self.page.locator(selector).inner_text()

    def exists(self, selector):
        return self.page.locator(selector).count() > 0

    def wait_selector(self, selector, timeout=30000):
        self.page.wait_for_selector(selector, timeout=timeout)

    def evaluate(self, script):
        return self.page.evaluate(script)

    def screenshot(self, path="page.png"):
        self.page.screenshot(path=path, full_page=True)

    def close(self):
        try:
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self._pw:
                self._pw.stop()
        finally:
            self.page = None
            self.context = None
            self.browser = None
            self._pw = None


if __name__ == "__main__":
    mgr = PlaywrightManager(headless=False)
    mgr.start()
    mgr.goto("https://example.com")
    print(mgr.title())
    print(mgr.url())
    mgr.screenshot("example.png")
    mgr.close()
