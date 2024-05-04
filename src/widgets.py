"""
Side panel widgets
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QSlider,
    QLineEdit,
    QLabel
)

from PySide6.QtCore import Qt

class SidePanelWidget(QWidget):
    """
    Side pannel widget
    """

    def __init__(self, parent = None):
        super().__init__(parent)
        self._parent = parent
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.setContentsMargins(20, 20, 20, 20)
        self.sidebar_layout.setSpacing(20)

        self.seed_input_label = SeedInputLabel()
        self.seed_input = SeedInput(self)
        self.size_label = SizeLabel()
        self.size_input_n = SizeField(self)
        self.size_input_m = SizeField(self)
        self.speed_label = SpeedLabel()
        self.speed_slider = SpeedSlider(self)
        self.regenerate_button = RegenerateButton(self)
        self.start_button = ToggleButton(self)

        self.sidebar_layout.addWidget(self.seed_input_label)
        self.sidebar_layout.addWidget(self.seed_input)
        self.sidebar_layout.addWidget(self.size_label)
        self.sidebar_layout.addWidget(self.size_input_n)
        self.sidebar_layout.addWidget(self.size_input_m)
        self.sidebar_layout.addWidget(self.speed_label)
        self.sidebar_layout.addWidget(self.speed_slider)
        self.sidebar_layout.addWidget(self.regenerate_button)
        self.sidebar_layout.addWidget(self.start_button)

        self.setLayout(self.sidebar_layout)
        self.setMaximumWidth(300)

    def validate_all_inputs(self):
        """
        Validate all inputs
        """
        return (
            self.size_input_n.validate_input() and
            self.size_input_m.validate_input()
        )

class ToggleButton(QPushButton):
    """
    Start/stop toggle button
    """

    def __init__(self, parent = None):
        super().__init__("Start")
        self._parent = parent


class SeedInputLabel(QLabel):
    """
    Label of the seed input window
    """

    def __init__(self):
        super().__init__("Seed")


class SeedInput(QLineEdit):
    """
    Seed input text field
    """

    def __init__(self, parent = None):
        super().__init__()
        self._parent = parent
        self.setMaxLength(20)
        self.textChanged.connect(self.reset_color)

    def reset_color(self):
        """
        Reset the background color back from red
        """
        self.setStyleSheet("SeedInput {}")


class SpeedLabel(QLabel):
    """
    Speed adjustment label
    """

    def __init__(self):
        super().__init__("Generation speed")


class SpeedSlider(QSlider):
    """
    Speed adjustment slider
    """

    MIN_SPEED = 50
    MAX_SPEED = 1000

    def __init__(self, parent = None):
        super().__init__()
        self._parent = parent
        self.setOrientation(Qt.Horizontal)
        self.setRange(self.MIN_SPEED, self.MAX_SPEED)
        self.value = 300


class RegenerateButton(QPushButton):
    """
    Regenerate seed button
    """

    def __init__(self, parent = None):
        super().__init__(parent)
        self._parent = parent
        self.clicked.connect(self.on_click)

    def on_click(self) -> None:
        """
        Regenerate button, on click event
        """
        if self._parent.validate_all_inputs():
            grid = self._parent._parent.grid
            size = (self._parent.size_input_n.text(), self._parent.size_input_m)
            seed = self._parent.seed_input.text()
            grid.clear_grid()
            grid.grid.change_generation_size(*size)
            grid.grid.seed = seed
            grid.grid.set_up()
            grid.display_grid()


class SizeLabel(QLabel):
    """
    Label for the size input field
    """

    def __init__(self):
        super().__init__("Size")


class SizeField(QLineEdit):
    """
    Size input field
    """

    def __init__(self, parent = None) -> None:
        super().__init__()
        self._parent = parent
        self.textChanged.connect(self.reset_color)

    def reset_color(self):
        """
        Reset the background color back from red
        """
        self.setStyleSheet("SizeInput {}")

    def validate_input(self):
        """
        Validate input
        """
        data = self.text()
        if data:
            try:
                num = int(data)
            except Exception:
                self.setStyleSheet("SizeField { background-color: red; }")
                return False
            if num not in range(10, 101):
                self.setStyleSheet("SizeField { background-color: red; }")
                return False
        return True

