"""
UI Opener
"""

from PySide6.QtWidgets import QApplication
from main_window import MainWindow

def start_ui():
    """
    Opens QT application
    """
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
