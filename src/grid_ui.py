"""
Grid widget and grid cell widget
"""


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from grid import Grid


class GridWidget(QWidget):
    """
    Map grid widget
    """

    MAX_AGE_THRESHOLD = 100
    SPEED = 300

    def __init__(self, n_rows: int, n_cols: int, seed: str | None = None, parent = None) -> None:
        super().__init__(parent)
        self.grid = Grid(n_rows, n_cols, seed)
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.grid_size = (n_rows, n_cols)
        self.cells = []
        self.grid_layout = QVBoxLayout()
        self.grid_layout.setSpacing(0)
        self.setLayout(self.grid_layout)

    def clear_grid(self):
        """
        Clear current grid's layout
        """
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def display_grid(self):
        """
        Displays grid
        """
        for _ in range(self.n_rows):
            row = QHBoxLayout()
            row.setSpacing(0)
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
        for i, cell in enumerate(self.cells):
            color = QColor(
                self.grid[i // self.n_cols][i % self.n_cols].color
            )
            cell.set_color(color)

    def generate_map(self):
        """
        Start map's generation
        """
        self.grid.update_grid()
        self.update_grid()


class GridCellWidget(QLabel):
    """
    Cell widget
    """

    def __init__(self, parent=None):
        super().__init__()
        self._parent = parent
        self.setAutoFillBackground(True)
        self.setAlignment(Qt.AlignCenter)

    def set_color(self, color):
        """
        Set color of the cell
        """
        palette = self.palette()
        palette.setColor(self.backgroundRole(), color)
        self.setPalette(palette)