
"""
ui/settings.py

Settings panel for AI Code Sync Agent.
Requires: PySide6
"""

import json
import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QCheckBox,
    QPushButton,
    QLabel,
    QFileDialog,
    QHBoxLayout,
)

SETTINGS_FILE = "settings.json"


class SettingsPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")
        self.resize(700, 420)

        layout = QVBoxLayout(self)

        self.status = QLabel("Ready")
        layout.addWidget(self.status)

        form = QFormLayout()

        self.project_path = QLineEdit()
        self.chrome_profile = QLineEdit()
        self.start_url = QLineEdit("https://kimi.com")
        self.headless = QCheckBox()

        form.addRow("Project Folder", self.project_path)
        form.addRow("Chrome Profile", self.chrome_profile)
        form.addRow("Start URL", self.start_url)
        form.addRow("Headless Mode", self.headless)

        layout.addLayout(form)

        row = QHBoxLayout()
        self.browse_btn = QPushButton("Browse Project")
        self.load_btn = QPushButton("Load")
        self.save_btn = QPushButton("Save")

        row.addWidget(self.browse_btn)
        row.addStretch()
        row.addWidget(self.load_btn)
        row.addWidget(self.save_btn)

        layout.addLayout(row)

        self.browse_btn.clicked.connect(self.browse)
        self.load_btn.clicked.connect(self.load)
        self.save_btn.clicked.connect(self.save)

        self.load()

    def browse(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Project Folder")
        if folder:
            self.project_path.setText(folder)

    def load(self):
        path = Path(SETTINGS_FILE)
        if not path.exists():
            self.status.setText("No settings file found.")
            return

        data = json.loads(path.read_text(encoding="utf-8"))

        self.project_path.setText(data.get("project_path", ""))
        self.chrome_profile.setText(data.get("chrome_profile", ""))
        self.start_url.setText(data.get("start_url", "https://kimi.com"))
        self.headless.setChecked(data.get("headless", False))

        self.status.setText("Settings loaded.")

    def save(self):
        data = {
            "project_path": self.project_path.text(),
            "chrome_profile": self.chrome_profile.text(),
            "start_url": self.start_url.text(),
            "headless": self.headless.isChecked(),
        }

        Path(SETTINGS_FILE).write_text(
            json.dumps(data, indent=4),
            encoding="utf-8",
        )

        self.status.setText("Settings saved.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    panel = SettingsPanel()
    panel.show()
    sys.exit(app.exec())
