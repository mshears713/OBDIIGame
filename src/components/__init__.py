"""
Component Package

This package contains all component classes for the Entity-Component-System.

Educational Note:
    Components are data containers that define entity capabilities.
    By importing them here, other modules can use:
        from src.components import PositionComponent, HealthComponent
    instead of:
        from src.components.position import PositionComponent
        from src.components.health import HealthComponent
"""

from src.components.base import Component
from src.components.position import PositionComponent
from src.components.render import (
    RenderComponent,
    create_player_render,
    create_enemy_render,
    create_item_render
)
from src.components.health import HealthComponent
from src.components.name import NameComponent
from src.components.input import InputComponent
from src.components.signal import SignalComponent
from src.components.status_effect import StatusEffectComponent, StatusEffect
from src.components.tile_effect import TileEffectComponent
from src.components.ai import AIComponent, AIBehavior
from src.components.combat import CombatComponent
from src.components.inventory import InventoryComponent

__all__ = [
    'Component',
    'PositionComponent',
    'RenderComponent',
    'HealthComponent',
    'NameComponent',
    'InputComponent',
    'SignalComponent',
    'StatusEffectComponent',
    'StatusEffect',
    'TileEffectComponent',
    'AIComponent',
    'AIBehavior',
    'CombatComponent',
    'InventoryComponent',
    'create_player_render',
    'create_enemy_render',
    'create_item_render',
]
