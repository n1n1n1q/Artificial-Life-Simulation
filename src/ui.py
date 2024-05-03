"""
UI module
"""

import sys
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

    def __init__(self, n_rows: int, n_cols: int, seed: None | str = None):
        super().__init__()

        self.grid_size = (n_rows, n_cols)
        self.grid = Grid(*self.grid_size, seed)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.grid_layout = QVBoxLayout()
        self.central_widget.setLayout(self.grid_layout)

        self.create_grid_ui()

        self.update_button = QPushButton("Start")
        self.update_button.clicked.connect(self.toggle_update)
        self.grid_layout.addWidget(self.update_button)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_grid)

        self.is_running = False

    def create_grid_ui(self):
        """
        Create grid
        """
        self.cell_widgets = []

        for _ in range(self.grid_size[0]):
            row_layout = QHBoxLayout()
            for __ in range(self.grid_size[1]):
                cell_widget = CellWidget()
                row_layout.addWidget(cell_widget)
                self.cell_widgets.append(cell_widget)
            self.grid_layout.addLayout(row_layout)

        self.update_grid_ui()

    def update_grid_ui(self):
        """
        Update grid's ui
        """
        for i, cell_widget in enumerate(self.cell_widgets):
            cell = self.grid[i // self.grid_size[1]][i % self.grid_size[1]]
            color = QColor(cell.color)
            cell_widget.set_color(color)

    def update_grid(self):
        """
        Update grid
        """
        self.grid.update_grid()
        self.update_grid_ui()

    def toggle_update(self):
        """
        Toggle update
        """
        if self.is_running:
            self.timer.stop()
            self.update_button.setText("Start")
        else:
            self.timer.start(50)
            self.update_button.setText("Stop")
        self.is_running = not self.is_running


class CellWidget(QLabel):
    """
    Cell
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.setAlignment(Qt.AlignCenter)

    def set_color(self, color):
        """
        Set color
        """
        palette = self.palette()
        palette.setColor(self.backgroundRole(), color)
        self.setPalette(palette)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow(50, 50)
    window.show()
    sys.exit(app.exec())
