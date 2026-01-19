"""
pyqt-liquidglass: macOS Liquid Glass effects for PySide6/PyQt6.

This library provides a simple API to apply Apple's Liquid Glass visual
effects to Qt windows and widgets on macOS. On non-macOS platforms, all
functions are safe no-ops that return None or False.

Basic Usage::

    from PySide6.QtWidgets import QApplication, QMainWindow
    import pyqt_liquidglass as glass

    app = QApplication([])
    window = QMainWindow()
    window.setWindowTitle("Glass Demo")
    window.resize(800, 600)

    glass.prepare_window_for_glass(window)
    window.show()

    glass.apply_glass_to_window(window)
    glass.setup_traffic_lights_inset(window, x_offset=20, y_offset=15)

    app.exec()

Widget-specific glass (e.g., sidebar)::

    sidebar = QWidget()
    sidebar.setFixedWidth(200)
    glass.prepare_widget_for_glass(sidebar)

    # After window.show():
    glass.apply_glass_to_widget(
        sidebar, options=glass.GlassOptions.sidebar(corner_radius=12)
    )

"""

from __future__ import annotations

__version__ = "0.1.0"

from ._platform import HAS_GLASS_EFFECT, HAS_VISUAL_EFFECT, IS_MACOS, MACOS_VERSION
from ._types import BlendingMode, GlassMaterial, GlassOptions
from .glass import apply_glass_to_widget, apply_glass_to_window, remove_glass_effect
from .helpers import (
    prepare_widget_for_glass,
    prepare_window_for_glass,
    set_window_background_transparent,
)
from .traffic_lights import (
    hide_traffic_lights,
    setup_traffic_lights_inset,
    show_traffic_lights,
)

__all__ = [
    "HAS_GLASS_EFFECT",
    "HAS_VISUAL_EFFECT",
    "IS_MACOS",
    "MACOS_VERSION",
    "BlendingMode",
    "GlassMaterial",
    "GlassOptions",
    "__version__",
    "apply_glass_to_widget",
    "apply_glass_to_window",
    "hide_traffic_lights",
    "prepare_widget_for_glass",
    "prepare_window_for_glass",
    "remove_glass_effect",
    "set_window_background_transparent",
    "setup_traffic_lights_inset",
    "show_traffic_lights",
]
