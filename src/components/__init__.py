"""
Components Module

This module provides all component classes for the Entity-Component-System architecture.

Components are data containers that define specific aspects or capabilities of entities.
Import commonly used components directly from this module for convenience.

Example:
    >>> from src.components import PositionComponent, RenderComponent
    >>> position = PositionComponent(x=10, y=20)
    >>> render = RenderComponent(char='@', color='white')
"""

from src.components.base import Component
from src.components.position import PositionComponent
from src.components.render import (
    RenderComponent,
    create_player_render,
    create_enemy_render,
    create_item_render
)

__all__ = [
    'Component',
    'PositionComponent',
    'RenderComponent',
    'create_player_render',
    'create_enemy_render',
    'create_item_render',
]
