"""
Player Entity Factory

This module provides factory functions for creating the player entity.

Educational Notes:
------------------
Factory functions are functions that create and return objects with specific
configurations. Instead of manually assembling the player entity every time,
we use a factory function that encapsulates the creation logic.

Benefits of factory functions:
1. Consistency: Player always created with correct components
2. Maintainability: Change player setup in one place
3. Readability: create_player() is clearer than manual assembly
4. Testing: Easy to create test players with specific properties

The player is composed of multiple components following ECS architecture:
- PositionComponent: Location in the dungeon
- RenderComponent: Visual appearance ('@' symbol)
- HealthComponent: Hit points and death state
- NameComponent: Display name
- InputComponent: Marks as player-controlled
"""

from typing import Tuple
from src.entities.entity import Entity
from src.components import (
    PositionComponent,
    RenderComponent,
    HealthComponent,
    NameComponent,
    InputComponent,
    create_player_render
)


def create_player(x: int = 0, y: int = 0, name: str = "Player") -> Entity:
    """
    Create a player entity with all necessary components.

    Args:
        x: Starting X position (default 0)
        y: Starting Y position (default 0)
        name: Player's name (default "Player")

    Returns:
        Entity configured as the player character

    Educational Note:
        This factory encapsulates player creation. The player has:
        - Position: Where they are in the dungeon
        - Render: How they appear ('@' in white)
        - Health: 100 HP to start
        - Name: For display in messages
        - Input: Marks them as player-controlled

        By using a factory, we ensure every player has these required
        components and is configured consistently.

    Example:
        >>> # Create player at specific location
        >>> player = create_player(x=10, y=15, name="Hero")
        >>>
        >>> # Player has all necessary components
        >>> assert player.has_component(PositionComponent)
        >>> assert player.has_component(HealthComponent)
        >>> assert player.has_component(InputComponent)
        >>>
        >>> # Get player position
        >>> pos = player.get_component(PositionComponent)
        >>> assert pos.x == 10 and pos.y == 15
    """
    # Create new entity
    player = Entity()

    # Add player tag for easy identification
    player.add_tag("player")

    # Add position component
    player.add_component(PositionComponent(x=x, y=y))

    # Add render component (@ symbol in white)
    player.add_component(create_player_render())

    # Add health component (100 HP)
    player.add_component(HealthComponent(current_hp=100, max_hp=100))

    # Add name component
    player.add_component(NameComponent(
        name=name,
        description="An intrepid technician exploring the ECU system"
    ))

    # Add input component (marks as player-controlled)
    player.add_component(InputComponent())

    return player


def get_player_position(player: Entity) -> Tuple[int, int]:
    """
    Get player's current position.

    Args:
        player: The player entity

    Returns:
        (x, y) tuple of player coordinates

    Educational Note:
        Convenience function for common operation. Instead of:
            pos = player.get_component(PositionComponent)
            x, y = pos.x, pos.y

        You can write:
            x, y = get_player_position(player)

    Example:
        >>> player = create_player(x=10, y=15)
        >>> x, y = get_player_position(player)
        >>> assert x == 10 and y == 15
    """
    pos = player.get_component(PositionComponent)
    if pos:
        return (pos.x, pos.y)
    return (0, 0)


def set_player_position(player: Entity, x: int, y: int) -> None:
    """
    Set player's position to new coordinates.

    Args:
        player: The player entity
        x: New X coordinate
        y: New Y coordinate

    Educational Note:
        Useful for:
        - Spawning player at dungeon start
        - Teleportation effects
        - Respawning after death
        - Level transitions

    Example:
        >>> player = create_player()
        >>> set_player_position(player, 20, 25)
        >>> x, y = get_player_position(player)
        >>> assert x == 20 and y == 25
    """
    pos = player.get_component(PositionComponent)
    if pos:
        pos.set_position(x, y)


def is_player(entity: Entity) -> bool:
    """
    Check if an entity is the player.

    Args:
        entity: Entity to check

    Returns:
        True if entity has InputComponent (is player), False otherwise

    Educational Note:
        Two ways to identify the player:
        1. Check for InputComponent (used here)
        2. Check for "player" tag

        InputComponent is more reliable since it's unique to the player.
        Tags can be added to multiple entities.

    Example:
        >>> player = create_player()
        >>> enemy = Entity()
        >>> assert is_player(player) is True
        >>> assert is_player(enemy) is False
    """
    return entity.has_component(InputComponent)


def get_player_health(player: Entity) -> Tuple[int, int]:
    """
    Get player's current and maximum HP.

    Args:
        player: The player entity

    Returns:
        (current_hp, max_hp) tuple

    Example:
        >>> player = create_player()
        >>> current, maximum = get_player_health(player)
        >>> assert current == 100 and maximum == 100
        >>>
        >>> # Take damage
        >>> health = player.get_component(HealthComponent)
        >>> health.take_damage(30)
        >>> current, maximum = get_player_health(player)
        >>> assert current == 70 and maximum == 100
    """
    health = player.get_component(HealthComponent)
    if health:
        return (health.current_hp, health.max_hp)
    return (0, 0)


def is_player_alive(player: Entity) -> bool:
    """
    Check if player is alive.

    Args:
        player: The player entity

    Returns:
        True if player has HP > 0, False if dead

    Educational Note:
        Central check for game over conditions. When player dies:
        - Stop accepting input
        - Display death message
        - Offer restart/load options

    Example:
        >>> player = create_player()
        >>> assert is_player_alive(player) is True
        >>>
        >>> # Take fatal damage
        >>> health = player.get_component(HealthComponent)
        >>> health.take_damage(200)
        >>> assert is_player_alive(player) is False
    """
    health = player.get_component(HealthComponent)
    if health:
        return health.is_alive()
    return False
