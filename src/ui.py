"""
UI Module
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
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QTimer
from grid import Grid


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


class GridWidget(QWidget):
    """
    Map grid widget
    """

    MAX_AGE_THRESHOLD = 100

    def __init__(self, n_rows: int, n_cols: int, seed: str | None = None) -> None:
        super().__init__()
        self.grid = Grid(n_rows, n_cols, seed)
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.grid_size = (n_rows, n_cols)
        self.cells = []
        self.grid_layout = QVBoxLayout()
        self.setLayout(self.grid_layout)

    def display_grid(self):
        """
        Displays grid
        """
        for _ in range(self.n_rows):
            row = QHBoxLayout()
            for _ in range(self.n_cols):
                cell = GridCellWidget()
                row.addWidget(cell)
                self.cells.append(cell)
            self.grid_layout.addLayout(row)
        self.update_grid()

    def update_grid(self):
        """
        Updates current grid
        """
        self.grid.update_grid()
        for i, cell in enumerate(self.cells):
            color = QColor(
                self.grid[i // self.grid_size[1]][i % self.grid_size[1]].color
            )
            cell.set_color(color)


class ToggleButton(QPushButton):
    """
    Start/stop toggle button
    """

    def __init__(self):
        super().__init__("Start")


class SidePanelWidget(QWidget):
    """
    Side pannel widgets
    """

    def __init__(self):
        super().__init__()
        self.sidebar_layout = QVBoxLayout()
        self.setLayout(self.sidebar_layout)

        self.start_button = ToggleButton()
        self.sidebar_layout.addWidget(self.start_button)


class GridCellWidget(QLabel):
    """
    Cell widget
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.setAlignment(Qt.AlignCenter)

    def set_color(self, color):
        """
        Set color of the cell
        """
        palette = self.palette()
        palette.setColor(self.backgroundRole(), color)
        self.setPalette(palette)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
