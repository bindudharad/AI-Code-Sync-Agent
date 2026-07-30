
"""
ui/logs.py

Log viewer widget for AI Code Sync Agent.
Requires: PySide6
"""

import sys
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QLabel,
)


class LogViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Logs")

        layout = QVBoxLayout(self)

        self.status = QLabel("Ready")
        layout.addWidget(self.status)

        self.editor = QTextEdit()
        self.editor.setReadOnly(True)
        layout.addWidget(self.editor)

        buttons = QHBoxLayout()

        self.clear_btn = QPushButton("Clear")
        self.save_btn = QPushButton("Save")
        self.demo_btn = QPushButton("Demo")

        buttons.addWidget(self.demo_btn)
        buttons.addStretch()
        buttons.addWidget(self.save_btn)
        buttons.addWidget(self.clear_btn)

        layout.addLayout(buttons)

        self.clear_btn.clicked.connect(self.editor.clear)
        self.save_btn.clicked.connect(self.save_log)
        self.demo_btn.clicked.connect(self.demo)

    def add_log(self, message, level="INFO"):
        now = datetime.now().strftime("%H:%M:%S")
        self.editor.append(f"[{now}] [{level}] {message}")

    def set_status(self, text):
        self.status.setText(text)

    def save_log(self):
        Path("agent.log").write_text(
            self.editor.toPlainText(),
            encoding="utf-8"
        )
        self.add_log("Logs saved to agent.log", "SUCCESS")

    def demo(self):
        self.add_log("Agent started")
        self.add_log("Browser connected", "SUCCESS")
        self.add_log("Extracting files...")
        self.add_log("Completed", "SUCCESS")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = LogViewer()
    w.resize(900, 600)
    w.show()

    sys.exit(app.exec())
