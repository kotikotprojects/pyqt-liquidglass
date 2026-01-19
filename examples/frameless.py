"""Frameless window with glass effect example.

A floating panel without standard window decorations, useful for
custom UI elements like popovers, HUDs, or tool palettes.
"""

import sys

from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget

import pyqt_liquidglass as glass


class FloatingPanel(QWidget):
    """A frameless, draggable floating panel with glass effect."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Floating Panel")
        self.resize(300, 200)

        self._drag_position: QPoint | None = None

        self.setStyleSheet("background: transparent;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Floating Panel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            """
            font-size: 18px;
            font-weight: 600;
            color: white;
            background: transparent;
            """
        )

        subtitle = QLabel("Drag anywhere to move")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(
            """
            font-size: 12px;
            color: rgba(255, 255, 255, 0.7);
            background: transparent;
            """
        )

        close_button = QPushButton("Close")
        close_button.setStyleSheet(
            """
            QPushButton {
                background: rgba(255, 255, 255, 0.15);
                border: none;
                border-radius: 8px;
                padding: 10px 24px;
                color: white;
                font-size: 13px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.25);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.1);
            }
            """
        )
        close_button.clicked.connect(self.close)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()
        layout.addWidget(close_button)

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if (
            event.buttons() == Qt.MouseButton.LeftButton
            and self._drag_position is not None
        ):
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802, ARG002
        self._drag_position = None


def main() -> int:
    app = QApplication(sys.argv)

    panel = FloatingPanel()

    # Prepare with frameless=True to remove window decorations
    glass.prepare_window_for_glass(panel, frameless=True)

    panel.show()

    # Apply glass with rounded corners for the floating look
    glass.apply_glass_to_window(panel, options=glass.GlassOptions(corner_radius=16.0))

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
