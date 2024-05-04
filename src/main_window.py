"""
Main window of the UI
"""

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QWidget,
)

from PySide6.QtCore import Qt, QTimer
from widgets import ToggleButton, SidePanelWidget, GridWidget, GridCellWidget


class MainWindow(QMainWindow):
    """
    Main window
    """

    def __init__(self) -> None:
        super().__init__()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.window_layout = QHBoxLayout()
        self.central_widget.setLayout(self.window_layout)

        self.side_panel = SidePanelWidget()
        self.window_layout.addWidget(self.side_panel)

        self.grid = GridWidget(50, 50)
        self.window_layout.addWidget(self.grid)
        self.grid.display_grid()

        self.timer = QTimer()
        self.timer.timeout.connect(self.grid.update_grid)
        self.is_running = False
        self.side_panel.start_button.clicked.connect(self.toggle_update)

    def toggle_update(self):
        """
        Toggle button handler
        """
        if self.is_running:
            self.timer.stop()
            self.side_panel.start_button.setText("Start")
        else:
            self.timer.start(50)
            self.side_panel.start_button.setText("Stop")
        self.is_running = not self.is_running
