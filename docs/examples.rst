Examples
========

This page contains complete, runnable examples demonstrating various use cases.

Full Window Glass
-----------------

The simplest example: glass filling the entire window content area.

.. code-block:: python

   """Full window glass effect example."""

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
           label.setStyleSheet("""
               font-size: 28px;
               font-weight: 600;
               color: white;
               background: transparent;
           """)

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

Sidebar Pattern
---------------

Settings-style window with a glass sidebar and opaque content area. This is the most common pattern for macOS applications.

.. code-block:: python

   """Sidebar with glass effect example."""

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
           layout.setContentsMargins(20, 20, 20, 20)

           self.title = QLabel("General")
           self.title.setStyleSheet("""
               font-size: 18px;
               font-weight: bold;
               color: white;
               background: transparent;
           """)

           self.description = QLabel("Configure general application settings.")
           self.description.setStyleSheet("""
               font-size: 14px;
               color: #888888;
               background: transparent;
           """)

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


   def main() -> int:
       app = QApplication(sys.argv)

       window = MainWindow()
       glass.prepare_window_for_glass(window)
       window.show()

       # Inset traffic lights to sit nicely on sidebar
       glass.setup_traffic_lights_inset(window, x_offset=18, y_offset=12)

       # Apply glass to sidebar with rounded corners
       glass.apply_glass_to_widget(window.sidebar, options=glass.GlassOptions.sidebar())

       return app.exec()


   if __name__ == "__main__":
       sys.exit(main())

Frameless Floating Panel
------------------------

A frameless, draggable panel useful for HUDs, tool palettes, or popovers.

.. code-block:: python

   """Frameless window with glass effect example."""

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
           title.setStyleSheet("""
               font-size: 18px;
               font-weight: 600;
               color: white;
               background: transparent;
           """)

           subtitle = QLabel("Drag anywhere to move")
           subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
           subtitle.setStyleSheet("""
               font-size: 12px;
               color: rgba(255, 255, 255, 0.7);
               background: transparent;
           """)

           close_button = QPushButton("Close")
           close_button.setStyleSheet("""
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
           """)
           close_button.clicked.connect(self.close)

           layout.addWidget(title)
           layout.addWidget(subtitle)
           layout.addStretch()
           layout.addWidget(close_button)

       def mousePressEvent(self, event: QMouseEvent) -> None:
           if event.button() == Qt.MouseButton.LeftButton:
               self._drag_position = (
                   event.globalPosition().toPoint() - self.frameGeometry().topLeft()
               )
               event.accept()

       def mouseMoveEvent(self, event: QMouseEvent) -> None:
           if (
               event.buttons() == Qt.MouseButton.LeftButton
               and self._drag_position is not None
           ):
               self.move(event.globalPosition().toPoint() - self._drag_position)
               event.accept()

       def mouseReleaseEvent(self, event: QMouseEvent) -> None:
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

Custom GlassOptions
-------------------

Demonstrates different glass configurations side by side.

.. code-block:: python

   """Custom GlassOptions example."""

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
           label.setStyleSheet("""
               font-size: 16px;
               font-weight: 600;
               color: white;
               background: transparent;
           """)

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
       glass.apply_glass_to_widget(
           window.panel_default,
           options=glass.GlassOptions(corner_radius=0.0, padding=(8, 8, 8, 8)),
       )

       glass.apply_glass_to_widget(
           window.panel_rounded,
           options=glass.GlassOptions(corner_radius=16.0, padding=(8, 8, 8, 8)),
       )

       glass.apply_glass_to_widget(
           window.panel_padded,
           options=glass.GlassOptions(corner_radius=12.0, padding=(20, 20, 20, 20)),
       )

       return app.exec()


   if __name__ == "__main__":
       sys.exit(main())

Traffic Lights Control
----------------------

Demonstrates hiding, showing, and repositioning the macOS window buttons.

.. code-block:: python

   """Traffic lights control example."""

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
           title.setStyleSheet("""
               font-size: 22px;
               font-weight: 600;
               color: white;
               background: transparent;
           """)

           description = QLabel(
               "The traffic lights have been repositioned.\n"
               "Use the button below to hide or show them."
           )
           description.setAlignment(Qt.AlignmentFlag.AlignCenter)
           description.setStyleSheet("""
               font-size: 13px;
               color: rgba(255, 255, 255, 0.7);
               background: transparent;
           """)

           buttons_layout = QHBoxLayout()
           buttons_layout.setSpacing(12)

           self.toggle_button = QPushButton("Hide Traffic Lights")
           self.toggle_button.setStyleSheet("""
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
           """)
           self.toggle_button.clicked.connect(self._toggle_traffic_lights)

           buttons_layout.addStretch()
           buttons_layout.addWidget(self.toggle_button)
           buttons_layout.addStretch()

           layout.addWidget(title)
           layout.addWidget(description)
           layout.addStretch()
           layout.addLayout(buttons_layout)

           self.setCentralWidget(central)

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
