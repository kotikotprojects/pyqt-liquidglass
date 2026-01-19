API Reference
=============

This page documents the public API of pyqt-liquidglass.

pyqt_liquidglass
----------------

.. automodule:: pyqt_liquidglass
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __all__

Platform Constants
------------------

.. py:data:: pyqt_liquidglass.IS_MACOS
   :type: bool
   :noindex:

   ``True`` if running on macOS, ``False`` otherwise.

.. py:data:: pyqt_liquidglass.MACOS_VERSION
   :type: tuple[int, int, int] | None
   :noindex:

   macOS version as a tuple (major, minor, patch), or ``None`` on other platforms.

.. py:data:: pyqt_liquidglass.HAS_GLASS_EFFECT
   :type: bool
   :noindex:

   ``True`` if ``NSGlassEffectView`` is available (macOS 26+).

.. py:data:: pyqt_liquidglass.HAS_VISUAL_EFFECT
   :type: bool
   :noindex:

   ``True`` if ``NSVisualEffectView`` is available.
