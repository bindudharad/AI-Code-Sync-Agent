
"""
browser/cdp_browser.py

Connect to an already running Chrome instance via the
Chrome DevTools Protocol (CDP).

Start Chrome first with:

chrome.exe --remote-debugging-port=9222

Then use this class to attach to it.
"""

from playwright.sync_api import sync_playwright


class CDPBrowser:
    def __init__(self, endpoint="http://127.0.0.1:9222"):
        self.endpoint = endpoint
        self._pw = None
        self.browser = None
        self.context = None
        self.page = None

    def connect(self):
        if self.page:
            return self.page

        self._pw = sync_playwright().start()
        self.browser = self._pw.chromium.connect_over_cdp(self.endpoint)

        contexts = self.browser.contexts
        if contexts:
            self.context = contexts[0]
        else:
            self.context = self.browser.new_context()

        pages = self.context.pages
        if pages:
            self.page = pages[0]
        else:
            self.page = self.context.new_page()

        return self.page

    def new_tab(self):
        self.connect()
        self.page = self.context.new_page()
        return self.page

    def goto(self, url, timeout=60000):
        self.connect()
        self.page.goto(url, wait_until="domcontentloaded", timeout=timeout)

    def title(self):
        self.connect()
        return self.page.title()

    def url(self):
        self.connect()
        return self.page.url

    def html(self):
        self.connect()
        return self.page.content()

    def evaluate(self, script):
        self.connect()
        return self.page.evaluate(script)

    def click(self, selector):
        self.page.locator(selector).click()

    def fill(self, selector, value):
        self.page.locator(selector).fill(value)

    def screenshot(self, path="cdp_browser.png"):
        self.page.screenshot(path=path, full_page=True)

    def close(self):
        try:
            if self.browser:
                self.browser.close()
        finally:
            if self._pw:
                self._pw.stop()
            self.browser = None
            self.context = None
            self.page = None
            self._pw = None


if __name__ == "__main__":
    browser = CDPBrowser()
    browser.connect()
    print("Connected!")
    print("Title:", browser.title())
    print("URL:", browser.url())
    input("Press Enter to close...")
    browser.close()
