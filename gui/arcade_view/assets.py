"""
Asset Management System

Handles loading and caching of textures, sounds, and other game assets.
Creates placeholder textures when asset files are not available.
"""

import arcade
from typing import Dict, Optional, Tuple
from pathlib import Path
import os


class AssetManager:
    """
    Manages game assets including textures, sounds, and fonts.

    This class provides:
    - Lazy loading of assets
    - Caching to prevent duplicate loads
    - Procedural generation of placeholder textures
    - Easy asset lookup by tile type or entity name
    """

    def __init__(self, asset_dir: Optional[Path] = None):
        """
        Initialize the asset manager.

        Args:
            asset_dir: Path to the assets directory. If None, uses default location.
        """
        if asset_dir is None:
            # Default to project root/assets
            self.asset_dir = Path(__file__).parent.parent.parent / 'assets'
        else:
            self.asset_dir = Path(asset_dir)

        # Cache dictionaries
        self._texture_cache: Dict[str, arcade.Texture] = {}
        self._sound_cache: Dict[str, arcade.Sound] = {}

        # Create placeholder textures
        self._create_placeholder_textures()

    def _create_placeholder_textures(self):
        """
        Create procedural placeholder textures for all tile and entity types.

        These are used when asset files are not available. Each texture is
        a simple colored square with a character or symbol.
        """
        from .config import (
            SPRITE_PIXEL_SIZE, COLOR_FLOOR, COLOR_WALL, COLOR_PLAYER,
            COLOR_ENEMY, COLOR_ITEM
        )

        # Tile textures
        self._create_colored_texture('.', COLOR_FLOOR, name='floor')
        self._create_colored_texture('#', COLOR_WALL, name='wall')

        # Entity textures
        self._create_colored_texture('@', COLOR_PLAYER, name='player')
        self._create_colored_texture('E', COLOR_ENEMY, name='enemy')
        self._create_colored_texture('?', COLOR_ITEM, name='item')

        # Special tiles
        self._create_colored_texture('>', (100, 255, 100), name='stairs_down')
        self._create_colored_texture('<', (255, 255, 100), name='stairs_up')
        self._create_colored_texture('~', (100, 150, 255), name='water')
        self._create_colored_texture('^', (255, 200, 100), name='trap')

        # Create textures for various enemy types
        enemy_types = {
            'voltage_spike': (255, 255, 100),
            'corrupted_sensor': (200, 100, 255),
            'misfiring_injector': (255, 150, 50),
            'glitched_relay': (100, 255, 255),
        }

        for enemy_name, color in enemy_types.items():
            self._create_colored_texture('E', color, name=enemy_name)

    def _create_colored_texture(self, char: str, color: Tuple[int, int, int],
                                name: str, size: int = 32) -> arcade.Texture:
        """
        Create a simple colored square texture with a character overlay.

        Args:
            char: ASCII character to draw on the texture
            color: RGB color tuple
            name: Name for the texture (used for caching)
            size: Size of the texture in pixels

        Returns:
            The created texture
        """
        import arcade.color as arcade_color

        # Create a simple colored square for now
        # In a full implementation, we'd draw the character using PIL or arcade.draw_text
        texture = arcade.make_soft_square_texture(size, color, outer_alpha=255)
        texture.name = name

        self._texture_cache[name] = texture
        return texture

    def get_texture(self, tile_char: str) -> arcade.Texture:
        """
        Get texture for a given ASCII tile character.

        Args:
            tile_char: The ASCII character representing the tile

        Returns:
            Arcade texture for the tile
        """
        # Map ASCII characters to texture names
        tile_map = {
            '.': 'floor',
            '#': 'wall',
            '@': 'player',
            'E': 'enemy',
            'e': 'enemy',
            '?': 'item',
            '!': 'item',
            '>': 'stairs_down',
            '<': 'stairs_up',
            '~': 'water',
            '^': 'trap',
        }

        texture_name = tile_map.get(tile_char, 'floor')
        return self._texture_cache.get(texture_name, self._texture_cache['floor'])

    def get_entity_texture(self, entity_name: str, tags: list = None) -> arcade.Texture:
        """
        Get texture for a given entity.

        Args:
            entity_name: Name of the entity
            tags: List of entity tags (e.g., ['enemy', 'boss'])

        Returns:
            Arcade texture for the entity
        """
        # Try to find specific texture
        if entity_name.lower() in self._texture_cache:
            return self._texture_cache[entity_name.lower()]

        # Fall back to generic textures based on tags
        if tags:
            if 'player' in tags:
                return self._texture_cache['player']
            elif 'enemy' in tags:
                return self._texture_cache['enemy']
            elif 'item' in tags:
                return self._texture_cache['item']

        # Default fallback
        return self._texture_cache.get('floor')

    def load_sound(self, sound_name: str) -> Optional[arcade.Sound]:
        """
        Load a sound file.

        Args:
            sound_name: Name of the sound file (without extension)

        Returns:
            Arcade Sound object, or None if not found
        """
        # Check cache first
        if sound_name in self._sound_cache:
            return self._sound_cache[sound_name]

        # Try to load from assets directory
        sound_path = self.asset_dir / 'sounds' / f'{sound_name}.wav'

        if sound_path.exists():
            try:
                sound = arcade.load_sound(str(sound_path))
                self._sound_cache[sound_name] = sound
                return sound
            except Exception as e:
                print(f"Warning: Could not load sound {sound_name}: {e}")

        return None

    def create_particle_texture(self, color: Tuple[int, int, int],
                                size: int = 8) -> arcade.Texture:
        """
        Create a texture for particle effects.

        Args:
            color: RGB color tuple
            size: Size of the particle in pixels

        Returns:
            Arcade texture for the particle
        """
        return arcade.make_soft_circle_texture(size, color)


# Global asset manager instance
_asset_manager: Optional[AssetManager] = None


def get_asset_manager() -> AssetManager:
    """
    Get the global asset manager instance.

    Returns:
        The global AssetManager instance
    """
    global _asset_manager
    if _asset_manager is None:
        _asset_manager = AssetManager()
    return _asset_manager
