"""Platform detection and guards for macOS-specific functionality."""

from __future__ import annotations

import platform
import sys
from functools import wraps
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

__all__ = [
    "HAS_GLASS_EFFECT",
    "HAS_VISUAL_EFFECT",
    "IS_MACOS",
    "MACOS_VERSION",
    "platform_guard",
    "require_macos",
]

IS_MACOS: bool = sys.platform == "darwin"

MACOS_VERSION: tuple[int, int, int] | None = None
if IS_MACOS:
    try:
        version_str = platform.mac_ver()[0]
        parts = version_str.split(".")
        MACOS_VERSION = (
            int(parts[0]) if len(parts) > 0 else 0,
            int(parts[1]) if len(parts) > 1 else 0,
            int(parts[2]) if len(parts) > 2 else 0,  # noqa: PLR2004
        )
    except (ValueError, IndexError):
        MACOS_VERSION = (0, 0, 0)

_MIN_VISUAL_EFFECT_VERSION = (10, 10, 0)
_MIN_GLASS_EFFECT_VERSION = (26, 0, 0)

HAS_VISUAL_EFFECT: bool = (
    IS_MACOS
    and MACOS_VERSION is not None
    and MACOS_VERSION >= _MIN_VISUAL_EFFECT_VERSION
)

HAS_GLASS_EFFECT: bool = (
    IS_MACOS
    and MACOS_VERSION is not None
    and MACOS_VERSION >= _MIN_GLASS_EFFECT_VERSION
)


class MacOSRequiredError(RuntimeError):
    """Raised when a macOS-only function is called on a non-macOS platform."""

    def __init__(self, func_name: str) -> None:
        super().__init__(f"{func_name} requires macOS")


def require_macos[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    """
    Decorator that raises an error if called on non-macOS platforms.

    Args:
        func: The function to wrap.

    Returns:
        A wrapped function that raises MacOSRequiredError on non-macOS.

    Raises:
        MacOSRequiredError: If called on a non-macOS platform.
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        if not IS_MACOS:
            raise MacOSRequiredError(func.__name__)
        return func(*args, **kwargs)

    return wrapper


def platform_guard[**P, R](func: Callable[P, R | None]) -> Callable[P, R | None]:
    """
    Decorator that makes a function a no-op on non-macOS platforms.

    The wrapped function will return None without executing on non-macOS
    platforms, allowing cross-platform code to call macOS-specific
    functions safely.

    Args:
        func: The function to wrap.

    Returns:
        A wrapped function that returns None on non-macOS platforms.
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
        if not IS_MACOS:
            return None
        return func(*args, **kwargs)

    return wrapper
