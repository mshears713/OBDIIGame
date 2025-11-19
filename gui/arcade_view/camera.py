"""
Camera System

Implements smooth camera movement with easing, screen shake effects,
and viewport management for the Arcade GUI.
"""

import arcade
from typing import Tuple, Optional
import math


class SmoothCamera:
    """
    A camera that smoothly follows the player with configurable easing.

    Features:
    - Smooth interpolation to target position
    - Screen shake effects for impacts/explosions
    - Configurable dead zone (area where camera doesn't move)
    - Viewport clamping to map boundaries
    """

    def __init__(self, viewport_width: int, viewport_height: int,
                 camera_speed: float = 0.1):
        """
        Initialize the smooth camera.

        Args:
            viewport_width: Width of the viewport in pixels
            viewport_height: Height of the viewport in pixels
            camera_speed: Speed of camera interpolation (0.0-1.0)
        """
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        self.camera_speed = camera_speed

        # Camera position (center)
        self.position_x = 0.0
        self.position_y = 0.0

        # Target position (where we want to move)
        self.target_x = 0.0
        self.target_y = 0.0

        # Screen shake
        self.shake_intensity = 0.0
        self.shake_duration = 0.0
        self.shake_offset_x = 0.0
        self.shake_offset_y = 0.0

        # Arcade camera object
        self.camera = arcade.Camera(viewport_width, viewport_height)

    def set_target(self, x: float, y: float):
        """
        Set the camera target position.

        Args:
            x: Target x coordinate (world space)
            y: Target y coordinate (world space)
        """
        self.target_x = x
        self.target_y = y

    def update(self, delta_time: float):
        """
        Update camera position with smooth interpolation.

        Args:
            delta_time: Time elapsed since last update in seconds
        """
        # Smooth interpolation to target
        self.position_x += (self.target_x - self.position_x) * self.camera_speed
        self.position_y += (self.target_y - self.position_y) * self.camera_speed

        # Update screen shake
        if self.shake_duration > 0:
            self.shake_duration -= delta_time

            # Random shake offset
            import random
            angle = random.uniform(0, 2 * math.pi)
            self.shake_offset_x = math.cos(angle) * self.shake_intensity
            self.shake_offset_y = math.sin(angle) * self.shake_intensity

            # Decay shake intensity
            self.shake_intensity *= 0.95
        else:
            self.shake_offset_x = 0
            self.shake_offset_y = 0
            self.shake_intensity = 0

        # Calculate final camera position with shake
        final_x = self.position_x + self.shake_offset_x
        final_y = self.position_y + self.shake_offset_y

        # Update arcade camera (centered on position)
        self.camera.position = (
            final_x - self.viewport_width / 2,
            final_y - self.viewport_height / 2
        )

    def use(self):
        """Activate this camera for rendering."""
        self.camera.use()

    def add_shake(self, intensity: float, duration: float = 0.5):
        """
        Add screen shake effect.

        Args:
            intensity: Shake intensity in pixels
            duration: Duration of shake in seconds
        """
        self.shake_intensity = max(self.shake_intensity, intensity)
        self.shake_duration = max(self.shake_duration, duration)

    def screen_to_world(self, screen_x: float, screen_y: float) -> Tuple[float, float]:
        """
        Convert screen coordinates to world coordinates.

        Args:
            screen_x: X coordinate in screen space
            screen_y: Y coordinate in screen space

        Returns:
            Tuple of (world_x, world_y)
        """
        world_x = screen_x + self.camera.position[0]
        world_y = screen_y + self.camera.position[1]
        return world_x, world_y

    def world_to_screen(self, world_x: float, world_y: float) -> Tuple[float, float]:
        """
        Convert world coordinates to screen coordinates.

        Args:
            world_x: X coordinate in world space
            world_y: Y coordinate in world space

        Returns:
            Tuple of (screen_x, screen_y)
        """
        screen_x = world_x - self.camera.position[0]
        screen_y = world_y - self.camera.position[1]
        return screen_x, screen_y

    def get_viewport_bounds(self) -> Tuple[float, float, float, float]:
        """
        Get the current viewport boundaries in world space.

        Returns:
            Tuple of (left, right, bottom, top)
        """
        left = self.camera.position[0]
        bottom = self.camera.position[1]
        right = left + self.viewport_width
        top = bottom + self.viewport_height
        return left, right, bottom, top
