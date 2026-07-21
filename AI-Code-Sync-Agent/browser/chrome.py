from browser.playwright_manager import PlaywrightManager


class ChromeController:

    def __init__(self):

        self.manager = PlaywrightManager()

        self.page = None

    def launch(self):

        self.page = self.manager.start(
            headless=False
        )

        return self.page

    def close(self):

        self.manager.stop()