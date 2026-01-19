"""Full window glass effect example.

The simplest possible example: a window with glass filling the entire
content area.
"""

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget

import pyqt_liquidglass as glass


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Window Glass")
        self.resize(600, 400)

        central = QWidget()
        central.setStyleSheet("background: transparent;")

        layout = QVBoxLayout(central)
        layout.setContentsMargins(40, 60, 40, 40)

        label = QLabel("Hello, Liquid Glass!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            """
            font-size: 28px;
            font-weight: 600;
            color: white;
            background: transparent;
            """
        )

        layout.addWidget(label)
        self.setCentralWidget(central)


def main() -> int:
    app = QApplication(sys.argv)

    window = MainWindow()

    # Prepare window BEFORE showing
    glass.prepare_window_for_glass(window)

    window.show()

    # Apply glass AFTER showing
    glass.apply_glass_to_window(window)

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
