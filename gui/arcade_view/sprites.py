"""
Sprite Management

Handles creation and management of all game sprites including tiles,
entities, and animated sprites.
"""

import arcade
from typing import List, Optional, Dict
from src.entities.entity import Entity
from src.components import PositionComponent, RenderComponent, HealthComponent
from .config import TILE_WIDTH, TILE_HEIGHT, SPRITE_SCALING
from .assets import get_asset_manager


class TileSpriteFactory:
    """
    Factory for creating sprites from ASCII tile characters.

    This converts the ASCII map representation into Arcade sprites,
    maintaining the game's original tile-based structure.
    """

    def __init__(self):
        """Initialize the tile sprite factory."""
        self.asset_manager = get_asset_manager()

    def create_tile_sprite(self, tile_char: str, x: int, y: int) -> arcade.Sprite:
        """
        Create a sprite for a map tile.

        Args:
            tile_char: ASCII character representing the tile
            x: Grid X coordinate
            y: Grid Y coordinate

        Returns:
            Arcade sprite positioned at the given tile coordinates
        """
        texture = self.asset_manager.get_texture(tile_char)

        sprite = arcade.Sprite()
        sprite.texture = texture
        sprite.center_x = x * TILE_WIDTH + TILE_WIDTH / 2
        sprite.center_y = y * TILE_HEIGHT + TILE_HEIGHT / 2
        sprite.scale = SPRITE_SCALING

        return sprite


class EntitySprite(arcade.Sprite):
    """
    Enhanced sprite class for game entities.

    Extends arcade.Sprite to include:
    - Reference to the underlying game Entity
    - Health bar rendering
    - Animation state
    """

    def __init__(self, entity: Entity, texture: arcade.Texture):
        """
        Initialize entity sprite.

        Args:
            entity: The game Entity this sprite represents
            texture: The texture for the sprite
        """
        super().__init__()
        self.entity = entity
        self.texture = texture
        self.scale = SPRITE_SCALING

        # Animation
        self.animation_frames: List[arcade.Texture] = []
        self.current_frame = 0
        self.animation_time = 0.0
        self.animation_speed = 0.15  # seconds per frame

        # Update position from entity
        self.update_from_entity()

    def update_from_entity(self):
        """Update sprite position and state from the underlying entity."""
        pos = self.entity.get_component(PositionComponent)
        if pos:
            self.center_x = pos.x * TILE_WIDTH + TILE_WIDTH / 2
            self.center_y = pos.y * TILE_HEIGHT + TILE_HEIGHT / 2

    def update_animation(self, delta_time: float):
        """
        Update animation state.

        Args:
            delta_time: Time elapsed since last update
        """
        if not self.animation_frames:
            return

        self.animation_time += delta_time
        if self.animation_time >= self.animation_speed:
            self.animation_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.texture = self.animation_frames[self.current_frame]

    def draw_health_bar(self):
        """Draw health bar above the sprite if entity has health."""
        health_comp = self.entity.get_component(HealthComponent)
        if not health_comp:
            return

        # Only draw health bar if damaged
        if health_comp.current_hp >= health_comp.max_hp:
            return

        from .config import COLOR_HEALTH_BAR_GOOD, COLOR_HEALTH_BAR_WARNING, COLOR_HEALTH_BAR_CRITICAL

        # Health bar dimensions
        bar_width = 30
        bar_height = 4
        bar_offset_y = 20  # pixels above sprite

        # Calculate health percentage
        health_pct = health_comp.current_hp / health_comp.max_hp if health_comp.max_hp > 0 else 0

        # Choose color based on health
        if health_pct > 0.6:
            bar_color = COLOR_HEALTH_BAR_GOOD
        elif health_pct > 0.3:
            bar_color = COLOR_HEALTH_BAR_WARNING
        else:
            bar_color = COLOR_HEALTH_BAR_CRITICAL

        # Draw background (dark)
        arcade.draw_rectangle_filled(
            self.center_x,
            self.center_y + bar_offset_y,
            bar_width,
            bar_height,
            (50, 50, 50)
        )

        # Draw health bar
        arcade.draw_rectangle_filled(
            self.center_x - bar_width / 2 + (bar_width * health_pct) / 2,
            self.center_y + bar_offset_y,
            bar_width * health_pct,
            bar_height,
            bar_color
        )


class SpriteManager:
    """
    Manages all sprite lists for the game.

    Organizes sprites into layers for efficient rendering:
    - Terrain (floors, walls)
    - Items
    - Actors (player, enemies)
    - Effects (particles, projectiles)
    """

    def __init__(self):
        """Initialize sprite manager with empty sprite lists."""
        # Sprite lists for different layers
        self.terrain_sprites = arcade.SpriteList(use_spatial_hash=True)
        self.item_sprites = arcade.SpriteList()
        self.actor_sprites = arcade.SpriteList()
        self.effect_sprites = arcade.SpriteList()

        # Entity sprite mapping
        self.entity_to_sprite: Dict[int, EntitySprite] = {}  # entity.id -> sprite

        self.factory = TileSpriteFactory()
        self.asset_manager = get_asset_manager()

    def create_terrain_sprites(self, game_map) -> None:
        """
        Create sprites for all terrain tiles in the map.

        Args:
            game_map: The game Map object
        """
        self.terrain_sprites.clear()

        for y in range(game_map.height):
            for x in range(game_map.width):
                tile = game_map.get_tile(x, y)
                if tile:
                    # Determine tile character for rendering
                    if tile.blocks_movement:
                        tile_char = '#'
                    else:
                        tile_char = '.'

                    sprite = self.factory.create_tile_sprite(tile_char, x, y)
                    self.terrain_sprites.append(sprite)

    def create_entity_sprite(self, entity: Entity) -> Optional[EntitySprite]:
        """
        Create a sprite for a game entity.

        Args:
            entity: The Entity to create a sprite for

        Returns:
            EntitySprite, or None if entity can't be rendered
        """
        # Get render component
        render_comp = entity.get_component(RenderComponent)
        if not render_comp:
            return None

        # Get texture
        texture = self.asset_manager.get_entity_texture(
            entity.name if hasattr(entity, 'name') else 'unknown',
            entity.tags
        )

        # Create sprite
        sprite = EntitySprite(entity, texture)

        # Store mapping
        self.entity_to_sprite[id(entity)] = sprite

        return sprite

    def update_entity_sprites(self, entities: List[Entity]):
        """
        Update sprites for all entities.

        Adds new entities, removes dead ones, updates positions.

        Args:
            entities: List of all active game entities
        """
        # Clear actor and item sprites
        self.actor_sprites.clear()
        self.item_sprites.clear()

        # Track which entities we've seen
        seen_entities = set()

        for entity in entities:
            entity_id = id(entity)
            seen_entities.add(entity_id)

            # Get or create sprite
            if entity_id not in self.entity_to_sprite:
                sprite = self.create_entity_sprite(entity)
                if not sprite:
                    continue
            else:
                sprite = self.entity_to_sprite[entity_id]
                sprite.update_from_entity()

            # Add to appropriate sprite list
            if 'item' in entity.tags:
                self.item_sprites.append(sprite)
            else:
                self.actor_sprites.append(sprite)

        # Remove sprites for dead entities
        dead_entities = set(self.entity_to_sprite.keys()) - seen_entities
        for entity_id in dead_entities:
            del self.entity_to_sprite[entity_id]

    def update_animations(self, delta_time: float):
        """
        Update all sprite animations.

        Args:
            delta_time: Time elapsed since last update
        """
        for sprite in self.actor_sprites:
            if isinstance(sprite, EntitySprite):
                sprite.update_animation(delta_time)

    def draw_all(self):
        """Draw all sprite lists in correct order (back to front)."""
        self.terrain_sprites.draw()
        self.item_sprites.draw()
        self.actor_sprites.draw()
        self.effect_sprites.draw()

    def draw_health_bars(self):
        """Draw health bars for all entities."""
        for sprite in self.actor_sprites:
            if isinstance(sprite, EntitySprite):
                sprite.draw_health_bar()
