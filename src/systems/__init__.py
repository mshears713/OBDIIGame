"""
Systems Package

This package contains all game systems that operate on entities and components.

Educational Note:
    In ECS architecture, systems contain the game logic. They operate on
    entities that have specific components, implementing game behaviors.

    Examples:
    - RenderSystem: Draws entities with PositionComponent + RenderComponent
    - MovementSystem: Moves entities with PositionComponent
    - CombatSystem: Resolves combat between entities with HealthComponent
"""

from src.systems.renderer import Renderer
from src.systems.movement import MovementSystem
from src.systems.input_handler import InputHandler, Action, Command
from src.systems.crafting import CraftingSystem, Recipe, get_crafting_system, reset_crafting_system
from src.systems.save_load import SaveLoadSystem, get_save_load_system
from src.systems.ai import AISystem
from src.systems.combat import CombatSystem

__all__ = [
    'Renderer',
    'MovementSystem',
    'InputHandler',
    'Action',
    'Command',
    'CraftingSystem',
    'Recipe',
    'get_crafting_system',
    'reset_crafting_system',
    'SaveLoadSystem',
    'get_save_load_system',
    'AISystem',
    'CombatSystem',
]
