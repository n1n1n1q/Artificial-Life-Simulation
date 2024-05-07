"""
Side panel widgets
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSlider,
    QLineEdit,
    QLabel,
    QFrame,
    QSpacerItem,
    QSizePolicy,
)

from PySide6.QtCore import Qt


class SidePanelWidget(QWidget):
    """
    Side pannel widget
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        self.sidebar_layout = QVBoxLayout()

        self.main_title = Title("Terrain generation")
        self.options_subtitle = Subtitle("Options")
        self.seed_input_label = SeedInputLabel()
        self.seed_input = SeedInput(self)
        self.size_label = SizeLabel()
        self.size_input_n = SizeField(self)
        self.by = QLabel("x")
        self.size_input_m = SizeField(self)

        self.size_box = QWidget()
        self.size_box_layout = QHBoxLayout()
        self.size_box_layout.addWidget(self.size_input_m)
        self.size_box_layout.addWidget(self.by)
        self.size_box_layout.addWidget(self.size_input_n)
        self.size_box_layout.setContentsMargins(0, 0, 0, 0)
        self.size_box.setLayout(self.size_box_layout)

        self.delay_label = DelayLabel()
        self.delay_slider = DelaySlider(self)

        self.info_title = Subtitle("Info")
        self.info = Info(self)
        self.regenerate_button = RegenerateButton(self)
        self.start_button = ToggleButton(self)

        self.top_section = QWidget()
        self.top_layout = QVBoxLayout()
        self.top_layout.addWidget(self.main_title, alignment=Qt.AlignmentFlag.AlignTop)
        self.top_layout.addWidget(self.info_title, alignment=Qt.AlignmentFlag.AlignTop)
        self.top_layout.addWidget(self.info, alignment=Qt.AlignmentFlag.AlignTop)
        self.top_layout.addWidget(
            self.options_subtitle, alignment=Qt.AlignmentFlag.AlignTop
        )
        self.top_layout.addWidget(
            self.seed_input_label, alignment=Qt.AlignmentFlag.AlignTop
        )
        self.top_layout.addWidget(self.seed_input, alignment=Qt.AlignmentFlag.AlignTop)
        self.top_layout.addWidget(self.size_label, alignment=Qt.AlignmentFlag.AlignTop)
        self.top_layout.addWidget(self.size_box, alignment=Qt.AlignmentFlag.AlignTop)
        self.top_layout.addWidget(self.delay_label, alignment=Qt.AlignmentFlag.AlignTop)
        self.top_layout.addWidget(
            self.delay_slider, alignment=Qt.AlignmentFlag.AlignTop
        )
        self.top_layout.addWidget(self.regenerate_button)
        self.top_section.setLayout(self.top_layout)

        self.bottom_section = QWidget()
        self.bottom_layout = QVBoxLayout()
        self.bottom_layout.addWidget(
            self.start_button, alignment=Qt.AlignmentFlag.AlignBottom
        )
        self.bottom_section.setLayout(self.bottom_layout)

        self.sidebar_layout.addWidget(self.top_section)
        self.sidebar_layout.addWidget(self.bottom_section)
        self.setLayout(self.sidebar_layout)
        self.setMaximumWidth(400)
        self.setMaximumHeight(1080)

    def validate_all_inputs(self):
        """
        Validate all inputs
        """
        return self.size_input_n.validate_input() and self.size_input_m.validate_input()


class Subtitle(QLabel):
    """
    Subtitle class
    """

    def _init__(self, title):
        super().__init__()
        self.setText(title)


class Title(QLabel):
    """
    Title class
    """

    def __init__(self, title):
        super().__init__()
        self.setText(title)


class ToggleButton(QPushButton):
    """
    Start/stop toggle button
    """

    def __init__(self, parent=None):
        super().__init__("Start")
        self._parent = parent


class SeedInputLabel(QLabel):
    """
    Label of the seed input window
    """

    def __init__(self):
        super().__init__("Seed")
        self.setContentsMargins(0, 0, 0, 0)


class SeedInput(QLineEdit):
    """
    Seed input text field
    """

    def __init__(self, parent=None):
        super().__init__()
        self._parent = parent
        self.setMaxLength(20)
        self.textChanged.connect(self.reset_color)

    def reset_color(self):
        """
        Reset the background color back from red
        """
        self.setStyleSheet("SeedInput {}")


class DelayLabel(QLabel):
    """
    Delay adjustment label
    """

    def __init__(self):
        super().__init__("Generation delay")
        self.setContentsMargins(0, 0, 0, 0)


class DelaySlider(QSlider):
    """
    Delay adjustment slider
    """

    MIN_DELAY = 50
    MAX_DELAY = 1000

    def __init__(self, parent=None):
        super().__init__()
        self._parent = parent
        self.setOrientation(Qt.Horizontal)
        self.setRange(self.MIN_DELAY, self.MAX_DELAY)
        self.setValue(300)
        self.valueChanged.connect(self.update_info)

    def update_info(self):
        """
        Update info's delay val
        """
        info = self._parent.info
        info.delay = self.value()
        info.update_text()


class RegenerateButton(QPushButton):
    """
    Regenerate seed button
    """

    def __init__(self, parent=None):
        super().__init__("Regenerate")
        self._parent = parent
        self.clicked.connect(self.on_click)

    def on_click(self) -> None:
        """
        Regenerate button, on click event
        """
        if self._parent.validate_all_inputs():
            grid = self._parent._parent.grid
            try:
                size = (
                    int(self._parent.size_input_n.text()),
                    int(self._parent.size_input_m.text()),
                )
            except ValueError:
                size = grid.n_rows, grid.n_cols
            self._parent._parent.grid.n_rows, self._parent._parent.grid.n_cols = size
            seed = (
                self._parent.seed_input.text()
                if self._parent.seed_input.text()
                else grid.grid.generate_seed()
            )
            info = self._parent.info
            info.seed = seed
            info.size = size
            info.update_text()

            grid.setParent(None)
            self._parent._parent.init_grid(size, seed)


class SizeLabel(QLabel):
    """
    Label for the size input field
    """

    def __init__(self):
        super().__init__("Size")
        self.setContentsMargins(0, 0, 0, 0)


class SizeField(QLineEdit):
    """
    Size input field
    """

    def __init__(self, parent=None) -> None:
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
        data = self.text().strip()
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


class Info(QLabel):
    """
    Info class
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._parent = parent
        self.seed = None
        self.size = None
        self.delay = None

    def update_text(self):
        """
        Update info text
        """
        self.setText(
            f"""Seed = {self.seed}
Map's size: {self.size[0]}x{self.size[1]}
Delay: {self.delay}"""
        )
