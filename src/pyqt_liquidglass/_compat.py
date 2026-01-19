"""Qt binding compatibility layer for PySide6 and PyQt6."""

from __future__ import annotations

from typing import Literal

__all__ = [
    "PYQT6",
    "PYSIDE6",
    "QT_BINDING",
    "QtCore",
    "QtGui",
    "QtWidgets",
    "get_window_id",
]

PYSIDE6: bool = False
PYQT6: bool = False
QT_BINDING: Literal["PySide6", "PyQt6", "none"] = "none"

try:
    from PySide6 import QtCore, QtGui, QtWidgets

    PYSIDE6 = True
    QT_BINDING = "PySide6"
except ImportError:
    try:
        from PyQt6 import QtCore, QtGui, QtWidgets

        PYQT6 = True
        QT_BINDING = "PyQt6"
    except ImportError:
        msg = (
            "No Qt binding found. Install either PySide6 or PyQt6:\n"
            "  pip install PySide6\n"
            "  pip install PyQt6"
        )
        raise ImportError(msg) from None


def get_window_id(widget: QtWidgets.QWidget) -> int:
    """
    Get the native window ID from a Qt widget.

    Args:
        widget: A Qt widget that has been realized (shown).

    Returns:
        The native window ID as an integer.

    Note:
        PySide6 returns an int directly, while PyQt6 returns a sip.voidptr
        that needs to be converted.
    """
    win_id = widget.winId()
    if PYQT6:
        return int(win_id)  # type: ignore[arg-type]
    return win_id  # type: ignore[return-value]
