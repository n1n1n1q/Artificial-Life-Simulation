"""
Main window of the UI
"""

from PySide6.QtWidgets import (
    QMainWindow,
    QHBoxLayout,
    QWidget,
)

from PySide6.QtCore import QTimer, Qt
from ui.grid_ui import GridWidget
from ui.widgets import SidePanelWidget


class MainWindow(QMainWindow):
    """
    Main window
    """

    DELAY = 300

    def __init__(self) -> None:
        super().__init__()
        self.setMaximumSize(1920, 1080)
        self.setMinimumSize(1920, 1080)
        self.resize(1920, 1080)
        self.setWindowTitle("Terrain Generation")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.window_layout = QHBoxLayout()
        self.central_widget.setLayout(self.window_layout)

        self.side_panel = SidePanelWidget(self)
        self.window_layout.addWidget(
            self.side_panel, alignment=Qt.AlignmentFlag.AlignTop
        )

        self.init_grid((60, 60), None)

        self.side_panel.info.seed = self.grid.grid.seed
        self.side_panel.info.size = (self.grid.n_rows, self.grid.n_cols)
        self.side_panel.info.delay = self.side_panel.delay_slider.value()
        self.side_panel.info.update_text()

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
            self.change_speed(self.side_panel.delay_slider.value())
            self.timer.start(self.DELAY)
            self.side_panel.start_button.setText("Stop")
        self.side_panel.regenerate_button.setEnabled(self.is_running)
        self.side_panel.delay_slider.setEnabled(self.is_running)
        self.is_running = not self.is_running

    def init_grid(self, size, seed):
        """
        Init grid
        """
        self.grid = GridWidget(*size, seed=seed, parent=self)
        self.window_layout.addWidget(self.grid, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid.display_grid()
        self.timer = QTimer()
        self.timer.timeout.connect(self.grid.generate_map)

    @classmethod
    def change_speed(cls, new):
        """
        ...
        """
        cls.DELAY = new
