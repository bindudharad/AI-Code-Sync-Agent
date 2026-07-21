"""
Configuration File
"""

from pathlib import Path


class Config:

    def __init__(self):

        self.project_path = Path.cwd()

        self.chrome_path = None

        self.browser = "chrome"

        self.ai_provider = "kimi"

        self.auto_run = True

        self.auto_backup = True

    def get_project_path(self):
        return self.project_path

    def get_browser(self):
        return self.browser

    def get_provider(self):
        return self.ai_provider

    def is_auto_run(self):
        return self.auto_run

    def is_backup_enabled(self):
        return self.auto_backup