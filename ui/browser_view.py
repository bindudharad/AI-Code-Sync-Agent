"""ui/browser_view.py"""
import sys
from PySide6.QtWidgets import QApplication,QWidget,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QTextEdit

class BrowserView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Browser View")
        lay=QVBoxLayout(self)
        top=QHBoxLayout()
        self.url=QLabel("URL: Not Connected")
        self.status=QLabel("Status: Idle")
        top.addWidget(self.url); top.addStretch(); top.addWidget(self.status)
        lay.addLayout(top)
        self.log=QTextEdit(); self.log.setReadOnly(True)
        lay.addWidget(self.log)
        btn=QHBoxLayout()
        for t,fn in [("Connect",self.demo_connect),("Refresh",self.demo_refresh),("Screenshot",self.demo_shot),("Clear",self.log.clear)]:
            b=QPushButton(t); b.clicked.connect(fn); btn.addWidget(b)
        lay.addLayout(btn)
    def demo_connect(self):
        self.url.setText("URL: https://kimi.com"); self.status.setText("Status: Connected"); self.log.append("Connected")
    def demo_refresh(self): self.log.append("Refreshed")
    def demo_shot(self): self.log.append("Screenshot captured")

if __name__=="__main__":
    app=QApplication(sys.argv); w=BrowserView(); w.resize(900,500); w.show(); sys.exit(app.exec())
