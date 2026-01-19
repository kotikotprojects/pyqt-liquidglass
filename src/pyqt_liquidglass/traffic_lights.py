"""Traffic light (window button) positioning for macOS windows."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ._bridge import get_nsview_from_widget
from ._platform import platform_guard

if TYPE_CHECKING:
    from ._compat import QtWidgets

__all__ = ["hide_traffic_lights", "setup_traffic_lights_inset", "show_traffic_lights"]

_NS_WINDOW_CLOSE_BUTTON: int = 0
_NS_WINDOW_MINIATURIZE_BUTTON: int = 1
_NS_WINDOW_ZOOM_BUTTON: int = 2
_NS_WINDOW_TITLE_HIDDEN: int = 1
_NS_FULL_SIZE_CONTENT_VIEW_WINDOW_MASK: int = 1 << 15

_NS_LAYOUT_ATTRIBUTE_LEADING: int = 5
_NS_LAYOUT_ATTRIBUTE_TRAILING: int = 6
_NS_LAYOUT_ATTRIBUTE_CENTER_Y: int = 10
_NS_LAYOUT_RELATION_EQUAL: int = 0


def _get_traffic_light_buttons(ns_window: Any) -> tuple[Any, Any, Any]:  # noqa: ANN401
    """Get the close, minimize, and zoom buttons from an NSWindow."""
    close_btn = ns_window.standardWindowButton_(_NS_WINDOW_CLOSE_BUTTON)  # ty: ignore
    minimize_btn = ns_window.standardWindowButton_(_NS_WINDOW_MINIATURIZE_BUTTON)  # ty: ignore
    zoom_btn = ns_window.standardWindowButton_(_NS_WINDOW_ZOOM_BUTTON)  # ty: ignore
    return close_btn, minimize_btn, zoom_btn


@platform_guard
def setup_traffic_lights_inset(
    window: QtWidgets.QWidget, x_offset: float = 0.0, y_offset: float = 0.0
) -> bool:
    """
    Reposition the traffic light buttons (close, minimize, zoom).

    Uses NSLayoutConstraint to position the buttons with an offset from
    their default location. This method is more robust than frame-based
    positioning as it survives window resizes.

    Args:
        window: The window whose traffic lights to reposition.
        x_offset: Horizontal offset in points from the left edge.
        y_offset: Vertical offset in points from the center.

    Returns:
        True if the traffic lights were successfully repositioned,
        False otherwise.

    Note:
        This function configures the window for full-size content view
        and transparent titlebar automatically.
    """
    ns_view = get_nsview_from_widget(window)
    if ns_view is None:
        return False

    ns_window = ns_view.window()  # ty: ignore
    if ns_window is None:
        return False

    from AppKit import NSLayoutConstraint  # noqa: PLC0415  # ty: ignore

    current_mask = ns_window.styleMask()  # ty: ignore
    ns_window.setStyleMask_(  # ty: ignore
        current_mask | _NS_FULL_SIZE_CONTENT_VIEW_WINDOW_MASK
    )
    ns_window.setTitlebarAppearsTransparent_(True)  # ty: ignore
    ns_window.setTitleVisibility_(_NS_WINDOW_TITLE_HIDDEN)  # ty: ignore

    close_btn, minimize_btn, zoom_btn = _get_traffic_light_buttons(ns_window)

    if close_btn is None:
        return False

    close_btn.setTranslatesAutoresizingMaskIntoConstraints_(False)  # ty: ignore
    if minimize_btn is not None:
        minimize_btn.setTranslatesAutoresizingMaskIntoConstraints_(False)  # ty: ignore
    if zoom_btn is not None:
        zoom_btn.setTranslatesAutoresizingMaskIntoConstraints_(False)  # ty: ignore

    superview = close_btn.superview()  # ty: ignore
    if superview is None:
        return False

    button_spacing = 6.0
    make_constraint = (  # ty: ignore
        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_
    )

    constraint_close_x = make_constraint(
        close_btn,
        _NS_LAYOUT_ATTRIBUTE_LEADING,
        _NS_LAYOUT_RELATION_EQUAL,
        superview,
        _NS_LAYOUT_ATTRIBUTE_LEADING,
        1.0,
        x_offset,
    )
    superview.addConstraint_(constraint_close_x)  # ty: ignore

    constraint_close_y = make_constraint(
        close_btn,
        _NS_LAYOUT_ATTRIBUTE_CENTER_Y,
        _NS_LAYOUT_RELATION_EQUAL,
        superview,
        _NS_LAYOUT_ATTRIBUTE_CENTER_Y,
        1.0,
        y_offset,
    )
    superview.addConstraint_(constraint_close_y)  # ty: ignore

    if minimize_btn is not None:
        constraint_min_x = make_constraint(
            minimize_btn,
            _NS_LAYOUT_ATTRIBUTE_LEADING,
            _NS_LAYOUT_RELATION_EQUAL,
            close_btn,
            _NS_LAYOUT_ATTRIBUTE_TRAILING,
            1.0,
            button_spacing,
        )
        superview.addConstraint_(constraint_min_x)  # ty: ignore

        constraint_min_y = make_constraint(
            minimize_btn,
            _NS_LAYOUT_ATTRIBUTE_CENTER_Y,
            _NS_LAYOUT_RELATION_EQUAL,
            superview,
            _NS_LAYOUT_ATTRIBUTE_CENTER_Y,
            1.0,
            y_offset,
        )
        superview.addConstraint_(constraint_min_y)  # ty: ignore

    if zoom_btn is not None and minimize_btn is not None:
        constraint_zoom_x = make_constraint(
            zoom_btn,
            _NS_LAYOUT_ATTRIBUTE_LEADING,
            _NS_LAYOUT_RELATION_EQUAL,
            minimize_btn,
            _NS_LAYOUT_ATTRIBUTE_TRAILING,
            1.0,
            button_spacing,
        )
        superview.addConstraint_(constraint_zoom_x)  # ty: ignore

        constraint_zoom_y = make_constraint(
            zoom_btn,
            _NS_LAYOUT_ATTRIBUTE_CENTER_Y,
            _NS_LAYOUT_RELATION_EQUAL,
            superview,
            _NS_LAYOUT_ATTRIBUTE_CENTER_Y,
            1.0,
            y_offset,
        )
        superview.addConstraint_(constraint_zoom_y)  # ty: ignore

    return True


@platform_guard
def hide_traffic_lights(window: QtWidgets.QWidget) -> bool:
    """
    Hide the traffic light buttons while keeping window functionality.

    The buttons are hidden but the window remains closable, minimizable,
    and zoomable via keyboard shortcuts and menu commands.

    Args:
        window: The window whose traffic lights to hide.

    Returns:
        True if successful, False otherwise.
    """
    ns_view = get_nsview_from_widget(window)
    if ns_view is None:
        return False

    ns_window = ns_view.window()  # ty: ignore
    if ns_window is None:
        return False

    close_btn, minimize_btn, zoom_btn = _get_traffic_light_buttons(ns_window)

    for btn in (close_btn, minimize_btn, zoom_btn):
        if btn is not None:
            btn.setHidden_(True)  # ty: ignore

    return True


@platform_guard
def show_traffic_lights(window: QtWidgets.QWidget) -> bool:
    """
    Show previously hidden traffic light buttons.

    Args:
        window: The window whose traffic lights to show.

    Returns:
        True if successful, False otherwise.
    """
    ns_view = get_nsview_from_widget(window)
    if ns_view is None:
        return False

    ns_window = ns_view.window()  # ty: ignore
    if ns_window is None:
        return False

    close_btn, minimize_btn, zoom_btn = _get_traffic_light_buttons(ns_window)

    for btn in (close_btn, minimize_btn, zoom_btn):
        if btn is not None:
            btn.setHidden_(False)  # ty: ignore

    return True
