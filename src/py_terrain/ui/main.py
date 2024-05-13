"""
Ui main
"""

import sys
import os

from importlib import resources as impresources
from PySide6.QtWidgets import QApplication
from py_terrain.ui.main_window import MainWindow


def start_ui():
    """
    Opens QT application
    """
    # print(f'OS: {os.listdir()}')
    app = QApplication([])
    window = MainWindow()
    app.setStyleSheet(impresources.read_text('py_terrain', 'style.qss'))
    window.show()
    sys.exit(app.exec())
