"""Configuration settings for Pygame GUI.

This module contains all configuration constants for the Pygame-based
graphical interface, including display settings, colors, and timing.
"""

from dataclasses import dataclass
from typing import Tuple

# Display settings
TILE_SIZE = 16  # Size of each tile in pixels
DEFAULT_WINDOW_WIDTH = 1280
DEFAULT_WINDOW_HEIGHT = 720
DEFAULT_FPS = 60

# Map viewport settings
MAP_VIEWPORT_WIDTH = 50  # Tiles visible horizontally
MAP_VIEWPORT_HEIGHT = 40  # Tiles visible vertically

# HUD settings
HUD_WIDTH = 300  # Width of the HUD panel in pixels
HUD_BACKGROUND_COLOR = (20, 20, 30)
HUD_TEXT_COLOR = (200, 200, 220)
HUD_BORDER_COLOR = (100, 100, 120)

# Bar colors (for HP, Fuel, etc.)
HP_BAR_COLOR = (200, 50, 50)
HP_BAR_BG_COLOR = (80, 20, 20)
FUEL_BAR_COLOR = (50, 200, 50)
FUEL_BAR_BG_COLOR = (20, 80, 20)
VOLTAGE_BAR_COLOR = (50, 150, 255)
VOLTAGE_BAR_BG_COLOR = (20, 60, 100)

# Warning thresholds
HP_WARNING_THRESHOLD = 0.3  # Show warning below 30%
FUEL_WARNING_THRESHOLD = 0.2  # Show warning below 20%

# Animation settings
ANIMATION_FRAME_DURATION = 0.3  # Seconds per animation frame
BLINK_DURATION = 0.5  # Seconds for warning blink cycle

# Floating text settings
FLOAT_TEXT_DURATION = 0.8  # Seconds
FLOAT_TEXT_RISE_SPEED = 30  # Pixels per second
FLOAT_TEXT_FADE_START = 0.3  # Start fading at 30% of duration

# Particle settings
PARTICLE_LIFETIME = 1.0  # Seconds
PARTICLE_SPEED_MIN = 20  # Pixels per second
PARTICLE_SPEED_MAX = 60  # Pixels per second
PARTICLE_FADE_START = 0.5  # Start fading at 50% of lifetime

# Minimap settings
MINIMAP_SCALE = 4  # Pixels per map tile
MINIMAP_MARGIN = 10  # Pixels from edge
MINIMAP_ALPHA = 180  # Transparency (0-255)

# Color palette (matching ASCII renderer colors)
COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (220, 50, 50),
    'green': (50, 220, 50),
    'blue': (50, 50, 220),
    'yellow': (220, 220, 50),
    'cyan': (50, 220, 220),
    'magenta': (220, 50, 220),
    'gray': (128, 128, 128),
    'dark_gray': (64, 64, 64),
    'light_gray': (192, 192, 192),
    'orange': (255, 165, 0),
    'purple': (160, 32, 240),
    'brown': (139, 69, 19),
}

# Tile-specific colors for fallback rendering
TILE_COLORS = {
    '.': COLORS['dark_gray'],     # Floor
    '#': COLORS['gray'],           # Wall
    '+': COLORS['brown'],          # Door
    '>': COLORS['cyan'],           # Stairs down
    '<': COLORS['cyan'],           # Stairs up
    '~': COLORS['blue'],           # CAN pathway
    '*': COLORS['yellow'],         # Spark/voltage trap
    '@': COLORS['white'],          # Player
    '!': COLORS['magenta'],        # Item
    'E': COLORS['red'],            # Enemy
}

# Sound settings
MUSIC_VOLUME = 0.3  # Background music volume (0.0 to 1.0)
SFX_VOLUME = 0.5    # Sound effects volume (0.0 to 1.0)


@dataclass
class PygameConfig:
    """Configuration for Pygame GUI."""

    tile_size: int = TILE_SIZE
    window_width: int = DEFAULT_WINDOW_WIDTH
    window_height: int = DEFAULT_WINDOW_HEIGHT
    fps: int = DEFAULT_FPS

    # Viewport settings
    viewport_width: int = MAP_VIEWPORT_WIDTH
    viewport_height: int = MAP_VIEWPORT_HEIGHT

    # HUD settings
    hud_width: int = HUD_WIDTH

    # Audio settings
    music_volume: float = MUSIC_VOLUME
    sfx_volume: float = SFX_VOLUME

    # Enable/disable features
    enable_animations: bool = True
    enable_particles: bool = True
    enable_sound: bool = True
    enable_minimap: bool = True
    enable_floating_text: bool = True

    def __post_init__(self):
        """Validate configuration values."""
        if self.tile_size < 8:
            raise ValueError("Tile size must be at least 8 pixels")
        if self.fps < 1 or self.fps > 144:
            raise ValueError("FPS must be between 1 and 144")
        if not (0.0 <= self.music_volume <= 1.0):
            raise ValueError("Music volume must be between 0.0 and 1.0")
        if not (0.0 <= self.sfx_volume <= 1.0):
            raise ValueError("SFX volume must be between 0.0 and 1.0")
