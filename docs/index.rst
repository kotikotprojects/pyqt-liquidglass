pyqt-liquidglass
================

**macOS Liquid Glass effects for PySide6 and PyQt6**

pyqt-liquidglass brings Apple's Liquid Glass visual effects to your Qt applications on macOS. It provides a clean Python API to apply the native ``NSGlassEffectView`` (macOS 26+) or ``NSVisualEffectView`` (fallback) to windows and widgets.

----

Features
--------

- **Window Glass**: Apply glass effects to entire windows
- **Widget Glass**: Target specific widgets like sidebars or panels
- **Traffic Lights Control**: Reposition, hide, or show window buttons
- **GlassOptions**: Configure corner radius, padding, materials, and blending
- **Cross-Version**: Uses ``NSGlassEffectView`` on macOS 26+, falls back to ``NSVisualEffectView``
- **Safe No-ops**: All functions work on non-macOS platforms (return ``None`` or ``False``)

Quick Example
-------------

.. code-block:: python

   from PySide6.QtWidgets import QApplication, QMainWindow
   import pyqt_liquidglass as glass

   app = QApplication([])
   window = QMainWindow()
   window.resize(800, 600)

   # Prepare before showing
   glass.prepare_window_for_glass(window)
   window.show()

   # Apply glass after showing
   glass.apply_glass_to_window(window)

   app.exec()

Installation
------------

.. code-block:: bash

   pip install pyqt-liquidglass

Or with uv:

.. code-block:: bash

   uv add pyqt-liquidglass

**Requirements**: Python 3.12+, macOS, PySide6 or PyQt6

----

Documentation
=============

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   getting_started
   core_concepts
   examples

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api

----

Indices
=======

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

----

License
=======

MIT License. See LICENSE.md for details.
