"""
browser/page_loader.py
Page loading utilities for AI Code Sync Agent.
"""

from browser.playwright_manager import PlaywrightManager


class PageLoader:
    def __init__(self, manager=None, headless=False):
        self.manager = manager or PlaywrightManager(headless=headless)

    def open(self, url):
        self.manager.start()
        self.manager.goto(url)
        return self.manager.html()

    def reload(self):
        if self.manager.page:
            self.manager.page.reload(wait_until="networkidle")
            return self.manager.html()
        return ""

    def wait_network_idle(self):
        if self.manager.page:
            self.manager.page.wait_for_load_state("networkidle")

    def wait_dom_ready(self):
        if self.manager.page:
            self.manager.page.wait_for_load_state("domcontentloaded")

    def title(self):
        return self.manager.title()

    def current_url(self):
        return self.manager.url()

    def html(self):
        return self.manager.html()

    def screenshot(self, path="page.png"):
        self.manager.screenshot(path)

    def close(self):
        self.manager.close()


if __name__ == "__main__":
    loader = PageLoader(headless=False)
    loader.open("https://example.com")
    print(loader.title())
    print(loader.current_url())
    print(loader.html()[:200])
    loader.close()
