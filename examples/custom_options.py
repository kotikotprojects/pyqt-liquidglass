"""Custom GlassOptions example.

Demonstrates how to configure glass effects with custom parameters
including corner radius, padding, and materials.
"""

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

import pyqt_liquidglass as glass


class GlassPanel(QWidget):
    """A panel that will have glass applied to it."""

    def __init__(self, title: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        label = QLabel(title)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            """
            font-size: 16px;
            font-weight: 600;
            color: white;
            background: transparent;
            """
        )

        layout.addWidget(label)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Custom Glass Options")
        self.resize(800, 400)

        central = QWidget()
        central.setStyleSheet("background: transparent;")

        layout = QHBoxLayout(central)
        layout.setContentsMargins(20, 60, 20, 20)
        layout.setSpacing(20)

        # Three panels with different glass options
        self.panel_default = GlassPanel("Default\n(no radius)")
        self.panel_default.setFixedWidth(200)

        self.panel_rounded = GlassPanel("Rounded\n(radius: 16)")
        self.panel_rounded.setFixedWidth(200)

        self.panel_padded = GlassPanel("Padded\n(padding: 20)")
        self.panel_padded.setFixedWidth(200)

        layout.addWidget(self.panel_default)
        layout.addWidget(self.panel_rounded)
        layout.addWidget(self.panel_padded)

        self.setCentralWidget(central)


def main() -> int:
    app = QApplication(sys.argv)

    window = MainWindow()

    glass.prepare_window_for_glass(window)

    window.show()

    # Apply window glass as background
    glass.apply_glass_to_window(window)

    # Apply different glass options to each panel
    # Panel 1: Default options (no corner radius)
    glass.apply_glass_to_widget(
        window.panel_default,
        options=glass.GlassOptions(corner_radius=0.0, padding=(8, 8, 8, 8)),
    )

    # Panel 2: Rounded corners
    glass.apply_glass_to_widget(
        window.panel_rounded,
        options=glass.GlassOptions(corner_radius=16.0, padding=(8, 8, 8, 8)),
    )

    # Panel 3: Large padding
    glass.apply_glass_to_widget(
        window.panel_padded,
        options=glass.GlassOptions(corner_radius=12.0, padding=(20, 20, 20, 20)),
    )

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
