"""
browser/scroll_manager.py
Scrolling utilities for AI Code Sync Agent.
"""

import time
from browser.playwright_manager import PlaywrightManager


class ScrollManager:
    def __init__(self, manager=None):
        self.manager = manager or PlaywrightManager()

    @property
    def page(self):
        return self.manager.page

    def to_top(self):
        if self.page:
            self.page.evaluate("window.scrollTo(0, 0);")

    def to_bottom(self):
        if self.page:
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight);")

    def by(self, pixels=1000):
        if self.page:
            self.page.evaluate(f"window.scrollBy(0, {int(pixels)});")

    def smooth_to_bottom(self, step=800, delay=0.4, max_rounds=100):
        if not self.page:
            return
        previous = -1
        for _ in range(max_rounds):
            height = self.page.evaluate("document.body.scrollHeight")
            self.page.evaluate(f"window.scrollBy(0, {int(step)});")
            self.page.wait_for_timeout(int(delay * 1000))
            new_height = self.page.evaluate("document.body.scrollHeight")
            if new_height == previous == height:
                break
            previous = new_height

    def until_selector(self, selector, step=600, delay=0.3, limit=100):
        if not self.page:
            return False
        for _ in range(limit):
            if self.page.locator(selector).count() > 0:
                return True
            self.page.evaluate(f"window.scrollBy(0, {int(step)});")
            self.page.wait_for_timeout(int(delay * 1000))
        return False

    def infinite_scroll(self, delay=0.5):
        if not self.page:
            return
        last_height = 0
        while True:
            self.to_bottom()
            self.page.wait_for_timeout(int(delay * 1000))
            height = self.page.evaluate("document.body.scrollHeight")
            if height == last_height:
                break
            last_height = height


if __name__ == "__main__":
    mgr = PlaywrightManager(headless=False)
    mgr.start()
    mgr.goto("https://example.com")
    scroller = ScrollManager(mgr)
    scroller.to_bottom()
    time.sleep(1)
    scroller.to_top()
    mgr.close()
