"""Type definitions for pyqt-liquidglass."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum

__all__ = ["BlendingMode", "GlassMaterial", "GlassOptions"]


class GlassMaterial(IntEnum):
    """
    Available materials for glass effects.

    These map to NSVisualEffectMaterial values for the fallback
    implementation on pre-macOS 26 systems.
    """

    TITLEBAR = 3
    SELECTION = 4
    MENU = 5
    POPOVER = 6
    SIDEBAR = 7
    HEADER_VIEW = 10
    SHEET = 11
    WINDOW_BACKGROUND = 12
    HUD = 13
    FULLSCREEN_UI = 15
    TOOLTIP = 17
    CONTENT_BACKGROUND = 18
    UNDER_WINDOW_BACKGROUND = 21
    UNDER_PAGE_BACKGROUND = 22


class BlendingMode(IntEnum):
    """
    Blending modes for visual effect views.

    These map to NSVisualEffectBlendingMode values.
    """

    BEHIND_WINDOW = 0
    WITHIN_WINDOW = 1


@dataclass(frozen=True, slots=True)
class GlassOptions:
    """
    Configuration options for glass effects.

    Attributes:
        corner_radius: Corner radius in points for rounded glass effects.
            Only applies to NSGlassEffectView on macOS 26+.
        material: The visual effect material to use. Only applies to
            NSVisualEffectView fallback on older macOS versions.
        blending_mode: How the effect blends with content. Only applies
            to NSVisualEffectView fallback.
        padding: Inset padding from widget edges in points (left, top, right, bottom).
    """

    corner_radius: float = 0.0
    material: GlassMaterial = GlassMaterial.UNDER_WINDOW_BACKGROUND
    blending_mode: BlendingMode = BlendingMode.BEHIND_WINDOW
    padding: tuple[float, float, float, float] = field(default=(0.0, 0.0, 0.0, 0.0))

    @classmethod
    def sidebar(
        cls, *, corner_radius: float = 10.0, padding: float = 9.0
    ) -> GlassOptions:
        """
        Create options optimized for sidebar glass effects.

        Args:
            corner_radius: Corner radius for rounded corners.
            padding: Uniform padding from all edges.

        Returns:
            GlassOptions configured for sidebar use.
        """
        return cls(
            corner_radius=corner_radius,
            material=GlassMaterial.SIDEBAR,
            blending_mode=BlendingMode.BEHIND_WINDOW,
            padding=(padding, padding, padding, padding),
        )

    @classmethod
    def window(cls) -> GlassOptions:
        """
        Create options for full window glass effects.

        Returns:
            GlassOptions configured for window-wide glass.
        """
        return cls(
            corner_radius=0.0,
            material=GlassMaterial.UNDER_WINDOW_BACKGROUND,
            blending_mode=BlendingMode.BEHIND_WINDOW,
            padding=(0.0, 0.0, 0.0, 0.0),
        )
