"""
Grid widget and grid cell widget
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPixmap

from py_terrain.grid import Grid


class GridWidget(QWidget):
    """
    Map grid widget
    """

    DELAY = 300

    def __init__(
        self, n_rows: int, n_cols: int, seed: str | None = None, parent=None
    ) -> None:
        super().__init__(parent)
        self.grid = Grid(n_rows, n_cols, seed)
        self.setFixedHeight(900)
        self.setFixedWidth(1400)
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.cells = []
        self.grid_layout = QVBoxLayout()
        self.grid_layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.parent_ = parent
        self.setLayout(self.grid_layout)
        self.parent_.side_panel.export_button.clicked.connect(self.export_as_png)

    def clear_grid(self):
        """
        Clear current grid's layout
        """
        self.grid_layout = QVBoxLayout()
        self.grid_layout.setSpacing(0)
        self.cells = []

    def display_grid(self):
        """
        Displays grid
        """
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        for _ in range(self.n_rows):
            row = QHBoxLayout()
            row.setAlignment(Qt.AlignmentFlag.AlignCenter)
            row.setSpacing(0)
            row.setContentsMargins(0, 0, 0, 0)
            for _ in range(self.n_cols):
                cell = GridCellWidget(self, self.n_cols, self.n_rows)
                cell.raise_()
                row.addWidget(cell, alignment=Qt.AlignmentFlag.AlignCenter)
                self.cells.append(cell)
            self.grid_layout.addLayout(row)
        self.update_grid()

    def update_grid(self):
        """
        Updates current grid
        """
        for i, cell in enumerate(self.cells):
            color = QColor(self.grid[i // self.n_cols][i % self.n_cols].color)
            cell.set_color(color)

    def generate_map(self):
        """
        Start map's generation
        """
        is_stopped = self.grid.update_grid()
        self.update_grid()
        if is_stopped:
            self.parent_.toggle_update()
            self.parent_.side_panel.textures_button.setEnabled(True)

    def export_as_png(self):
        """
        Export the map as png
        """
        pixmap = QPixmap(self.size())
        self.render(pixmap)
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "PNG (*.png)"
        )
        if file_name:
            pixmap.save(file_name + ".png", "PNG")


class GridCellWidget(QLabel):
    """
    Cell widget
    """

    def __init__(self, parent=None, grid_width=None, grid_height=None):
        super().__init__()
        self.parent_ = parent
        min_side = min(1400 / grid_width, 900 / grid_height)
        self.setFixedSize(min_side, min_side)
        self.setAutoFillBackground(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def set_color(self, color):
        """
        Set color of the cell
        """
        palette = self.palette()
        palette.setColor(self.backgroundRole(), color)
        self.setPalette(palette)

    def set_texture(self, filepath):
        """
        Set texture to cell
        """
        pixmap = QPixmap(filepath)
        self.setPixmap(pixmap)
        self.setScaledContents(True)
