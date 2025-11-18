"""
Data Loader Package

This package handles loading game content from JSON configuration files.

Educational Note:
    Data-driven design separates content from code. This package provides
    utilities for loading floors, enemies, items, and other game content
    from JSON files, and factories for creating entities from those definitions.
"""

from src.data_loader.json_loader import JSONLoader, load_floor_config
from src.data_loader.entity_factory import (
    EntityFactory,
    get_entity_factory,
    create_enemy,
    create_item
)

__all__ = [
    'JSONLoader',
    'load_floor_config',
    'EntityFactory',
    'get_entity_factory',
    'create_enemy',
    'create_item',
]
