"""
Lighting System

Implements dynamic lighting using Arcade's light layer.
Creates atmospheric effects with light sources, shadows, and fog of war.
"""

import arcade
from typing import List, Tuple, Optional
from arcade.experimental.lights import Light, LightLayer
from src.entities.entity import Entity
from src.components import PositionComponent
from .config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TILE_WIDTH, TILE_HEIGHT,
    LIGHT_RADIUS_PLAYER, LIGHT_RADIUS_AMBIENT, AMBIENT_LIGHT_COLOR
)


class LightingSystem:
    """
    Manages dynamic lighting effects for the game.

    Features:
    - Player flashlight/glow
    - Environmental light sources
    - Ambient lighting
    - Fog of war
    - Pulsing/flickering lights
    """

    def __init__(self):
        """Initialize the lighting system."""
        # Create light layer
        self.light_layer = LightLayer(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Set ambient light (base darkness level)
        self.light_layer.set_background_color(AMBIENT_LIGHT_COLOR)

        # Light sources
        self.player_light: Optional[Light] = None
        self.static_lights: List[Light] = []
        self.dynamic_lights: List[Light] = []

        # Flicker state
        self.flicker_time = 0.0

    def setup(self, player_pos: Tuple[int, int]):
        """
        Set up initial lighting.

        Args:
            player_pos: Player position in grid coordinates
        """
        # Create player light
        world_x = player_pos[0] * TILE_WIDTH + TILE_WIDTH / 2
        world_y = player_pos[1] * TILE_HEIGHT + TILE_HEIGHT / 2

        self.player_light = Light(
            world_x,
            world_y,
            radius=LIGHT_RADIUS_PLAYER,
            color=(200, 220, 255),  # Cool white
            mode='soft'
        )
        self.light_layer.add(self.player_light)

    def update(self, delta_time: float, player_pos: Tuple[int, int], entities: List[Entity]):
        """
        Update lighting system.

        Args:
            delta_time: Time elapsed since last update
            player_pos: Player position in grid coordinates
            entities: List of all game entities
        """
        # Update player light position
        if self.player_light:
            world_x = player_pos[0] * TILE_WIDTH + TILE_WIDTH / 2
            world_y = player_pos[1] * TILE_HEIGHT + TILE_HEIGHT / 2
            self.player_light.position = (world_x, world_y)

        # Update flicker time
        self.flicker_time += delta_time

        # Update dynamic lights (flickering, pulsing, etc.)
        self._update_dynamic_lights(delta_time)

    def _update_dynamic_lights(self, delta_time: float):
        """
        Update dynamic light effects.

        Args:
            delta_time: Time elapsed
        """
        import math

        for light in self.dynamic_lights:
            # Pulsing effect
            if hasattr(light, 'pulse'):
                pulse_speed = 2.0  # Hz
                pulse_amount = 0.2  # 20% variation

                base_radius = getattr(light, 'base_radius', light.radius)
                light.radius = base_radius * (
                    1.0 + pulse_amount * math.sin(self.flicker_time * pulse_speed * 2 * math.pi)
                )

            # Flickering effect
            if hasattr(light, 'flicker'):
                import random
                if random.random() < 0.1:  # 10% chance per frame
                    light.radius *= random.uniform(0.8, 1.2)

    def add_static_light(self, x: int, y: int, radius: float = 100,
                        color: Tuple[int, int, int] = (255, 200, 100)):
        """
        Add a static light source.

        Args:
            x: Grid X coordinate
            y: Grid Y coordinate
            radius: Light radius in pixels
            color: RGB color tuple
        """
        world_x = x * TILE_WIDTH + TILE_WIDTH / 2
        world_y = y * TILE_HEIGHT + TILE_HEIGHT / 2

        light = Light(world_x, world_y, radius=radius, color=color, mode='soft')
        self.static_lights.append(light)
        self.light_layer.add(light)

    def add_pulsing_light(self, x: int, y: int, radius: float = 100,
                         color: Tuple[int, int, int] = (255, 100, 100)):
        """
        Add a pulsing light source.

        Args:
            x: Grid X coordinate
            y: Grid Y coordinate
            radius: Base light radius in pixels
            color: RGB color tuple
        """
        world_x = x * TILE_WIDTH + TILE_WIDTH / 2
        world_y = y * TILE_HEIGHT + TILE_HEIGHT / 2

        light = Light(world_x, world_y, radius=radius, color=color, mode='soft')
        light.pulse = True  # Custom attribute
        light.base_radius = radius
        self.dynamic_lights.append(light)
        self.light_layer.add(light)

    def add_flickering_light(self, x: int, y: int, radius: float = 80,
                           color: Tuple[int, int, int] = (255, 150, 50)):
        """
        Add a flickering light source (like fire or faulty wiring).

        Args:
            x: Grid X coordinate
            y: Grid Y coordinate
            radius: Base light radius in pixels
            color: RGB color tuple
        """
        world_x = x * TILE_WIDTH + TILE_WIDTH / 2
        world_y = y * TILE_HEIGHT + TILE_HEIGHT / 2

        light = Light(world_x, world_y, radius=radius, color=color, mode='soft')
        light.flicker = True  # Custom attribute
        self.dynamic_lights.append(light)
        self.light_layer.add(light)

    def add_temporary_light(self, x: int, y: int, duration: float = 1.0,
                          radius: float = 60, color: Tuple[int, int, int] = (255, 255, 200)):
        """
        Add a temporary light (for explosions, sparks, etc.).

        Args:
            x: Grid X coordinate
            y: Grid Y coordinate
            duration: How long the light lasts in seconds
            radius: Light radius in pixels
            color: RGB color tuple
        """
        world_x = x * TILE_WIDTH + TILE_WIDTH / 2
        world_y = y * TILE_HEIGHT + TILE_HEIGHT / 2

        light = Light(world_x, world_y, radius=radius, color=color, mode='soft')
        light.lifetime = duration  # Custom attribute
        light.age = 0.0

        self.dynamic_lights.append(light)
        self.light_layer.add(light)

    def remove_dead_lights(self):
        """Remove temporary lights that have expired."""
        dead_lights = []

        for light in self.dynamic_lights:
            if hasattr(light, 'lifetime'):
                light.age = getattr(light, 'age', 0) + 0.016  # Approximate frame time
                if light.age >= light.lifetime:
                    dead_lights.append(light)
                    self.light_layer.remove(light)

        for light in dead_lights:
            self.dynamic_lights.remove(light)

    def clear_dynamic_lights(self):
        """Clear all dynamic lights."""
        for light in self.dynamic_lights:
            self.light_layer.remove(light)
        self.dynamic_lights.clear()

    def draw(self):
        """Draw the lighting layer."""
        # The light layer should be drawn after all sprites
        # but before the HUD
        pass  # Drawing is handled by the light layer's use() method

    def use(self):
        """Activate the light layer for rendering with lights."""
        self.light_layer.use()
