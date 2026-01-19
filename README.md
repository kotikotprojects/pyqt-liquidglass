# pyqt-liquidglass

[![PyPI version](https://badge.fury.io/py/pyqt-liquidglass.svg)](https://pypi.org/project/pyqt-liquidglass/)
[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE.md)
[![Documentation](https://readthedocs.org/projects/pyqt-liquidglass/badge/?version=latest)](https://pyqt-liquidglass.readthedocs.io)

macOS Liquid Glass effects for PySide6 and PyQt6.

![Screenshot](assets/screenshot.png)

## Overview

pyqt-liquidglass provides a Python API to apply Apple's native glass visual effects to Qt windows and widgets. On macOS 26+, it uses `NSGlassEffectView` for Liquid Glass. On older versions, it falls back to `NSVisualEffectView`.

## Features

- Apply glass effects to entire windows or specific widgets
- Configure corner radius, padding, and materials
- Reposition, hide, or show window traffic lights
- Automatic Qt binding detection (PySide6, PyQt6)
- Safe no-ops on non-macOS platforms

## Installation

```bash
pip install pyqt-liquidglass
```

Or with uv:

```bash
uv add pyqt-liquidglass
```

## Quick Start

```python
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
```

### Sidebar Pattern

```python
# Apply glass to a sidebar widget
glass.apply_glass_to_widget(sidebar, options=glass.GlassOptions.sidebar())

# Position traffic lights
glass.setup_traffic_lights_inset(window, x_offset=18, y_offset=12)
```

### Custom Options

```python
options = glass.GlassOptions(
    corner_radius=16.0,
    padding=(10, 10, 10, 10),
)
glass.apply_glass_to_window(window, options=options)
```

## Requirements

- Python 3.12+
- macOS
- PySide6 or PyQt6

Tested with PySide6. PyQt6 should work but is not explicitly tested.

## Documentation

Full documentation: [pyqt-liquidglass.readthedocs.io](https://pyqt-liquidglass.readthedocs.io)

## License

MIT
