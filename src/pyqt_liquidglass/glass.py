"""Core glass effect implementation for macOS Liquid Glass."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ._bridge import get_nsview_from_widget
from ._platform import HAS_GLASS_EFFECT, IS_MACOS, platform_guard
from ._types import BlendingMode, GlassOptions

if TYPE_CHECKING:
    from ._compat import QtWidgets

__all__ = ["apply_glass_to_widget", "apply_glass_to_window", "remove_glass_effect"]

_effect_registry: dict[int, tuple[Any, Any]] = {}
_next_effect_id: int = 0

_NS_WINDOW_BELOW: int = -1
_NS_VIEW_WIDTH_SIZABLE: int = 2
_NS_VIEW_HEIGHT_SIZABLE: int = 16
_NS_VIEW_MAX_X_MARGIN: int = 4
_NS_FULL_SIZE_CONTENT_VIEW_WINDOW_MASK: int = 1 << 15


def _create_glass_view(frame: Any, options: GlassOptions) -> Any | None:  # noqa: ANN401
    """
    Create an NSGlassEffectView or NSVisualEffectView.

    Attempts to use NSGlassEffectView on macOS 26+, falling back to
    NSVisualEffectView on older versions.

    Args:
        frame: NSRect for the view's frame.
        options: Glass effect configuration.

    Returns:
        The created view, or None on failure.
    """
    import objc  # noqa: PLC0415  # ty: ignore

    if HAS_GLASS_EFFECT:
        try:
            glass_cls = objc.lookUpClass("NSGlassEffectView")  # ty: ignore
            glass = glass_cls.alloc().initWithFrame_(frame)  # ty: ignore
            if options.corner_radius > 0:
                glass.setCornerRadius_(options.corner_radius)  # ty: ignore
        except objc.nosuchclass_error:  # ty: ignore
            pass
        else:
            return glass

    try:
        from AppKit import (  # noqa: PLC0415  # ty: ignore
            NSVisualEffectBlendingModeBehindWindow,
            NSVisualEffectBlendingModeWithinWindow,
            NSVisualEffectStateActive,
            NSVisualEffectView,
        )

        glass = NSVisualEffectView.alloc().initWithFrame_(frame)  # ty: ignore
        glass.setMaterial_(options.material.value)  # ty: ignore

        blending = (
            NSVisualEffectBlendingModeBehindWindow  # ty: ignore
            if options.blending_mode == BlendingMode.BEHIND_WINDOW
            else NSVisualEffectBlendingModeWithinWindow  # ty: ignore
        )
        glass.setBlendingMode_(blending)  # ty: ignore
        glass.setState_(NSVisualEffectStateActive)  # ty: ignore
    except Exception:  # noqa: BLE001
        return None
    else:
        return glass


def _configure_window_for_glass(ns_window: Any) -> None:  # noqa: ANN401
    """Configure NSWindow properties for full window glass effect rendering."""
    from AppKit import NSColor  # noqa: PLC0415  # ty: ignore

    ns_window.setOpaque_(False)  # ty: ignore
    ns_window.setBackgroundColor_(NSColor.clearColor())  # ty: ignore

    current_mask = ns_window.styleMask()  # ty: ignore
    ns_window.setStyleMask_(current_mask | _NS_FULL_SIZE_CONTENT_VIEW_WINDOW_MASK)  # ty: ignore
    ns_window.setTitlebarAppearsTransparent_(True)  # ty: ignore


def _configure_titlebar_for_glass(ns_window: Any) -> None:  # noqa: ANN401
    """Configure only titlebar for widget-level glass (no window transparency)."""
    current_mask = ns_window.styleMask()  # ty: ignore
    ns_window.setStyleMask_(current_mask | _NS_FULL_SIZE_CONTENT_VIEW_WINDOW_MASK)  # ty: ignore
    ns_window.setTitlebarAppearsTransparent_(True)  # ty: ignore


@platform_guard
def apply_glass_to_window(
    window: QtWidgets.QWidget, options: GlassOptions | None = None
) -> int | None:
    """
    Apply glass effect to an entire window.

    Creates an NSGlassEffectView (macOS 26+) or NSVisualEffectView (fallback)
    that fills the window's content area behind all Qt content.

    Uses one of three strategies based on window configuration:
    1. Sibling Injection: If root view has a superview, adds glass as sibling
    2. Content Swap: For frameless windows, creates a container and swaps
    3. Child Fallback: Adds glass inside root view at bottom of z-order

    Args:
        window: A top-level QWidget (typically QMainWindow).
        options: Glass effect configuration. Uses defaults if None.

    Returns:
        An effect ID for later removal, or None if the effect could not
        be applied.

    Note:
        The window should be shown before calling this function.
    """
    if options is None:
        options = GlassOptions.window()

    root_view = get_nsview_from_widget(window)
    if root_view is None:
        return None

    ns_window = root_view.window()  # ty: ignore
    if ns_window is None:
        return None

    from AppKit import NSView  # noqa: PLC0415  # ty: ignore
    from Foundation import NSMakeRect  # noqa: PLC0415  # ty: ignore

    superview = root_view.superview()  # ty: ignore
    content_view = ns_window.contentView()  # ty: ignore

    container: Any = None
    performed_swap = False

    if superview is not None:
        container = superview
    elif root_view == content_view:
        frame = root_view.frame()  # ty: ignore
        new_container = NSView.alloc().initWithFrame_(frame)  # ty: ignore
        new_container.setAutoresizingMask_(  # ty: ignore
            _NS_VIEW_WIDTH_SIZABLE | _NS_VIEW_HEIGHT_SIZABLE
        )
        new_container.setWantsLayer_(True)  # ty: ignore

        ns_window.setContentView_(new_container)  # ty: ignore

        root_view.setFrame_(new_container.bounds())  # ty: ignore
        root_view.setAutoresizingMask_(  # ty: ignore
            _NS_VIEW_WIDTH_SIZABLE | _NS_VIEW_HEIGHT_SIZABLE
        )
        new_container.addSubview_(root_view)  # ty: ignore

        container = root_view.superview()  # ty: ignore
        performed_swap = True
    else:
        container = root_view

    _configure_window_for_glass(ns_window)

    if container == root_view.superview():  # ty: ignore
        frame_rect = root_view.frame()  # ty: ignore
    else:
        frame_rect = root_view.bounds()  # ty: ignore

    if performed_swap:
        frame_rect = container.bounds()  # ty: ignore

    pad_left, pad_top, pad_right, pad_bottom = options.padding
    frame_rect = NSMakeRect(  # ty: ignore
        frame_rect.origin.x + pad_left,  # ty: ignore
        frame_rect.origin.y + pad_bottom,  # ty: ignore
        frame_rect.size.width - pad_left - pad_right,  # ty: ignore
        frame_rect.size.height - pad_top - pad_bottom,  # ty: ignore
    )

    glass = _create_glass_view(frame_rect, options)
    if glass is None:
        return None

    glass.setAutoresizingMask_(_NS_VIEW_WIDTH_SIZABLE | _NS_VIEW_HEIGHT_SIZABLE)  # ty: ignore

    if container == root_view.superview():  # ty: ignore
        container.addSubview_positioned_relativeTo_(  # ty: ignore
            glass, _NS_WINDOW_BELOW, root_view
        )
    else:
        container.addSubview_positioned_relativeTo_(  # ty: ignore
            glass, _NS_WINDOW_BELOW, None
        )

    global _next_effect_id  # noqa: PLW0603
    effect_id = _next_effect_id
    _next_effect_id += 1
    _effect_registry[effect_id] = (glass, container)

    window._glass_view = glass  # type: ignore[attr-defined]  # noqa: SLF001  # ty: ignore

    return effect_id


@platform_guard
def apply_glass_to_widget(
    widget: QtWidgets.QWidget, options: GlassOptions | None = None
) -> int | None:
    """
    Apply glass effect to a specific widget.

    Creates a glass effect view sized and positioned to match the widget's
    geometry within its parent window.

    Args:
        widget: The widget to apply the glass effect to.
        options: Glass effect configuration. Uses GlassOptions.sidebar()
            defaults if None.

    Returns:
        An effect ID for later removal, or None if the effect could not
        be applied.

    Note:
        The widget must be visible and part of a shown window.
        The effect view tracks widget resize and move events.
    """
    from ._compat import QtCore  # noqa: PLC0415

    if options is None:
        options = GlassOptions.sidebar()

    widget.setAttribute(QtCore.Qt.WidgetAttribute.WA_NativeWindow)
    widget.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

    ns_view = get_nsview_from_widget(widget)
    if ns_view is None:
        return None

    ns_window = ns_view.window()  # ty: ignore
    if ns_window is None:
        return None

    superview = ns_view.superview()  # ty: ignore
    if superview is None:
        return None

    from Foundation import NSMakeRect  # noqa: PLC0415  # ty: ignore

    _configure_titlebar_for_glass(ns_window)

    content_view = ns_window.contentView()  # ty: ignore
    sidebar_frame = ns_view.frame()  # ty: ignore
    content_frame = content_view.frame()  # ty: ignore

    pad_left, pad_top, pad_right, pad_bottom = options.padding

    glass_frame = NSMakeRect(  # ty: ignore
        sidebar_frame.origin.x + pad_left,  # ty: ignore
        pad_bottom,
        sidebar_frame.size.width - pad_left - pad_right,  # ty: ignore
        content_frame.size.height - pad_top - pad_bottom,  # ty: ignore
    )

    glass = _create_glass_view(glass_frame, options)
    if glass is None:
        return None

    glass.setAutoresizingMask_(_NS_VIEW_HEIGHT_SIZABLE | _NS_VIEW_MAX_X_MARGIN)  # ty: ignore
    content_view.addSubview_positioned_relativeTo_(glass, _NS_WINDOW_BELOW, None)  # ty: ignore

    def update_glass_frame() -> None:
        sf = ns_view.frame()  # ty: ignore
        cf = content_view.frame()  # ty: ignore
        new_frame = NSMakeRect(  # ty: ignore
            sf.origin.x + pad_left,  # ty: ignore
            pad_bottom,
            sf.size.width - pad_left - pad_right,  # ty: ignore
            cf.size.height - pad_top - pad_bottom,  # ty: ignore
        )
        glass.setFrame_(new_frame)  # ty: ignore

    original_resize = widget.resizeEvent
    original_move = widget.moveEvent

    def on_resize(event: Any) -> None:  # noqa: ANN401
        update_glass_frame()
        original_resize(event)

    def on_move(event: Any) -> None:  # noqa: ANN401
        update_glass_frame()
        original_move(event)

    widget.resizeEvent = on_resize  # type: ignore[method-assign]
    widget.moveEvent = on_move  # type: ignore[method-assign]

    global _next_effect_id  # noqa: PLW0603
    effect_id = _next_effect_id
    _next_effect_id += 1
    _effect_registry[effect_id] = (glass, content_view)

    widget._glass_view = glass  # type: ignore[attr-defined]  # noqa: SLF001
    widget._update_glass_frame = update_glass_frame  # type: ignore[attr-defined]  # noqa: SLF001

    return effect_id


def remove_glass_effect(effect_id: int) -> bool:
    """
    Remove a previously applied glass effect.

    Args:
        effect_id: The identifier returned by apply_glass_to_window or
            apply_glass_to_widget.

    Returns:
        True if the effect was successfully removed, False if the effect
        ID was not found.
    """
    if effect_id not in _effect_registry:
        return False

    glass_view, _ = _effect_registry.pop(effect_id)

    if IS_MACOS:
        try:
            glass_view.removeFromSuperview()  # ty: ignore
        except Exception:  # noqa: BLE001
            return False

    return True
