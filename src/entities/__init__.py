"""
Entity Package

This package contains the Entity class and entity factory functions.

Educational Note:
    Entities are containers for components. Factory functions provide
    convenient ways to create pre-configured entities (player, enemies, items).
"""

from src.entities.entity import Entity
from src.entities.player import (
    create_player,
    get_player_position,
    set_player_position,
    is_player,
    get_player_health,
    is_player_alive
)

__all__ = [
    'Entity',
    'create_player',
    'get_player_position',
    'set_player_position',
    'is_player',
    'get_player_health',
    'is_player_alive',
]
