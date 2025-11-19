"""
Arcade Renderer

Coordinates all rendering operations including sprites, effects, lighting, and HUD.
Replaces the ASCII renderer while maintaining the same game state.
"""

import arcade
from typing import List, Optional
from src.entities.entity import Entity
from src.models import Map
from .sprites import SpriteManager
from .effects import ParticleEffectManager
from .camera import SmoothCamera
from .config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TILE_WIDTH, TILE_HEIGHT,
    COLOR_BACKGROUND
)


class ArcadeRenderer:
    """
    Main renderer for the Arcade GUI.

    Coordinates rendering of:
    - Terrain sprites
    - Entity sprites
    - Particle effects
    - Lighting
    - HUD elements
    """

    def __init__(self, game_map: Map):
        """
        Initialize the Arcade renderer.

        Args:
            game_map: The game Map to render
        """
        self.game_map = game_map

        # Initialize subsystems
        self.sprite_manager = SpriteManager()
        self.particle_manager = ParticleEffectManager()
        self.camera = SmoothCamera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Create terrain sprites from map
        self.sprite_manager.create_terrain_sprites(game_map)

        # Lighting (will be implemented in lighting step)
        self.light_layer = None

    def update(self, delta_time: float, entities: List[Entity], player_pos: tuple):
        """
        Update all rendering components.

        Args:
            delta_time: Time elapsed since last update
            entities: List of all game entities
            player_pos: Tuple of (x, y) player position in grid coordinates
        """
        # Update camera to follow player
        player_x = player_pos[0] * TILE_WIDTH + TILE_WIDTH / 2
        player_y = player_pos[1] * TILE_HEIGHT + TILE_HEIGHT / 2
        self.camera.set_target(player_x, player_y)
        self.camera.update(delta_time)

        # Update entity sprites
        self.sprite_manager.update_entity_sprites(entities)

        # Update animations
        self.sprite_manager.update_animations(delta_time)

        # Update particle effects
        self.particle_manager.update(delta_time)

    def draw(self):
        """Draw all game elements in correct order."""
        # Clear background
        arcade.set_background_color(COLOR_BACKGROUND)

        # Use world camera for game objects
        self.camera.use()

        # Draw sprites (terrain, items, actors)
        self.sprite_manager.draw_all()

        # Draw health bars
        self.sprite_manager.draw_health_bars()

        # Draw particle effects
        self.particle_manager.draw()

    def add_screen_shake(self, intensity: float, duration: float = 0.5):
        """
        Add screen shake effect.

        Args:
            intensity: Shake intensity in pixels
            duration: Duration in seconds
        """
        self.camera.add_shake(intensity, duration)

    def create_effect(self, effect_type: str, x: int, y: int, **kwargs):
        """
        Create a visual effect at the given grid position.

        Args:
            effect_type: Type of effect ('spark', 'glitch', 'impact', etc.)
            x: Grid X coordinate
            y: Grid Y coordinate
            **kwargs: Additional effect parameters
        """
        # Convert grid coordinates to world coordinates
        world_x = x * TILE_WIDTH + TILE_WIDTH / 2
        world_y = y * TILE_HEIGHT + TILE_HEIGHT / 2

        # Create the appropriate effect
        if effect_type == 'voltage':
            self.particle_manager.create_voltage_arc(world_x, world_y)
        elif effect_type == 'spark':
            self.particle_manager.create_spark_discharge(world_x, world_y)
        elif effect_type == 'glitch':
            self.particle_manager.create_glitch_burst(world_x, world_y)
        elif effect_type == 'smoke':
            self.particle_manager.create_smoke(world_x, world_y, kwargs.get('duration', 1.0))
        elif effect_type == 'fire':
            self.particle_manager.create_fire(world_x, world_y, kwargs.get('duration', 1.0))
        elif effect_type == 'impact':
            color = kwargs.get('color', (255, 255, 255))
            self.particle_manager.create_impact(world_x, world_y, color)
        elif effect_type == 'heal':
            self.particle_manager.create_heal(world_x, world_y)
        elif effect_type == 'data':
            self.particle_manager.create_data_decode(world_x, world_y)

    def get_camera(self) -> SmoothCamera:
        """
        Get the camera object.

        Returns:
            The SmoothCamera instance
        """
        return self.camera
