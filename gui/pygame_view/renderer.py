"""Pygame renderer for OBD-II Chronicles.

This module provides graphical rendering for the game, replacing the ASCII
renderer while maintaining all game logic intact.
"""

import pygame
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
from src.models import Map
from src.entities.entity import Entity
from src.components.position import PositionComponent
from src.components.render import RenderComponent
from src.components.health import HealthComponent
from src.components.name import NameComponent

from .config import (
    TILE_SIZE, COLORS, HUD_WIDTH, HUD_BACKGROUND_COLOR, HUD_TEXT_COLOR,
    HUD_BORDER_COLOR, HP_BAR_COLOR, HP_BAR_BG_COLOR, FUEL_BAR_COLOR,
    FUEL_BAR_BG_COLOR, VOLTAGE_BAR_COLOR, VOLTAGE_BAR_BG_COLOR,
    HP_WARNING_THRESHOLD, ANIMATION_FRAME_DURATION, BLINK_DURATION,
    MINIMAP_SCALE, MINIMAP_MARGIN, MINIMAP_ALPHA
)
from .assets import AssetManager
from .animations import AnimationManager


@dataclass
class FloatingText:
    """Represents floating combat text."""
    text: str
    x: int
    y: int
    color: Tuple[int, int, int]
    lifetime: float
    max_lifetime: float


@dataclass
class Particle:
    """Represents a visual particle effect."""
    x: float
    y: float
    vx: float  # Velocity X
    vy: float  # Velocity Y
    color: Tuple[int, int, int]
    size: int
    lifetime: float
    max_lifetime: float


class PygameRenderer:
    """Renders the game world using Pygame."""

    def __init__(self, screen: pygame.Surface, asset_manager: AssetManager,
                 config):
        """Initialize the Pygame renderer.

        Args:
            screen: Pygame screen surface to render to
            asset_manager: Asset manager for loading sprites
            config: Pygame configuration object
        """
        self.screen = screen
        self.assets = asset_manager
        self.config = config

        # Calculate viewport size in tiles
        screen_width, screen_height = screen.get_size()
        self.viewport_width = (screen_width - config.hud_width) // config.tile_size
        self.viewport_height = screen_height // config.tile_size

        # Animation state
        self.animation_timer = 0.0
        self.animation_frame = 0
        self.blink_timer = 0.0

        # Animation manager
        self.animation_manager = AnimationManager(config.tile_size)

        # Floating text and particles
        self.floating_texts: List[FloatingText] = []
        self.particles: List[Particle] = []

        # Camera position (in tiles)
        self.camera_x = 0
        self.camera_y = 0

        # Explored tiles (for fog of war)
        self.explored_tiles: set[Tuple[int, int]] = set()

    def render(self, game_map: Map, entities: List[Entity], player: Entity,
               message_log: List[str], dt: float = 0.016):
        """Render the complete game state.

        Args:
            game_map: The game map to render
            entities: List of all entities
            player: The player entity
            message_log: Recent game messages
            dt: Delta time since last frame (seconds)
        """
        # Update timers
        self._update_timers(dt)

        # Clear screen
        self.screen.fill(COLORS['black'])

        # Update camera to center on player
        self._update_camera(player, game_map)

        # Calculate render area
        map_area = pygame.Rect(0, 0,
                               self.viewport_width * self.config.tile_size,
                               self.viewport_height * self.config.tile_size)

        # Render map tiles
        self._render_map(game_map, map_area)

        # Render entities
        self._render_entities(entities, map_area)

        # Render particles
        if self.config.enable_particles:
            self._render_particles(map_area, dt)

        # Render floating text
        if self.config.enable_floating_text:
            self._render_floating_text(map_area, dt)

        # Render HUD
        self._render_hud(player, message_log)

        # Render minimap
        if self.config.enable_minimap:
            self._render_minimap(game_map, player)

    def _update_timers(self, dt: float):
        """Update animation and effect timers.

        Args:
            dt: Delta time in seconds
        """
        self.animation_timer += dt
        if self.animation_timer >= ANIMATION_FRAME_DURATION:
            self.animation_timer = 0.0
            self.animation_frame = (self.animation_frame + 1) % 4
            # Update tile animations
            if self.config.enable_animations:
                self.animation_manager.update(dt)

        self.blink_timer += dt
        if self.blink_timer >= BLINK_DURATION:
            self.blink_timer = 0.0

    def _update_camera(self, player: Entity, game_map: Map):
        """Update camera position to follow player.

        Args:
            player: The player entity
            game_map: The game map
        """
        pos = player.get_component(PositionComponent)
        if not pos:
            return

        # Center camera on player
        self.camera_x = pos.x - self.viewport_width // 2
        self.camera_y = pos.y - self.viewport_height // 2

        # Clamp camera to map boundaries
        self.camera_x = max(0, min(self.camera_x,
                                   game_map.width - self.viewport_width))
        self.camera_y = max(0, min(self.camera_y,
                                   game_map.height - self.viewport_height))

    def _render_map(self, game_map: Map, area: pygame.Rect):
        """Render the map tiles.

        Args:
            game_map: The game map
            area: Rectangle defining the render area
        """
        for y in range(self.viewport_height):
            for x in range(self.viewport_width):
                map_x = x + self.camera_x
                map_y = y + self.camera_y

                # Check bounds
                if not game_map.is_in_bounds(map_x, map_y):
                    continue

                # Get tile
                tile = game_map.get_tile(map_x, map_y)
                if not tile:
                    continue

                # Mark as explored
                self.explored_tiles.add((map_x, map_y))

                # Get sprite for tile - check for animation first
                sprite = None
                if (self.config.enable_animations and
                    self.animation_manager.is_animated(tile.ascii_char)):
                    sprite = self.animation_manager.get_animation_frame(tile.ascii_char)

                if not sprite:
                    sprite = self.assets.get_tile_sprite(tile.ascii_char)

                # Calculate screen position
                screen_x = x * self.config.tile_size
                screen_y = y * self.config.tile_size

                # Blit sprite
                self.screen.blit(sprite, (screen_x, screen_y))

    def _render_entities(self, entities: List[Entity], area: pygame.Rect):
        """Render all entities.

        Args:
            entities: List of entities to render
            area: Rectangle defining the render area
        """
        # Sort entities by render order
        sorted_entities = sorted(
            entities,
            key=lambda e: e.get_component(RenderComponent).render_order
            if e.get_component(RenderComponent) else 0
        )

        for entity in sorted_entities:
            pos = entity.get_component(PositionComponent)
            render = entity.get_component(RenderComponent)

            if not pos or not render:
                continue

            # Check if entity is in viewport
            if not self._is_in_viewport(pos.x, pos.y):
                continue

            # Calculate screen position
            screen_x = (pos.x - self.camera_x) * self.config.tile_size
            screen_y = (pos.y - self.camera_y) * self.config.tile_size

            # Get sprite
            sprite = self.assets.get_tile_sprite(render.char, render.color)

            # Blit sprite
            self.screen.blit(sprite, (screen_x, screen_y))

    def _is_in_viewport(self, x: int, y: int) -> bool:
        """Check if a position is in the current viewport.

        Args:
            x: X position in map coordinates
            y: Y position in map coordinates

        Returns:
            True if position is visible, False otherwise
        """
        return (self.camera_x <= x < self.camera_x + self.viewport_width and
                self.camera_y <= y < self.camera_y + self.viewport_height)

    def _render_hud(self, player: Entity, message_log: List[str]):
        """Render the HUD panel.

        Args:
            player: The player entity
            message_log: Recent game messages
        """
        # Calculate HUD area
        screen_width, screen_height = self.screen.get_size()
        hud_x = screen_width - self.config.hud_width
        hud_rect = pygame.Rect(hud_x, 0, self.config.hud_width, screen_height)

        # Draw HUD background
        pygame.draw.rect(self.screen, HUD_BACKGROUND_COLOR, hud_rect)
        pygame.draw.line(self.screen, HUD_BORDER_COLOR,
                        (hud_x, 0), (hud_x, screen_height), 2)

        # Get player components
        health = player.get_component(HealthComponent)
        name = player.get_component(NameComponent)

        # Draw player name
        y_offset = 20
        if name:
            name_surface = self.assets.create_text_surface(
                name.name, 'title', HUD_TEXT_COLOR
            )
            self.screen.blit(name_surface, (hud_x + 20, y_offset))
            y_offset += 50

        # Draw HP bar
        if health:
            y_offset = self._draw_stat_bar(
                hud_x + 20, y_offset, self.config.hud_width - 40,
                "HP", health.current_hp, health.max_hp,
                HP_BAR_COLOR, HP_BAR_BG_COLOR,
                HP_WARNING_THRESHOLD
            )
            y_offset += 20

        # Draw message log
        y_offset += 20
        log_title = self.assets.create_text_surface(
            "Messages:", 'hud', HUD_TEXT_COLOR
        )
        self.screen.blit(log_title, (hud_x + 20, y_offset))
        y_offset += 30

        # Display last 10 messages
        for message in message_log[-10:]:
            # Wrap long messages
            words = message.split()
            line = ""
            for word in words:
                test_line = line + word + " "
                test_surface = self.assets.create_text_surface(
                    test_line, 'default', HUD_TEXT_COLOR
                )
                if test_surface.get_width() > self.config.hud_width - 40:
                    if line:
                        msg_surface = self.assets.create_text_surface(
                            line, 'default', HUD_TEXT_COLOR
                        )
                        self.screen.blit(msg_surface, (hud_x + 20, y_offset))
                        y_offset += 18
                    line = word + " "
                else:
                    line = test_line

            if line:
                msg_surface = self.assets.create_text_surface(
                    line, 'default', HUD_TEXT_COLOR
                )
                self.screen.blit(msg_surface, (hud_x + 20, y_offset))
                y_offset += 18

    def _draw_stat_bar(self, x: int, y: int, width: int, label: str,
                       current: int, maximum: int,
                       bar_color: Tuple[int, int, int],
                       bg_color: Tuple[int, int, int],
                       warning_threshold: float = 0.0) -> int:
        """Draw a stat bar (HP, fuel, etc.).

        Args:
            x: X position
            y: Y position
            width: Width of the bar
            label: Label text
            current: Current value
            maximum: Maximum value
            bar_color: Color for the filled portion
            bg_color: Color for the background
            warning_threshold: Show warning below this percentage

        Returns:
            Y position after the bar
        """
        # Draw label
        label_surface = self.assets.create_text_surface(
            f"{label}: {current}/{maximum}", 'default', HUD_TEXT_COLOR
        )
        self.screen.blit(label_surface, (x, y))
        y += 20

        # Draw background bar
        bar_height = 20
        bg_rect = pygame.Rect(x, y, width, bar_height)
        pygame.draw.rect(self.screen, bg_color, bg_rect)

        # Draw filled bar
        fill_width = int(width * (current / max(1, maximum)))
        fill_rect = pygame.Rect(x, y, fill_width, bar_height)
        pygame.draw.rect(self.screen, bar_color, fill_rect)

        # Draw border
        pygame.draw.rect(self.screen, HUD_BORDER_COLOR, bg_rect, 1)

        # Show warning blink if below threshold
        if warning_threshold > 0 and current / max(1, maximum) < warning_threshold:
            if self.blink_timer < BLINK_DURATION / 2:
                warning_surface = self.assets.create_text_surface(
                    "!", 'hud', COLORS['red']
                )
                self.screen.blit(warning_surface, (x + width + 10, y))

        return y + bar_height

    def _render_minimap(self, game_map: Map, player: Entity):
        """Render a minimap overlay.

        Args:
            game_map: The game map
            player: The player entity
        """
        # Create minimap surface
        minimap_width = game_map.width * MINIMAP_SCALE
        minimap_height = game_map.height * MINIMAP_SCALE
        minimap = pygame.Surface((minimap_width, minimap_height))
        minimap.set_alpha(MINIMAP_ALPHA)
        minimap.fill(COLORS['black'])

        # Draw explored tiles
        for (map_x, map_y) in self.explored_tiles:
            tile = game_map.get_tile(map_x, map_y)
            if not tile:
                continue

            # Determine color based on tile type
            if tile.walkable:
                color = COLORS['dark_gray']
            else:
                color = COLORS['gray']

            # Draw tile
            tile_rect = pygame.Rect(
                map_x * MINIMAP_SCALE,
                map_y * MINIMAP_SCALE,
                MINIMAP_SCALE,
                MINIMAP_SCALE
            )
            pygame.draw.rect(minimap, color, tile_rect)

        # Draw player position
        pos = player.get_component(PositionComponent)
        if pos:
            player_rect = pygame.Rect(
                pos.x * MINIMAP_SCALE,
                pos.y * MINIMAP_SCALE,
                MINIMAP_SCALE,
                MINIMAP_SCALE
            )
            pygame.draw.rect(minimap, COLORS['white'], player_rect)

        # Blit minimap to screen
        screen_width, screen_height = self.screen.get_size()
        minimap_x = MINIMAP_MARGIN
        minimap_y = screen_height - minimap_height - MINIMAP_MARGIN
        self.screen.blit(minimap, (minimap_x, minimap_y))

    def _render_floating_text(self, area: pygame.Rect, dt: float):
        """Render floating combat text.

        Args:
            area: Rectangle defining the render area
            dt: Delta time
        """
        # Update and render floating texts
        texts_to_remove = []

        for text in self.floating_texts:
            text.lifetime -= dt

            if text.lifetime <= 0:
                texts_to_remove.append(text)
                continue

            # Calculate alpha based on lifetime
            alpha = int(255 * (text.lifetime / text.max_lifetime))
            alpha = max(0, min(255, alpha))

            # Render text
            text_surface = self.assets.create_text_surface(
                text.text, 'float_text', text.color
            )
            text_surface.set_alpha(alpha)

            # Calculate position (rise over time)
            y_offset = int((text.max_lifetime - text.lifetime) * 30)
            self.screen.blit(text_surface, (text.x, text.y - y_offset))

        # Remove expired texts
        for text in texts_to_remove:
            self.floating_texts.remove(text)

    def _render_particles(self, area: pygame.Rect, dt: float):
        """Render particle effects.

        Args:
            area: Rectangle defining the render area
            dt: Delta time
        """
        particles_to_remove = []

        for particle in self.particles:
            particle.lifetime -= dt

            if particle.lifetime <= 0:
                particles_to_remove.append(particle)
                continue

            # Update position
            particle.x += particle.vx * dt
            particle.y += particle.vy * dt

            # Calculate alpha
            alpha = int(255 * (particle.lifetime / particle.max_lifetime))
            alpha = max(0, min(255, alpha))

            # Draw particle
            color_with_alpha = (*particle.color, alpha)
            particle_surface = pygame.Surface((particle.size, particle.size))
            particle_surface.set_alpha(alpha)
            particle_surface.fill(particle.color)

            screen_x = int(particle.x)
            screen_y = int(particle.y)
            self.screen.blit(particle_surface, (screen_x, screen_y))

        # Remove expired particles
        for particle in particles_to_remove:
            self.particles.remove(particle)

    def add_floating_text(self, text: str, x: int, y: int,
                          color: Tuple[int, int, int] = (255, 255, 255),
                          lifetime: float = 0.8):
        """Add floating text at a position.

        Args:
            text: Text to display
            x: X position (world coordinates)
            y: Y position (world coordinates)
            color: RGB color
            lifetime: Duration in seconds
        """
        # Convert world coords to screen coords
        screen_x = (x - self.camera_x) * self.config.tile_size
        screen_y = (y - self.camera_y) * self.config.tile_size

        floating_text = FloatingText(
            text=text,
            x=screen_x,
            y=screen_y,
            color=color,
            lifetime=lifetime,
            max_lifetime=lifetime
        )
        self.floating_texts.append(floating_text)

    def add_particle(self, x: int, y: int, vx: float, vy: float,
                     color: Tuple[int, int, int], size: int = 4,
                     lifetime: float = 1.0):
        """Add a particle effect.

        Args:
            x: X position (world coordinates)
            y: Y position (world coordinates)
            vx: X velocity (pixels per second)
            vy: Y velocity (pixels per second)
            color: RGB color
            size: Particle size in pixels
            lifetime: Duration in seconds
        """
        # Convert world coords to screen coords
        screen_x = (x - self.camera_x) * self.config.tile_size
        screen_y = (y - self.camera_y) * self.config.tile_size

        particle = Particle(
            x=screen_x,
            y=screen_y,
            vx=vx,
            vy=vy,
            color=color,
            size=size,
            lifetime=lifetime,
            max_lifetime=lifetime
        )
        self.particles.append(particle)
