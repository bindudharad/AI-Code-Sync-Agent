"""
Simple Logger
"""

from datetime import datetime


class Logger:

    def _time(self):
        return datetime.now().strftime("%H:%M:%S")

    def info(self, message):
        print(f"[{self._time()}] [INFO] {message}")

    def success(self, message):
        print(f"[{self._time()}] [SUCCESS] {message}")

    def warning(self, message):
        print(f"[{self._time()}] [WARNING] {message}")

    def error(self, message):
        print(f"[{self._time()}] [ERROR] {message}")

    def line(self):
        print("=" * 70)