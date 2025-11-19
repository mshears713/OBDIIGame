"""Asset management for Pygame GUI.

This module handles loading and caching of sprites, textures, fonts, and sounds.
It provides a centralized asset manager for the Pygame interface.
"""

import os
from pathlib import Path
from typing import Dict, Optional, Tuple, List
import pygame

from .config import TILE_SIZE, COLORS, TILE_COLORS


class AssetManager:
    """Manages loading and caching of game assets."""

    def __init__(self, tile_size: int = TILE_SIZE):
        """Initialize the asset manager.

        Args:
            tile_size: Size of tiles in pixels
        """
        self.tile_size = tile_size
        self.sprites: Dict[str, pygame.Surface] = {}
        self.animations: Dict[str, List[pygame.Surface]] = {}
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.fonts: Dict[str, pygame.font.Font] = {}

        # Asset directories
        self.assets_dir = Path(__file__).parent.parent.parent / "assets"
        self.sprites_dir = self.assets_dir / "sprites"
        self.sounds_dir = self.assets_dir / "sounds"
        self.music_dir = self.assets_dir / "music"

        # Ensure asset directories exist
        self._ensure_directories()

        # Initialize pygame font module
        pygame.font.init()

        # Load default font
        self.fonts['default'] = pygame.font.Font(None, 16)
        self.fonts['hud'] = pygame.font.Font(None, 20)
        self.fonts['title'] = pygame.font.Font(None, 32)
        self.fonts['float_text'] = pygame.font.Font(None, 18)

    def _ensure_directories(self):
        """Create asset directories if they don't exist."""
        self.assets_dir.mkdir(exist_ok=True)
        self.sprites_dir.mkdir(exist_ok=True)
        self.sounds_dir.mkdir(exist_ok=True)
        self.music_dir.mkdir(exist_ok=True)

    def get_tile_sprite(self, char: str, color: str = 'white') -> pygame.Surface:
        """Get or create a sprite for a tile character.

        Args:
            char: ASCII character representing the tile
            color: Color name for the sprite

        Returns:
            Pygame surface with the tile sprite
        """
        cache_key = f"{char}_{color}"

        # Return cached sprite if available
        if cache_key in self.sprites:
            return self.sprites[cache_key]

        # Try to load from file
        sprite_path = self.sprites_dir / f"{cache_key}.png"
        if sprite_path.exists():
            sprite = pygame.image.load(str(sprite_path))
            sprite = pygame.transform.scale(sprite, (self.tile_size, self.tile_size))
            self.sprites[cache_key] = sprite
            return sprite

        # Create fallback colored rectangle
        sprite = self._create_fallback_sprite(char, color)
        self.sprites[cache_key] = sprite
        return sprite

    def _create_fallback_sprite(self, char: str, color: str) -> pygame.Surface:
        """Create a fallback colored sprite with the character rendered.

        Args:
            char: ASCII character to render
            color: Color name for the sprite

        Returns:
            Pygame surface with fallback sprite
        """
        surface = pygame.Surface((self.tile_size, self.tile_size))

        # Get color from palette, defaulting to color from TILE_COLORS or white
        if char in TILE_COLORS:
            bg_color = TILE_COLORS[char]
        elif color in COLORS:
            bg_color = COLORS[color]
        else:
            bg_color = COLORS['white']

        # Fill with background color
        surface.fill(bg_color)

        # Render character on top
        font = self.fonts['default']
        text_surface = font.render(char, True, COLORS['black'])
        text_rect = text_surface.get_rect(center=(self.tile_size // 2, self.tile_size // 2))
        surface.blit(text_surface, text_rect)

        return surface

    def load_animation(self, name: str, frame_count: int) -> List[pygame.Surface]:
        """Load an animation sequence.

        Args:
            name: Name of the animation
            frame_count: Number of frames in the animation

        Returns:
            List of pygame surfaces representing animation frames
        """
        if name in self.animations:
            return self.animations[name]

        frames = []
        for i in range(frame_count):
            frame_path = self.sprites_dir / f"{name}_{i}.png"
            if frame_path.exists():
                frame = pygame.image.load(str(frame_path))
                frame = pygame.transform.scale(frame, (self.tile_size, self.tile_size))
                frames.append(frame)
            else:
                # Create placeholder frame
                frames.append(self._create_placeholder_frame(name, i, frame_count))

        if frames:
            self.animations[name] = frames

        return frames

    def _create_placeholder_frame(self, name: str, frame_index: int,
                                   total_frames: int) -> pygame.Surface:
        """Create a placeholder animation frame.

        Args:
            name: Animation name
            frame_index: Current frame index
            total_frames: Total number of frames

        Returns:
            Placeholder pygame surface
        """
        surface = pygame.Surface((self.tile_size, self.tile_size))

        # Pulsing effect based on frame index
        intensity = int(128 + 127 * (frame_index / max(1, total_frames - 1)))
        color = (intensity, intensity, 0)  # Yellow pulse

        surface.fill(color)
        return surface

    def load_sound(self, name: str) -> Optional[pygame.mixer.Sound]:
        """Load a sound effect.

        Args:
            name: Name of the sound file (without extension)

        Returns:
            Pygame Sound object, or None if not found
        """
        if name in self.sounds:
            return self.sounds[name]

        # Try different audio formats
        for ext in ['.ogg', '.wav', '.mp3']:
            sound_path = self.sounds_dir / f"{name}{ext}"
            if sound_path.exists():
                try:
                    sound = pygame.mixer.Sound(str(sound_path))
                    self.sounds[name] = sound
                    return sound
                except pygame.error as e:
                    print(f"Warning: Could not load sound {sound_path}: {e}")

        # Return None if sound not found
        return None

    def play_sound(self, name: str, volume: float = 1.0):
        """Play a sound effect.

        Args:
            name: Name of the sound
            volume: Volume level (0.0 to 1.0)
        """
        sound = self.load_sound(name)
        if sound:
            sound.set_volume(volume)
            sound.play()

    def load_music(self, name: str) -> bool:
        """Load and play background music.

        Args:
            name: Name of the music file (without extension)

        Returns:
            True if music loaded successfully, False otherwise
        """
        # Try different audio formats
        for ext in ['.ogg', '.mp3', '.wav']:
            music_path = self.music_dir / f"{name}{ext}"
            if music_path.exists():
                try:
                    pygame.mixer.music.load(str(music_path))
                    return True
                except pygame.error as e:
                    print(f"Warning: Could not load music {music_path}: {e}")

        return False

    def play_music(self, volume: float = 0.3, loops: int = -1):
        """Play the loaded background music.

        Args:
            volume: Volume level (0.0 to 1.0)
            loops: Number of times to loop (-1 = infinite)
        """
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops)

    def stop_music(self):
        """Stop the background music."""
        pygame.mixer.music.stop()

    def get_font(self, font_type: str = 'default') -> pygame.font.Font:
        """Get a font by type.

        Args:
            font_type: Type of font ('default', 'hud', 'title', 'float_text')

        Returns:
            Pygame font object
        """
        return self.fonts.get(font_type, self.fonts['default'])

    def create_text_surface(self, text: str, font_type: str = 'default',
                            color: Tuple[int, int, int] = (255, 255, 255)) -> pygame.Surface:
        """Create a text surface.

        Args:
            text: Text to render
            font_type: Type of font to use
            color: RGB color tuple

        Returns:
            Pygame surface with rendered text
        """
        font = self.get_font(font_type)
        return font.render(text, True, color)

    def cleanup(self):
        """Clean up loaded assets."""
        self.sprites.clear()
        self.animations.clear()
        self.sounds.clear()
        pygame.mixer.music.stop()
