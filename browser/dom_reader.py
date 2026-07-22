"""
browser/dom_reader.py
DOM reader utilities for AI Code Sync Agent.
"""

from browser.playwright_manager import PlaywrightManager


class DOMReader:
    def __init__(self, manager=None):
        self.manager = manager or PlaywrightManager()

    @property
    def page(self):
        return self.manager.page

    def html(self):
        return self.manager.html()

    def title(self):
        return self.manager.title()

    def text(self, selector):
        self.manager.wait_selector(selector)
        return self.page.locator(selector).inner_text()

    def texts(self, selector):
        return [e.inner_text() for e in self.page.locator(selector).all()]

    def attribute(self, selector, name):
        self.manager.wait_selector(selector)
        return self.page.locator(selector).first.get_attribute(name)

    def exists(self, selector):
        return self.manager.exists(selector)

    def count(self, selector):
        return self.page.locator(selector).count()

    def elements(self, selector):
        return self.page.locator(selector).all()

    def links(self):
        return self.page.locator("a").evaluate_all(
            "(els)=>els.map(e=>({text:e.innerText,href:e.href}))"
        )

    def code_blocks(self):
        selectors = ["pre code", "pre", "code"]
        blocks = []
        for s in selectors:
            if self.exists(s):
                blocks.extend(self.texts(s))
        return blocks


if __name__ == "__main__":
    mgr = PlaywrightManager(headless=False)
    mgr.start()
    mgr.goto("https://example.com")
    reader = DOMReader(mgr)
    print(reader.title())
    print(reader.links())
    mgr.close()
