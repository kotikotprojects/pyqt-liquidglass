"""Bridge utilities for converting Qt objects to native macOS Cocoa objects."""

from __future__ import annotations

from ctypes import c_void_p
from typing import TYPE_CHECKING, Any

from ._compat import QtWidgets, get_window_id
from ._platform import IS_MACOS

if TYPE_CHECKING:
    from ._compat import QtCore

__all__ = [
    "convert_qt_rect_to_ns_frame",
    "get_nsview_from_widget",
    "get_nswindow_from_widget",
]


def get_nsview_from_widget(widget: QtWidgets.QWidget) -> Any | None:  # noqa: ANN401
    """
    Get the NSView backing a QWidget.

    Args:
        widget: A Qt widget that has been realized (shown on screen).

    Returns:
        The NSView object (as a PyObjC object), or None if unavailable
        or not on macOS.

    Note:
        The widget must have a valid window ID, which typically requires
        the widget to be shown before calling this function.
    """
    if not IS_MACOS:
        return None

    try:
        import objc  # noqa: PLC0415  # ty: ignore

        win_id = get_window_id(widget)
        return objc.objc_object(c_void_p=c_void_p(win_id))  # ty: ignore
    except Exception:  # noqa: BLE001
        return None


def get_nswindow_from_widget(widget: QtWidgets.QWidget) -> Any | None:  # noqa: ANN401
    """
    Get the NSWindow containing a QWidget.

    Args:
        widget: A Qt widget that has been realized (shown on screen).

    Returns:
        The NSWindow object (as a PyObjC object), or None if unavailable
        or not on macOS.
    """
    ns_view = get_nsview_from_widget(widget)
    if ns_view is None:
        return None

    try:
        return ns_view.window()  # ty: ignore
    except Exception:  # noqa: BLE001
        return None


def convert_qt_rect_to_ns_frame(
    qt_rect: QtCore.QRect, container_height: float, *, is_flipped: bool = False
) -> tuple[float, float, float, float]:
    """
    Convert a Qt rectangle to Cocoa NSRect coordinates.

    Qt uses a top-left origin coordinate system where Y increases downward.
    Cocoa (when not flipped) uses a bottom-left origin where Y increases
    upward.

    Args:
        qt_rect: Rectangle in Qt coordinates.
        container_height: Height of the container view for Y-axis conversion.
        is_flipped: Whether the container view uses flipped coordinates
            (top-left origin like Qt). Default is False (standard Cocoa).

    Returns:
        A tuple of (x, y, width, height) in Cocoa coordinates.
    """
    x = float(qt_rect.x())
    width = float(qt_rect.width())
    height = float(qt_rect.height())

    if is_flipped:
        y = float(qt_rect.y())
    else:
        y = container_height - float(qt_rect.y()) - height

    return (x, y, width, height)
