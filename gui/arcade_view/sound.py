"""
Sound System

Manages audio playback including sound effects and ambient loops.
"""

import arcade
from typing import Optional, Dict
from pathlib import Path
from .config import (
    SOUND_VOLUME_MASTER, SOUND_VOLUME_SFX, SOUND_VOLUME_AMBIENT,
    SOUND_VOLUME_MUSIC
)


class SoundManager:
    """
    Manages game audio including SFX and ambient sounds.

    Features:
    - Lazy loading of sounds
    - Volume control
    - Ambient sound loops
    - Positional audio (future)
    """

    def __init__(self, asset_dir: Optional[Path] = None):
        """
        Initialize the sound manager.

        Args:
            asset_dir: Path to assets directory
        """
        if asset_dir is None:
            self.asset_dir = Path(__file__).parent.parent.parent / 'assets'
        else:
            self.asset_dir = Path(asset_dir)

        # Sound cache
        self._sound_cache: Dict[str, arcade.Sound] = {}

        # Currently playing ambient sounds
        self._ambient_players: Dict[str, arcade.media.Player] = {}

        # Volume settings
        self.master_volume = SOUND_VOLUME_MASTER
        self.sfx_volume = SOUND_VOLUME_SFX
        self.ambient_volume = SOUND_VOLUME_AMBIENT
        self.music_volume = SOUND_VOLUME_MUSIC

    def load_sound(self, sound_name: str) -> Optional[arcade.Sound]:
        """
        Load a sound file.

        Args:
            sound_name: Name of the sound (without extension)

        Returns:
            Sound object or None if not found
        """
        # Check cache
        if sound_name in self._sound_cache:
            return self._sound_cache[sound_name]

        # Try to load
        sound_path = self.asset_dir / 'sounds' / f'{sound_name}.wav'

        if not sound_path.exists():
            # Try .ogg
            sound_path = self.asset_dir / 'sounds' / f'{sound_name}.ogg'

        if sound_path.exists():
            try:
                sound = arcade.load_sound(str(sound_path))
                self._sound_cache[sound_name] = sound
                return sound
            except Exception as e:
                print(f"Warning: Could not load sound '{sound_name}': {e}")

        return None

    def play_sound(self, sound_name: str, volume: Optional[float] = None):
        """
        Play a sound effect.

        Args:
            sound_name: Name of the sound to play
            volume: Optional volume override (0.0-1.0)
        """
        sound = self.load_sound(sound_name)
        if sound:
            if volume is None:
                volume = self.sfx_volume * self.master_volume
            else:
                volume = volume * self.master_volume

            arcade.play_sound(sound, volume)

    def play_ambient(self, sound_name: str, loop: bool = True):
        """
        Play an ambient sound.

        Args:
            sound_name: Name of the ambient sound
            loop: Whether to loop the sound
        """
        # Stop existing ambient sound with same name
        if sound_name in self._ambient_players:
            self.stop_ambient(sound_name)

        sound = self.load_sound(sound_name)
        if sound:
            volume = self.ambient_volume * self.master_volume
            player = arcade.play_sound(sound, volume, looping=loop)
            self._ambient_players[sound_name] = player

    def stop_ambient(self, sound_name: str):
        """
        Stop an ambient sound.

        Args:
            sound_name: Name of the ambient sound to stop
        """
        if sound_name in self._ambient_players:
            player = self._ambient_players[sound_name]
            # Note: arcade.Sound player doesn't have a stop method in all versions
            # This is a placeholder - actual implementation may vary
            del self._ambient_players[sound_name]

    def stop_all_ambient(self):
        """Stop all ambient sounds."""
        self._ambient_players.clear()

    def set_master_volume(self, volume: float):
        """
        Set master volume.

        Args:
            volume: Volume level (0.0-1.0)
        """
        self.master_volume = max(0.0, min(1.0, volume))

    def set_sfx_volume(self, volume: float):
        """
        Set sound effects volume.

        Args:
            volume: Volume level (0.0-1.0)
        """
        self.sfx_volume = max(0.0, min(1.0, volume))

    def set_ambient_volume(self, volume: float):
        """
        Set ambient sound volume.

        Args:
            volume: Volume level (0.0-1.0)
        """
        self.ambient_volume = max(0.0, min(1.0, volume))


# Predefined sound effects for the game
class GameSounds:
    """Constants for game sound effect names."""

    # Movement
    FOOTSTEP = "footstep"
    RELAY_CLICK = "relay_click"

    # Combat
    HIT = "hit"
    MISS = "miss"
    DEATH = "death"

    # Electrical/Voltage
    SPARK = "spark"
    VOLTAGE_ARC = "voltage_arc"
    ELECTRICAL_HUM = "electrical_hum"

    # Items
    PICKUP = "pickup"
    DROP = "drop"
    USE_ITEM = "use_item"

    # UI
    MENU_SELECT = "menu_select"
    ERROR = "error"
    SUCCESS = "success"

    # Ambient
    AMBIENT_ECU = "ambient_ecu"
    AMBIENT_ENGINE = "ambient_engine"
    AMBIENT_DATA = "ambient_data"

    # Subsystem specific
    IGNITION_FIRE = "ignition_fire"
    FUEL_FLOW = "fuel_flow"
    CAN_BUS_DATA = "can_bus_data"
    TRANSMISSION_GRIND = "transmission_grind"


# Global sound manager instance
_sound_manager: Optional[SoundManager] = None


def get_sound_manager() -> SoundManager:
    """
    Get the global sound manager instance.

    Returns:
        The SoundManager singleton
    """
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager()
    return _sound_manager
