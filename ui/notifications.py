
"""
ui/notifications.py

Notification widget for AI Code Sync Agent.
Requires: PySide6
"""

import sys
from datetime import datetime
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QHBoxLayout,
    QLabel,
)


class NotificationPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Notifications")

        layout = QVBoxLayout(self)

        self.status = QLabel("0 Notifications")
        layout.addWidget(self.status)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        buttons = QHBoxLayout()

        self.demo_btn = QPushButton("Demo")
        self.clear_btn = QPushButton("Clear")

        buttons.addWidget(self.demo_btn)
        buttons.addStretch()
        buttons.addWidget(self.clear_btn)

        layout.addLayout(buttons)

        self.demo_btn.clicked.connect(self.demo_notifications)
        self.clear_btn.clicked.connect(self.clear)

        self.timer = QTimer()
        self.timer.timeout.connect(self._heartbeat)

    def notify(self, title, message, level="INFO"):
        ts = datetime.now().strftime("%H:%M:%S")
        self.list_widget.insertItem(
            0,
            f"[{ts}] [{level}] {title} - {message}"
        )
        self.status.setText(
            f"{self.list_widget.count()} Notifications"
        )

    def clear(self):
        self.list_widget.clear()
        self.status.setText("0 Notifications")

    def demo_notifications(self):
        self.notify("Agent", "Started", "SUCCESS")
        self.notify("Browser", "Connected to Kimi")
        self.notify("Extractor", "Found 12 files")
        self.notify("Writer", "Project synchronized", "SUCCESS")

    def start_heartbeat(self):
        self.timer.start(5000)

    def stop_heartbeat(self):
        self.timer.stop()

    def _heartbeat(self):
        self.notify("Heartbeat", "Agent is running")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    panel = NotificationPanel()
    panel.resize(700, 500)
    panel.show()

    sys.exit(app.exec())
