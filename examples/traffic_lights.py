"""Traffic lights control example.

Demonstrates hiding, showing, and repositioning the macOS window
traffic lights (close, minimize, zoom buttons).
"""

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

import pyqt_liquidglass as glass


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Traffic Lights Demo")
        self.resize(500, 300)

        self._lights_visible = True

        central = QWidget()
        central.setStyleSheet("background: transparent;")

        layout = QVBoxLayout(central)
        layout.setContentsMargins(40, 80, 40, 40)
        layout.setSpacing(20)

        title = QLabel("Traffic Lights Control")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            """
            font-size: 22px;
            font-weight: 600;
            color: white;
            background: transparent;
            """
        )

        description = QLabel(
            "The traffic lights have been repositioned.\n"
            "Use the buttons below to hide or show them."
        )
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setStyleSheet(
            """
            font-size: 13px;
            color: rgba(255, 255, 255, 0.7);
            background: transparent;
            """
        )

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)

        self.toggle_button = QPushButton("Hide Traffic Lights")
        self.toggle_button.setStyleSheet(self._button_style())
        self.toggle_button.clicked.connect(self._toggle_traffic_lights)

        buttons_layout.addStretch()
        buttons_layout.addWidget(self.toggle_button)
        buttons_layout.addStretch()

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addStretch()
        layout.addLayout(buttons_layout)

        self.setCentralWidget(central)

    def _button_style(self) -> str:
        return """
            QPushButton {
                background: rgba(255, 255, 255, 0.15);
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                color: white;
                font-size: 13px;
                min-width: 160px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.25);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.1);
            }
        """

    def _toggle_traffic_lights(self) -> None:
        if self._lights_visible:
            glass.hide_traffic_lights(self)
            self.toggle_button.setText("Show Traffic Lights")
        else:
            glass.show_traffic_lights(self)
            self.toggle_button.setText("Hide Traffic Lights")
        self._lights_visible = not self._lights_visible


def main() -> int:
    app = QApplication(sys.argv)

    window = MainWindow()

    glass.prepare_window_for_glass(window)

    window.show()

    # Apply glass to window
    glass.apply_glass_to_window(window)

    # Reposition traffic lights with custom offset
    glass.setup_traffic_lights_inset(window, x_offset=20, y_offset=16)

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
