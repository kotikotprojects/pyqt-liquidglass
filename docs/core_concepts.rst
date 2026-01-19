Core Concepts
=============

This page explains how pyqt-liquidglass works under the hood.

How Glass Effects Work
----------------------

Native Views
~~~~~~~~~~~~

macOS provides two classes for blur/glass effects:

- **NSGlassEffectView**: New in macOS 26 (Tahoe), provides the Liquid Glass effect
- **NSVisualEffectView**: Available since macOS 10.10, provides vibrancy effects

pyqt-liquidglass automatically uses ``NSGlassEffectView`` when available and falls back to ``NSVisualEffectView`` on older systems.

View Hierarchy
~~~~~~~~~~~~~~

Qt widgets map to native ``NSView`` objects. When you apply a glass effect, the library:

1. Gets the native ``NSView`` for your Qt widget
2. Creates a glass effect view (``NSGlassEffectView`` or ``NSVisualEffectView``)
3. Inserts it behind your widget's view in the z-order
4. Configures autoresizing so it tracks widget size changes

The glass view renders the blur effect, and your Qt content draws on top.

Window vs Widget Glass
----------------------

Window Glass
~~~~~~~~~~~~

``apply_glass_to_window()`` fills the entire window content area with glass:

.. code-block:: python

   glass.apply_glass_to_window(window)

This is ideal for:

- Full-window blur backgrounds
- Floating panels
- Modal dialogs

The function configures the window for transparent titlebar and full-size content view automatically.

Widget Glass
~~~~~~~~~~~~

``apply_glass_to_widget()`` applies glass to a specific widget region:

.. code-block:: python

   glass.apply_glass_to_widget(sidebar, options=glass.GlassOptions.sidebar())

This is ideal for:

- Sidebars (like macOS System Settings)
- Navigation panels
- Toolbars

The glass view tracks the widget's position and size, updating automatically on resize or move.

GlassOptions Configuration
--------------------------

The ``GlassOptions`` dataclass controls glass effect appearance:

.. code-block:: python

   from pyqt_liquidglass import GlassOptions

   options = GlassOptions(
       corner_radius=16.0,      # Rounded corners (NSGlassEffectView only)
       material=GlassMaterial.SIDEBAR,  # Material type
       blending_mode=BlendingMode.BEHIND_WINDOW,  # Blending mode
       padding=(10, 10, 10, 10),  # Left, top, right, bottom
   )

Attributes
~~~~~~~~~~

**corner_radius** (float)
   Corner radius in points. Only applies to ``NSGlassEffectView`` on macOS 26+. Default: 0.0

**material** (GlassMaterial)
   The visual effect material. Only applies to ``NSVisualEffectView`` fallback. Options include:

   - ``TITLEBAR``, ``SIDEBAR``, ``MENU``, ``POPOVER``
   - ``SHEET``, ``WINDOW_BACKGROUND``, ``HUD``, ``TOOLTIP``
   - ``CONTENT_BACKGROUND``, ``UNDER_WINDOW_BACKGROUND``

**blending_mode** (BlendingMode)
   How the effect blends with content:

   - ``BEHIND_WINDOW``: Blurs content behind the window
   - ``WITHIN_WINDOW``: Blurs content within the window

**padding** (tuple)
   Inset from widget edges in points: (left, top, right, bottom). Default: (0, 0, 0, 0)

Preset Methods
~~~~~~~~~~~~~~

For common use cases:

.. code-block:: python

   # Full window glass (no corner radius, no padding)
   options = GlassOptions.window()

   # Sidebar glass (10pt radius, 9pt padding)
   options = GlassOptions.sidebar()

   # Custom sidebar
   options = GlassOptions.sidebar(corner_radius=16.0, padding=12.0)

Coordinate Systems
------------------

Qt and Cocoa use different coordinate systems:

- **Qt**: Origin at top-left, Y increases downward
- **Cocoa**: Origin at bottom-left, Y increases upward

pyqt-liquidglass handles this conversion internally. When specifying ``y_offset`` for traffic lights, positive values move the buttons down from center.

Traffic Lights
--------------

The traffic lights are the close, minimize, and zoom buttons in the window titlebar.

Positioning
~~~~~~~~~~~

``setup_traffic_lights_inset()`` repositions the buttons using ``NSLayoutConstraint``:

.. code-block:: python

   glass.setup_traffic_lights_inset(window, x_offset=20, y_offset=12)

- **x_offset**: Distance from the left edge in points
- **y_offset**: Vertical offset from center (positive = down)

This method survives window resizes because it uses Auto Layout constraints rather than absolute positioning.

Visibility
~~~~~~~~~~

Hide the buttons while keeping window functionality:

.. code-block:: python

   glass.hide_traffic_lights(window)
   glass.show_traffic_lights(window)

The window remains closable, minimizable, and zoomable via keyboard shortcuts and menu commands.

Platform Detection
------------------

The library provides constants for platform detection:

.. code-block:: python

   from pyqt_liquidglass import (
       IS_MACOS,           # True if running on macOS
       MACOS_VERSION,      # Tuple like (15, 1, 0) or None
       HAS_GLASS_EFFECT,   # True if NSGlassEffectView is available
       HAS_VISUAL_EFFECT,  # True if NSVisualEffectView is available
   )

All glass functions are safe to call on non-macOS platforms. They return ``None`` or ``False`` without side effects.

Effect Lifecycle
----------------

Effect IDs
~~~~~~~~~~

``apply_glass_to_window()`` and ``apply_glass_to_widget()`` return an effect ID:

.. code-block:: python

   effect_id = glass.apply_glass_to_window(window)

Use this ID to remove the effect later:

.. code-block:: python

   glass.remove_glass_effect(effect_id)

Cleanup
~~~~~~~

When a window is closed, Qt destroys the widget hierarchy. The glass effect views are removed automatically as part of the native view cleanup. You don't need to manually remove effects before closing windows.
