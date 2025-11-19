"""
Particle Effects System

Implements visual effects using Arcade's particle engine including:
- Voltage arcs and electrical sparks
- Glitch bursts
- Smoke and fire effects
- Impact particles
"""

import arcade
from arcade import Emitter, EmitterIntervalWithTime, FadeParticle
from typing import Tuple, Optional
import math
import random


class ParticleEffectManager:
    """
    Manages particle effects for the game.

    Creates and updates particle emitters for various visual effects
    themed around automotive electronics.
    """

    def __init__(self):
        """Initialize the particle effect manager."""
        self.emitters: list[Emitter] = []
        self.asset_manager = None  # Will be set when needed

    def update(self, delta_time: float):
        """
        Update all active particle emitters.

        Args:
            delta_time: Time elapsed since last update
        """
        # Update emitters
        for emitter in self.emitters:
            emitter.update()

        # Remove dead emitters
        self.emitters = [e for e in self.emitters if not e.can_reap()]

    def draw(self):
        """Draw all active particle effects."""
        for emitter in self.emitters:
            emitter.draw()

    def create_voltage_arc(self, x: float, y: float):
        """
        Create a voltage arc/electrical spark effect.

        Args:
            x: X position in world coordinates
            y: Y position in world coordinates
        """
        from .config import PARTICLE_COUNT_MEDIUM

        # Electric blue particles
        emitter = Emitter(
            center_xy=(x, y),
            emit_controller=EmitterIntervalWithTime(0.01, 0.3),
            particle_factory=lambda emitter: FadeParticle(
                filename_or_texture=arcade.make_soft_circle_texture(8, (100, 200, 255)),
                change_xy=(
                    random.uniform(-50, 50),
                    random.uniform(-50, 50)
                ),
                lifetime=random.uniform(0.2, 0.5),
                scale=random.uniform(0.3, 0.8)
            )
        )

        self.emitters.append(emitter)

    def create_spark_discharge(self, x: float, y: float):
        """
        Create a spark discharge effect.

        Args:
            x: X position in world coordinates
            y: Y position in world coordinates
        """
        from .config import PARTICLE_COUNT_LOW

        # Yellow-white sparks
        emitter = Emitter(
            center_xy=(x, y),
            emit_controller=EmitterIntervalWithTime(0.01, 0.2),
            particle_factory=lambda emitter: FadeParticle(
                filename_or_texture=arcade.make_soft_circle_texture(6, (255, 255, 200)),
                change_xy=(
                    random.uniform(-100, 100),
                    random.uniform(-100, 100)
                ),
                lifetime=random.uniform(0.1, 0.3),
                scale=random.uniform(0.2, 0.6)
            )
        )

        self.emitters.append(emitter)

    def create_glitch_burst(self, x: float, y: float):
        """
        Create a digital glitch burst effect.

        Args:
            x: X position in world coordinates
            y: Y position in world coordinates
        """
        from .config import PARTICLE_COUNT_HIGH

        # Multicolored glitch particles
        colors = [
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Cyan
            (255, 255, 0),  # Yellow
            (255, 0, 0),    # Red
        ]

        emitter = Emitter(
            center_xy=(x, y),
            emit_controller=EmitterIntervalWithTime(0.005, 0.15),
            particle_factory=lambda emitter: FadeParticle(
                filename_or_texture=arcade.make_soft_square_texture(
                    random.randint(4, 12),
                    random.choice(colors)
                ),
                change_xy=(
                    random.uniform(-150, 150),
                    random.uniform(-150, 150)
                ),
                lifetime=random.uniform(0.1, 0.4),
                scale=random.uniform(0.3, 1.0)
            )
        )

        self.emitters.append(emitter)

    def create_smoke(self, x: float, y: float, duration: float = 1.0):
        """
        Create smoke effect (for burnout, damage, etc.).

        Args:
            x: X position in world coordinates
            y: Y position in world coordinates
            duration: How long the smoke emitter lasts
        """
        # Dark gray smoke rising upward
        emitter = Emitter(
            center_xy=(x, y),
            emit_controller=EmitterIntervalWithTime(0.05, duration),
            particle_factory=lambda emitter: FadeParticle(
                filename_or_texture=arcade.make_soft_circle_texture(20, (60, 60, 70)),
                change_xy=(
                    random.uniform(-10, 10),
                    random.uniform(20, 40)  # Rise upward
                ),
                lifetime=random.uniform(0.5, 1.5),
                scale=random.uniform(0.5, 1.5)
            )
        )

        self.emitters.append(emitter)

    def create_fire(self, x: float, y: float, duration: float = 1.0):
        """
        Create fire effect (for ignition, combustion, etc.).

        Args:
            x: X position in world coordinates
            y: Y position in world coordinates
            duration: How long the fire emitter lasts
        """
        # Orange-red fire particles
        emitter = Emitter(
            center_xy=(x, y),
            emit_controller=EmitterIntervalWithTime(0.03, duration),
            particle_factory=lambda emitter: FadeParticle(
                filename_or_texture=arcade.make_soft_circle_texture(
                    random.randint(10, 20),
                    (255, random.randint(100, 200), 0)
                ),
                change_xy=(
                    random.uniform(-20, 20),
                    random.uniform(30, 60)  # Rise upward
                ),
                lifetime=random.uniform(0.3, 0.8),
                scale=random.uniform(0.4, 1.2)
            )
        )

        self.emitters.append(emitter)

    def create_data_decode(self, x: float, y: float):
        """
        Create data decoding visual effect (matrix-style).

        Args:
            x: X position in world coordinates
            y: Y position in world coordinates
        """
        # Green digital particles
        emitter = Emitter(
            center_xy=(x, y),
            emit_controller=EmitterIntervalWithTime(0.02, 0.5),
            particle_factory=lambda emitter: FadeParticle(
                filename_or_texture=arcade.make_soft_circle_texture(6, (100, 255, 100)),
                change_xy=(
                    random.uniform(-30, 30),
                    random.uniform(-50, 10)  # Fall downward mostly
                ),
                lifetime=random.uniform(0.3, 0.7),
                scale=random.uniform(0.3, 0.7)
            )
        )

        self.emitters.append(emitter)

    def create_impact(self, x: float, y: float, color: Tuple[int, int, int] = (255, 255, 255)):
        """
        Create impact/hit effect.

        Args:
            x: X position in world coordinates
            y: Y position in world coordinates
            color: RGB color of the impact particles
        """
        from .config import PARTICLE_COUNT_MEDIUM

        emitter = Emitter(
            center_xy=(x, y),
            emit_controller=EmitterIntervalWithTime(0.01, 0.1),
            particle_factory=lambda emitter: FadeParticle(
                filename_or_texture=arcade.make_soft_circle_texture(8, color),
                change_xy=(
                    random.uniform(-80, 80),
                    random.uniform(-80, 80)
                ),
                lifetime=random.uniform(0.2, 0.4),
                scale=random.uniform(0.3, 0.8)
            )
        )

        self.emitters.append(emitter)

    def create_heal(self, x: float, y: float):
        """
        Create healing visual effect.

        Args:
            x: X position in world coordinates
            y: Y position in world coordinates
        """
        # Green healing particles rising up
        emitter = Emitter(
            center_xy=(x, y),
            emit_controller=EmitterIntervalWithTime(0.02, 0.5),
            particle_factory=lambda emitter: FadeParticle(
                filename_or_texture=arcade.make_soft_circle_texture(10, (100, 255, 150)),
                change_xy=(
                    random.uniform(-20, 20),
                    random.uniform(40, 80)  # Rise upward
                ),
                lifetime=random.uniform(0.4, 0.8),
                scale=random.uniform(0.4, 1.0)
            )
        )

        self.emitters.append(emitter)

    def create_directed_burst(self, x: float, y: float, direction: float,
                             spread: float = 45, color: Tuple[int, int, int] = (255, 200, 100)):
        """
        Create a directional particle burst.

        Args:
            x: X position in world coordinates
            y: Y position in world coordinates
            direction: Direction in degrees (0 = right, 90 = up)
            spread: Spread angle in degrees
            color: RGB color of particles
        """
        from .config import PARTICLE_COUNT_MEDIUM

        def particle_factory(emitter):
            # Convert direction to radians and add random spread
            angle_rad = math.radians(direction + random.uniform(-spread/2, spread/2))
            speed = random.uniform(50, 150)

            return FadeParticle(
                filename_or_texture=arcade.make_soft_circle_texture(8, color),
                change_xy=(
                    math.cos(angle_rad) * speed,
                    math.sin(angle_rad) * speed
                ),
                lifetime=random.uniform(0.3, 0.6),
                scale=random.uniform(0.4, 0.9)
            )

        emitter = Emitter(
            center_xy=(x, y),
            emit_controller=EmitterIntervalWithTime(0.01, 0.2),
            particle_factory=particle_factory
        )

        self.emitters.append(emitter)
