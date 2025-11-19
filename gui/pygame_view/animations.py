"""Animation system for Pygame GUI.

This module handles tile animations for special game elements like
CAN pathways, voltage traps, and spark effects.
"""

import pygame
from typing import Dict, List, Tuple
from .config import ANIMATION_FRAME_DURATION, COLORS


class AnimationManager:
    """Manages tile animations."""

    # Define which ASCII characters should be animated
    ANIMATED_TILES = {
        '~': 'can_pathway',      # CAN pathway - pulsing blue
        '*': 'spark',            # Spark/voltage trap - flickering yellow
        '^': 'voltage_trap',     # Voltage trap - electric arc
        '≈': 'water',           # Water/coolant - flowing
        '☼': 'power_source',    # Power source - glowing
    }

    def __init__(self, tile_size: int):
        """Initialize the animation manager.

        Args:
            tile_size: Size of tiles in pixels
        """
        self.tile_size = tile_size
        self.animation_frames: Dict[str, List[pygame.Surface]] = {}
        self.current_frame: Dict[str, int] = {}

        # Generate animation frames for each animated tile type
        self._generate_animations()

    def _generate_animations(self):
        """Generate animation frames for animated tiles."""
        # CAN pathway - pulsing blue glow
        self.animation_frames['can_pathway'] = self._create_pulse_animation(
            base_char='~',
            colors=[
                (30, 100, 180),
                (50, 130, 220),
                (70, 160, 255),
                (50, 130, 220),
            ],
            frame_count=4
        )
        self.current_frame['can_pathway'] = 0

        # Spark - flickering yellow/orange
        self.animation_frames['spark'] = self._create_flicker_animation(
            base_char='*',
            colors=[
                (255, 255, 100),
                (255, 200, 50),
                (255, 150, 0),
                (255, 100, 0),
            ],
            frame_count=4
        )
        self.current_frame['spark'] = 0

        # Voltage trap - electric arc effect
        self.animation_frames['voltage_trap'] = self._create_electric_animation(
            base_char='^',
            frame_count=4
        )
        self.current_frame['voltage_trap'] = 0

        # Water/coolant - flowing effect
        self.animation_frames['water'] = self._create_flow_animation(
            base_char='≈',
            colors=[
                (100, 150, 200),
                (120, 170, 220),
                (100, 150, 200),
                (80, 130, 180),
            ],
            frame_count=4
        )
        self.current_frame['water'] = 0

        # Power source - glowing
        self.animation_frames['power_source'] = self._create_glow_animation(
            base_char='☼',
            frame_count=4
        )
        self.current_frame['power_source'] = 0

    def _create_pulse_animation(self, base_char: str,
                                colors: List[Tuple[int, int, int]],
                                frame_count: int) -> List[pygame.Surface]:
        """Create a pulsing animation.

        Args:
            base_char: Character to render
            colors: List of colors for each frame
            frame_count: Number of frames

        Returns:
            List of animation frames
        """
        frames = []
        for i in range(frame_count):
            surface = pygame.Surface((self.tile_size, self.tile_size))
            color = colors[i % len(colors)]
            surface.fill(color)

            # Render character
            font = pygame.font.Font(None, self.tile_size)
            text = font.render(base_char, True, COLORS['black'])
            text_rect = text.get_rect(center=(self.tile_size // 2, self.tile_size // 2))
            surface.blit(text, text_rect)

            frames.append(surface)

        return frames

    def _create_flicker_animation(self, base_char: str,
                                  colors: List[Tuple[int, int, int]],
                                  frame_count: int) -> List[pygame.Surface]:
        """Create a flickering animation.

        Args:
            base_char: Character to render
            colors: List of colors for each frame
            frame_count: Number of frames

        Returns:
            List of animation frames
        """
        frames = []
        for i in range(frame_count):
            surface = pygame.Surface((self.tile_size, self.tile_size))
            color = colors[i % len(colors)]

            # Create glow effect
            for radius in range(self.tile_size // 2, 0, -2):
                intensity = int(255 * (radius / (self.tile_size // 2)))
                glow_color = tuple(min(255, c * intensity // 255) for c in color)
                pygame.draw.circle(
                    surface,
                    glow_color,
                    (self.tile_size // 2, self.tile_size // 2),
                    radius
                )

            # Render character
            font = pygame.font.Font(None, self.tile_size)
            text = font.render(base_char, True, COLORS['white'])
            text_rect = text.get_rect(center=(self.tile_size // 2, self.tile_size // 2))
            surface.blit(text, text_rect)

            frames.append(surface)

        return frames

    def _create_electric_animation(self, base_char: str,
                                   frame_count: int) -> List[pygame.Surface]:
        """Create an electric arc animation.

        Args:
            base_char: Character to render
            frame_count: Number of frames

        Returns:
            List of animation frames
        """
        import random

        frames = []
        base_color = (150, 150, 255)  # Light blue/purple

        for i in range(frame_count):
            surface = pygame.Surface((self.tile_size, self.tile_size))
            surface.fill(base_color)

            # Draw random lightning bolts
            for _ in range(3):
                start_x = random.randint(0, self.tile_size)
                start_y = 0
                end_x = random.randint(0, self.tile_size)
                end_y = self.tile_size

                # Create jagged line
                points = [(start_x, start_y)]
                for y in range(0, self.tile_size, self.tile_size // 4):
                    x = random.randint(max(0, start_x - 5), min(self.tile_size, start_x + 5))
                    points.append((x, y))
                points.append((end_x, end_y))

                # Draw lightning
                if len(points) > 1:
                    pygame.draw.lines(surface, COLORS['white'], False, points, 1)

            # Render character
            font = pygame.font.Font(None, self.tile_size)
            text = font.render(base_char, True, COLORS['black'])
            text_rect = text.get_rect(center=(self.tile_size // 2, self.tile_size // 2))
            surface.blit(text, text_rect)

            frames.append(surface)

        return frames

    def _create_flow_animation(self, base_char: str,
                               colors: List[Tuple[int, int, int]],
                               frame_count: int) -> List[pygame.Surface]:
        """Create a flowing animation.

        Args:
            base_char: Character to render
            colors: List of colors for each frame
            frame_count: Number of frames

        Returns:
            List of animation frames
        """
        frames = []
        for i in range(frame_count):
            surface = pygame.Surface((self.tile_size, self.tile_size))
            color = colors[i % len(colors)]

            # Create wave pattern
            for y in range(self.tile_size):
                wave_offset = int(2 * (i / frame_count + y / self.tile_size) * 255) % 50
                wave_color = tuple(min(255, c + wave_offset) for c in color)
                pygame.draw.line(
                    surface,
                    wave_color,
                    (0, y),
                    (self.tile_size, y)
                )

            # Render character
            font = pygame.font.Font(None, self.tile_size)
            text = font.render(base_char, True, COLORS['white'])
            text_rect = text.get_rect(center=(self.tile_size // 2, self.tile_size // 2))
            surface.blit(text, text_rect)

            frames.append(surface)

        return frames

    def _create_glow_animation(self, base_char: str,
                               frame_count: int) -> List[pygame.Surface]:
        """Create a glowing animation.

        Args:
            base_char: Character to render
            frame_count: Number of frames

        Returns:
            List of animation frames
        """
        frames = []
        base_color = (255, 255, 100)  # Yellow

        for i in range(frame_count):
            surface = pygame.Surface((self.tile_size, self.tile_size))

            # Pulsing glow intensity
            intensity = 0.5 + 0.5 * abs((i / frame_count) - 0.5) * 2

            # Draw glow
            for radius in range(self.tile_size // 2, 0, -1):
                alpha = int(intensity * 255 * (radius / (self.tile_size // 2)))
                glow_color = tuple(int(c * alpha / 255) for c in base_color)
                pygame.draw.circle(
                    surface,
                    glow_color,
                    (self.tile_size // 2, self.tile_size // 2),
                    radius
                )

            # Render character
            font = pygame.font.Font(None, self.tile_size)
            text = font.render(base_char, True, COLORS['black'])
            text_rect = text.get_rect(center=(self.tile_size // 2, self.tile_size // 2))
            surface.blit(text, text_rect)

            frames.append(surface)

        return frames

    def get_animation_frame(self, char: str) -> pygame.Surface:
        """Get the current animation frame for a character.

        Args:
            char: ASCII character

        Returns:
            Animation frame surface, or None if not animated
        """
        if char not in self.ANIMATED_TILES:
            return None

        animation_name = self.ANIMATED_TILES[char]
        if animation_name not in self.animation_frames:
            return None

        frames = self.animation_frames[animation_name]
        frame_index = self.current_frame.get(animation_name, 0)

        return frames[frame_index]

    def update(self, dt: float):
        """Update animation frames.

        Args:
            dt: Delta time in seconds
        """
        # Update all animation frame indices
        for anim_name in self.current_frame:
            if anim_name in self.animation_frames:
                frame_count = len(self.animation_frames[anim_name])
                self.current_frame[anim_name] = (self.current_frame[anim_name] + 1) % frame_count

    def is_animated(self, char: str) -> bool:
        """Check if a character has an animation.

        Args:
            char: ASCII character

        Returns:
            True if character is animated, False otherwise
        """
        return char in self.ANIMATED_TILES
