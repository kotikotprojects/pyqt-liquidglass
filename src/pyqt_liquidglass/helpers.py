"""Helper functions for preparing Qt widgets for glass effects."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._bridge import get_nswindow_from_widget
from ._platform import IS_MACOS

if TYPE_CHECKING:
    from ._compat import QtWidgets

__all__ = [
    "prepare_widget_for_glass",
    "prepare_window_for_glass",
    "set_window_background_transparent",
]

_NS_FULL_SIZE_CONTENT_VIEW_WINDOW_MASK: int = 1 << 15
_NS_WINDOW_TITLE_HIDDEN: int = 1
_NS_WINDOW_STYLE_MASK_BORDERLESS: int = 0


def prepare_window_for_glass(
    window: QtWidgets.QWidget,
    *,
    frameless: bool = False,
    transparent_titlebar: bool = True,
    full_size_content: bool = True,
) -> None:
    """
    Prepare a window for glass effects.

    Sets the necessary Qt widget attributes and configures the native
    NSWindow properties for glass effect rendering.

    Args:
        window: The window widget to prepare.
        frameless: If True, remove the window frame entirely using
            Qt.FramelessWindowHint.
        transparent_titlebar: If True, make the titlebar transparent
            on macOS so glass can extend underneath.
        full_size_content: If True, extend content view to cover the
            titlebar area.

    Note:
        Call this before showing the window for best results.
    """
    from ._compat import QtCore  # noqa: PLC0415

    window.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

    if frameless:
        window.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)

    if not IS_MACOS:
        return

    window.show()

    ns_window = get_nswindow_from_widget(window)
    if ns_window is None:
        return

    if frameless:
        ns_window.setHasShadow_(False)  # ty: ignore  # Keep shadow for depth
        return

    if full_size_content:
        current_mask = ns_window.styleMask()  # ty: ignore
        ns_window.setStyleMask_(  # ty: ignore
            current_mask | _NS_FULL_SIZE_CONTENT_VIEW_WINDOW_MASK
        )

    if transparent_titlebar:
        ns_window.setTitlebarAppearsTransparent_(True)  # ty: ignore
        ns_window.setTitleVisibility_(_NS_WINDOW_TITLE_HIDDEN)  # ty: ignore


def prepare_widget_for_glass(widget: QtWidgets.QWidget) -> None:
    """
    Prepare a widget for having glass effect applied.

    Sets the necessary Qt attributes for the widget to render correctly
    with a glass effect behind it. The widget's content will be visible
    on top of the glass effect.

    Args:
        widget: The widget to prepare.

    Note:
        This sets WA_TranslucentBackground which makes the widget
        background transparent. Ensure your widget's stylesheet or
        paint event handles the transparent background appropriately.
    """
    from ._compat import QtCore  # noqa: PLC0415

    widget.setAttribute(QtCore.Qt.WidgetAttribute.WA_NativeWindow)
    widget.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)


def set_window_background_transparent(window: QtWidgets.QWidget) -> None:
    """
    Make a window's background fully transparent.

    This is useful when you want complete control over the window
    appearance, such as creating a fully custom-drawn window with
    glass effects.

    Args:
        window: The window to make transparent.

    Note:
        After calling this, the window will have no visible background.
        You must provide your own background through stylesheets or
        painting.
    """
    from ._compat import QtCore, QtGui  # noqa: PLC0415

    window.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
    window.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoSystemBackground)

    palette = window.palette()
    palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(0, 0, 0, 0))
    window.setPalette(palette)

    if IS_MACOS:
        ns_window = get_nswindow_from_widget(window)
        if ns_window is not None:
            from AppKit import NSColor  # noqa: PLC0415  # ty: ignore

            ns_window.setOpaque_(False)  # ty: ignore
            ns_window.setBackgroundColor_(NSColor.clearColor())  # ty: ignore
