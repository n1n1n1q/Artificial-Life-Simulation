"""
Main window of the UI
"""

from PySide6.QtWidgets import (
    QMainWindow,
    QHBoxLayout,
    QWidget,
)

from PySide6.QtCore import QTimer
from grid_ui import GridWidget
from widgets import SidePanelWidget


class MainWindow(QMainWindow):
    """
    Main window
    """

    SPEED = 300

    def __init__(self) -> None:
        super().__init__()
        self.resize(1920, 1080)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.window_layout = QHBoxLayout()
        self.central_widget.setLayout(self.window_layout)

        self.side_panel = SidePanelWidget(self)
        self.window_layout.addWidget(self.side_panel)

        self.grid = GridWidget(30, 30, parent=self)
        self.window_layout.addWidget(self.grid)
        self.grid.display_grid()

        self.timer = QTimer()
        self.timer.timeout.connect(self.grid.generate_map)
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
            self.timer.start(self.SPEED)
            self.side_panel.start_button.setText("Stop")
        self.side_panel.regenerate_button.setEnabled(self.is_running)
        self.is_running = not self.is_running
