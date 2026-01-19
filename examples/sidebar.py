"""Sidebar with glass effect example.

Settings-style window with a glass sidebar and opaque content area.
This is the most common pattern for using Liquid Glass.
"""

import sys

from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

import pyqt_liquidglass as glass


class Sidebar(QWidget):
    """Transparent sidebar widget for glass effect."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedWidth(250)
        self.setStyleSheet("background: transparent;")

        layout = QVBoxLayout(self)
        # Top padding for traffic lights area
        layout.setContentsMargins(9, 18, 9, 9)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                font-size: 13px;
                background: transparent;
                border: none;
                outline: none;
            }
            QListWidget::item {
                padding: 5px 2px;
                margin: 0px 9px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background: rgba(255, 255, 255, 0.1);
            }
        """)
        self.list_widget.viewport().setStyleSheet("background: transparent;")

        for item_text in ["General", "Appearance", "Sound", "Network", "Privacy"]:
            self.list_widget.addItem(QListWidgetItem(item_text))

        self.list_widget.setCurrentRow(0)
        layout.addWidget(self.list_widget)


class Content(QWidget):
    """Opaque content area."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setStyleSheet("background-color: #1e1e1e;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 20)

        self.title = QLabel("General")
        self.title.setStyleSheet(
            """
            font-size: 18px;
            font-weight: bold;
            color: white;
            background: transparent;
            """
        )

        self.description = QLabel("Configure general application settings.")
        self.description.setStyleSheet(
            """
            font-size: 14px;
            color: #888888;
            background: transparent;
            """
        )

        layout.addWidget(self.title)
        layout.addSpacing(8)
        layout.addWidget(self.description)
        layout.addStretch()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Settings")
        self.resize(720, 600)

        central = QWidget()
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = Sidebar()
        self.content = Content()

        layout.addWidget(self.sidebar)
        layout.addWidget(self.content, 1)

        self.setCentralWidget(central)

        self.sidebar.list_widget.currentRowChanged.connect(self._on_selection_changed)

    def _on_selection_changed(self, row: int) -> None:
        items = ["General", "Appearance", "Sound", "Network", "Privacy"]
        descriptions = [
            "Configure general application settings.",
            "Customize colors, fonts, and themes.",
            "Adjust volume and audio devices.",
            "Manage network connections and proxy.",
            "Control permissions and data sharing.",
        ]
        if 0 <= row < len(items):
            self.content.title.setText(items[row])
            self.content.description.setText(descriptions[row])


def main() -> int:
    app = QApplication(sys.argv)

    window = MainWindow()

    # Prepare window before showing
    glass.prepare_window_for_glass(window)

    window.show()

    # Inset traffic lights to sit nicely on sidebar
    glass.setup_traffic_lights_inset(window, x_offset=18, y_offset=12)

    # Apply glass to sidebar with rounded corners
    glass.apply_glass_to_widget(window.sidebar, options=glass.GlassOptions.sidebar())

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
