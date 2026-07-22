"""
browser/chrome.py
ChromeController for AI Code Sync Agent.
"""

from playwright.sync_api import sync_playwright


class ChromeController:
    def __init__(self, headless=False):
        self.headless = headless
        self._playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def launch(self):
        print(__file__)
        print(">>> ChromeController.launch() called <<<")
        if self.page:
            return self.page
    
        self._playwright = sync_playwright().start()
    
        self.context = self._playwright.chromium.launch_persistent_context(
            user_data_dir=r"C:\Temp\ChromeDebugProfile",
            channel="chrome",
            headless=False,
            args=[
                "--start-maximized"
            ],
            no_viewport=True
        )
    
        # Look for an already-open Kimi tab
        for p in self.context.pages:
            if "kimi.com" in p.url:
                self.page = p
                print("Using existing Kimi tab")
                return self.page
    
        # Otherwise reuse the first existing tab
        if self.context.pages:
            # Use the first page that is not about:blank
            for p in self.context.pages:
                if p.url != "about:blank":
                    self.page = p
                    break
            else:
                self.page = self.context.pages[0]
        else:
            self.page = self.context.new_page()
    
        return self.page

    def open(self, url):
        print(">>> ChromeController.open() called <<<")
        if not self.page:
            self.launch()
    
        # If already on Kimi, don't open it again
        if "kimi.com" not in self.page.url:
            try:
                self.page.goto(
                    url,
                    wait_until="load",
                    timeout=120000
                )
                self.page.wait_for_load_state("networkidle")
                self.page.wait_for_timeout(3000)
            except Exception as e:
                print("Goto warning:", e)
            
            # Give the page time to finish loading
            self.page.wait_for_timeout(5000)
            
            print("Current URL:", self.page.url)
                
        print("Current URL:", self.page.url)

    def get_page_source(self):
        if not self.page:
            raise RuntimeError("Browser has not been launched.")
        return self.page.content()

    def current_url(self):
        return self.page.url if self.page else ""
    
    
    def title(self):
        if not self.page:
            return ""
        return self.page.title()
    
    
    def wait(self, seconds):
        if self.page:
            self.page.wait_for_timeout(int(seconds * 1000))

    def evaluate(self, script):
        if not self.page:
            raise RuntimeError("Browser has not been launched.")
        return self.page.evaluate(script)

    def screenshot(self, path="browser.png"):
        if not self.page:
            raise RuntimeError("Browser has not been launched.")
        self.page.screenshot(path=path, full_page=True)

    def close(self):
        try:
            if self.context:
                self.context.close()
    
            if self._playwright:
                self._playwright.stop()
    
        finally:
            self.context = None
            self.page = None
            self._playwright = None


if __name__ == "__main__":
    c = ChromeController()
    c.launch()
    c.open("https://example.com")
    print(c.current_url())
    print(c.get_page_source()[:200])
    c.close()
