"""
Configuration constants for the Arcade GUI

This module contains all configuration values for the Arcade-based interface,
including screen dimensions, tile sizes, colors, and performance settings.
"""

# Window Configuration
SCREEN_TITLE = "OBD-II Chronicles"
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FULLSCREEN = False

# Tile Configuration
TILE_WIDTH = 32  # pixels per tile
TILE_HEIGHT = 32  # pixels per tile
TILE_SCALING = 1.0  # Scale factor for tiles

# Sprite Configuration
SPRITE_SCALING = 1.0
SPRITE_PIXEL_SIZE = 32

# Camera Configuration
CAMERA_SPEED = 0.1  # Smoothing factor for camera movement (0.0-1.0)
VIEWPORT_MARGIN = 200  # Pixels from edge before camera moves

# Performance
TARGET_FPS = 60
SPRITE_LISTS_ENABLE_SPATIAL_HASH = True  # Improves collision detection performance

# Colors (RGB tuples)
COLOR_BACKGROUND = (10, 10, 15)  # Dark blue-black
COLOR_FOG_OF_WAR = (0, 0, 0, 200)  # Semi-transparent black
COLOR_FLOOR = (40, 40, 50)
COLOR_WALL = (80, 80, 100)
COLOR_PLAYER = (100, 200, 255)  # Cyan-blue
COLOR_ENEMY = (255, 100, 100)  # Red
COLOR_ITEM = (255, 220, 100)  # Gold
COLOR_HEALTH_BAR_GOOD = (100, 255, 100)  # Green
COLOR_HEALTH_BAR_WARNING = (255, 200, 100)  # Orange
COLOR_HEALTH_BAR_CRITICAL = (255, 100, 100)  # Red

# HUD Configuration
HUD_MARGIN = 10
HUD_BAR_WIDTH = 200
HUD_BAR_HEIGHT = 20
HUD_FONT_SIZE = 14
HUD_MESSAGE_COUNT = 5  # Number of recent messages to display

# Particle Effects
PARTICLE_COUNT_LOW = 5
PARTICLE_COUNT_MEDIUM = 15
PARTICLE_COUNT_HIGH = 30
PARTICLE_FADE_RATE = 5  # Alpha decrease per frame

# Lighting
LIGHT_RADIUS_PLAYER = 200  # Pixels
LIGHT_RADIUS_AMBIENT = 100  # Pixels
AMBIENT_LIGHT_COLOR = (40, 60, 80)  # Dim blue

# Animation
ANIMATION_SPEED_SLOW = 0.1  # Seconds per frame
ANIMATION_SPEED_NORMAL = 0.15
ANIMATION_SPEED_FAST = 0.2

# Sound
SOUND_VOLUME_MASTER = 0.5
SOUND_VOLUME_SFX = 0.7
SOUND_VOLUME_AMBIENT = 0.3
SOUND_VOLUME_MUSIC = 0.4

# Subsystem Theme Colors (for different dungeon areas)
SUBSYSTEM_COLORS = {
    'fuel_injection': (255, 150, 50),  # Orange
    'ignition': (255, 100, 100),  # Red
    'can_bus': (100, 255, 255),  # Cyan
    'transmission': (200, 100, 255),  # Purple
    'oxygen': (150, 255, 150),  # Green
    'ecu': (255, 255, 100),  # Yellow
}

# Debug
DEBUG_MODE = False
SHOW_FPS = True
SHOW_SPRITE_HITBOXES = False
