"""
Ui init
"""

import sys

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


def start_ui():
    """
    Opens QT application
    """
    app = QApplication([])
    window = MainWindow()
    with open("style.qss", "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())
    window.show()
    sys.exit(app.exec())
