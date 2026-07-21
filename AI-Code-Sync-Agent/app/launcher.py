"""
Launcher for AI Code Sync Agent
"""

from config import Config
from logger import Logger
from constants import APP_NAME, VERSION


class Launcher:

    def __init__(self):
        self.config = Config()
        self.logger = Logger()

    def start(self):

        self.logger.line()

        self.logger.info(APP_NAME)
        self.logger.info(f"Version : {VERSION}")

        self.logger.line()

        self.logger.success("Configuration Loaded")

        project = self.config.get_project_path()

        self.logger.info(f"Project Folder : {project}")

        self.logger.line()

        self.logger.success("Agent Started Successfully")

        # Next modules will be connected here
        # Browser Controller
        # Extractor
        # File Writer
        # Project Runner