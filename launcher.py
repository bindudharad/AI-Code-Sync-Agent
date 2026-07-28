"""
launcher.py
Main launcher for AI Code Sync Agent.
"""

from app.config import Config
from app.logger import Logger
from app.constants import APP_NAME, VERSION

from browser.chrome import ChromeController
from browser.dom_reader import DOMReader
from browser.page_loader import PageLoader

from browser.kimi_reader import KimiReader
from storage.file_writer import FileWriter


class Launcher:
    def __init__(self):
        self.config = Config()
        self.logger = Logger()

        self.browser = ChromeController(
            headless=self.config.get("headless", False)
            if hasattr(self.config, "get") else False
        )

    def start(self):
        self.logger.line()
        self.logger.info(APP_NAME)
        self.logger.info(f"Version : {VERSION}")
        self.logger.line()

        project = ""
        if hasattr(self.config, "get_project_path"):
            project = self.config.get_project_path()

        self.logger.success("Configuration Loaded")
        self.logger.info(f"Project Folder : {project}")
        self.logger.line()

        try:
            self.logger.info("Launching browser...")
            self.browser.launch()

            start_url = (
                "https://www.kimi.com/chat/"
                "19b3c998-83a2-8cc8-8000-095893872bff"
                "?chat_enter_method=history"
            )

            if hasattr(self.config, "get_start_url"):
                start_url = self.config.get_start_url()

            self.browser.open(start_url)
            self.browser.page.wait_for_load_state("networkidle")
            self.browser.page.wait_for_timeout(5000)

            loader = PageLoader()
            loader.manager = self.browser

            dom_reader = DOMReader(loader.manager)

            self.logger.success("Browser opened")
            self.logger.info(f"URL : {self.browser.current_url()}")
            self.logger.info(f"Title : {dom_reader.title()}")

            html = self.browser.get_page_source()
            self.logger.info(f"HTML size : {len(html)} bytes")
            
            reader = KimiReader(self.browser)
            
            blocks = reader.get_code_blocks()
            
            writer = FileWriter(project)
            
            print("=" * 60)
            print(f"Found {len(blocks)} files")
            print("=" * 60)
            
            for file in blocks:
            
                path = file["path"]
                code = file["code"]
            
                if len(code.strip()) < 20:
                    print(f"[SKIPPED] {path} (too small)")
                    continue
            
                writer.save(path, code)
            
            print("\nFinished extracting files.")
            
            self.logger.success("Agent Started Successfully")


        except Exception as e:
            self.logger.error(f"Launcher Error : {e}")

        finally:
            input("\nPress Enter to close the browser...")
            self.browser.close()


if __name__ == "__main__":
    Launcher().start()