Getting Started
===============

This guide covers installation and basic usage of pyqt-liquidglass.

Installation
------------

Using pip
~~~~~~~~~

.. code-block:: bash

   pip install pyqt-liquidglass

Using uv
~~~~~~~~

.. code-block:: bash

   uv add pyqt-liquidglass

Requirements
------------

- **Python**: 3.12 or higher
- **Operating System**: macOS (functions are safe no-ops on other platforms)
- **Qt Binding**: PySide6 or PyQt6

The library automatically detects your Qt binding.

Quick Start
-----------

The Three-Step Pattern
~~~~~~~~~~~~~~~~~~~~~~

Every glass effect follows the same pattern:

1. **Prepare** the window before showing
2. **Show** the window
3. **Apply** the glass effect

.. code-block:: python

   import pyqt_liquidglass as glass

   # 1. Prepare before showing
   glass.prepare_window_for_glass(window)

   # 2. Show the window
   window.show()

   # 3. Apply glass after showing
   glass.apply_glass_to_window(window)

Full Window Example
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import sys
   from PySide6.QtCore import Qt
   from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget

   import pyqt_liquidglass as glass


   class MainWindow(QMainWindow):
       def __init__(self) -> None:
           super().__init__()
           self.setWindowTitle("Glass Demo")
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
       glass.prepare_window_for_glass(window)
       window.show()
       glass.apply_glass_to_window(window)

       return app.exec()


   if __name__ == "__main__":
       sys.exit(main())

Key Points
~~~~~~~~~~

- Set ``background: transparent`` on widgets that should show the glass through
- Call ``prepare_window_for_glass()`` before ``show()``
- Call ``apply_glass_to_window()`` after ``show()``
- The window needs to be visible for the native view hierarchy to exist

Widget Glass
~~~~~~~~~~~~

For applying glass to specific widgets (like sidebars):

.. code-block:: python

   sidebar = QWidget()
   sidebar.setFixedWidth(250)
   sidebar.setStyleSheet("background: transparent;")

   # After window.show():
   glass.apply_glass_to_widget(sidebar, options=glass.GlassOptions.sidebar())

Traffic Lights
~~~~~~~~~~~~~~

Reposition the macOS window buttons:

.. code-block:: python

   glass.setup_traffic_lights_inset(window, x_offset=20, y_offset=12)

Hide or show them:

.. code-block:: python

   glass.hide_traffic_lights(window)
   glass.show_traffic_lights(window)

Next Steps
----------

- Learn about :doc:`core_concepts` to understand how glass effects work
- See :doc:`examples` for complete working examples
- Check the :doc:`api` for detailed function signatures
