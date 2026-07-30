
"""ui/dashboard.py
Simple dashboard window for AI Code Sync Agent.
Requires: PySide6
"""
import sys
from PySide6.QtCore import Qt,QTimer
from PySide6.QtWidgets import QApplication,QMainWindow,QWidget,QHBoxLayout,QVBoxLayout,QLabel,QPushButton,QTextEdit,QTreeWidget,QTreeWidgetItem

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Code Sync Agent")
        self.resize(1400,850)
        root=QWidget(); self.setCentralWidget(root)
        layout=QHBoxLayout(root)
        self.tree=QTreeWidget(); self.tree.setHeaderLabel("Project")
        self.logs=QTextEdit(); self.logs.setReadOnly(True)
        right=QVBoxLayout()
        self.status=QLabel("● Idle")
        self.start=QPushButton("Start Agent")
        self.stop=QPushButton("Stop Agent")
        self.clear=QPushButton("Clear Logs")
        self.start.clicked.connect(self.start_agent)
        self.stop.clicked.connect(self.stop_agent)
        self.clear.clicked.connect(self.logs.clear)
        btns=QHBoxLayout(); btns.addWidget(self.start); btns.addWidget(self.stop); btns.addWidget(self.clear)
        right.addWidget(self.status); right.addLayout(btns); right.addWidget(self.logs)
        layout.addWidget(self.tree,2); layout.addLayout(right,5)
        self.timer=QTimer(); self.timer.timeout.connect(lambda:self.logs.append("Heartbeat..."))

    def add_file(self,path):
        parent=self.tree.invisibleRootItem()
        for part in path.replace("\\","/").split("/"):
            node=None
            for i in range(parent.childCount()):
                if parent.child(i).text(0)==part:
                    node=parent.child(i); break
            if node is None:
                node=QTreeWidgetItem([part]); parent.addChild(node)
            parent=node

    def start_agent(self):
        self.status.setText("🟢 Running"); self.logs.append("Agent started."); self.timer.start(1000)

    def stop_agent(self):
        self.timer.stop(); self.status.setText("🔴 Stopped"); self.logs.append("Agent stopped.")

if __name__=="__main__":
    app=QApplication(sys.argv)
    w=Dashboard()
    w.add_file("backend/app.py")
    w.add_file("frontend/src/App.tsx")
    w.show()
    sys.exit(app.exec())
