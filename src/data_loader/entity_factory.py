"""
Entity Factory - Creates game entities from JSON definitions

This module provides factory functions to instantiate entities (enemies, items, etc.)
from JSON configuration files, automatically creating and attaching the appropriate
components based on the JSON data.

Educational Notes:
------------------
The Factory Pattern is a creational design pattern that provides an interface for
creating objects without specifying their exact class. In this case, we read JSON
configuration and create entity objects with the correct components.

Benefits of Entity Factories:
1. **Centralized Entity Creation:** All entity creation logic in one place
2. **Data-Driven Design:** Entities defined in JSON, not hardcoded
3. **Consistency:** All entities created the same way
4. **Easy Testing:** Mock JSON data for tests
5. **Modding Support:** Players can add new entities via JSON

The factory pattern combined with ECS architecture provides maximum flexibility:
- JSON defines what components an entity has
- Factory attaches those components
- Systems operate on component combinations
"""

from typing import Optional, Dict, Any, List
from src.entities.entity import Entity
from src.components import (
    PositionComponent,
    RenderComponent,
    HealthComponent,
    NameComponent,
    SignalComponent,
    InputComponent
)
from src.data_loader.json_loader import JSONLoader


class EntityFactory:
    """
    Factory for creating entities from JSON definitions.

    This factory reads JSON configurations and constructs complete Entity objects
    with all necessary components attached.

    Educational Note:
        The factory separates entity creation from entity use. Systems don't need
        to know how entities are created - they just operate on components.

        This is the Single Responsibility Principle in action: the factory's job
        is creation, systems' job is logic.

    Example:
        >>> factory = EntityFactory()
        >>> enemy = factory.create_enemy("corrupted_packet", x=10, y=5)
        >>> # Enemy has HealthComponent, RenderComponent, etc.
        >>> health = enemy.get_component(HealthComponent)
        >>> print(f"Enemy HP: {health.max_hp}")
    """

    def __init__(self, json_loader: Optional[JSONLoader] = None):
        """
        Initialize entity factory.

        Args:
            json_loader: JSONLoader instance (creates new one if not provided)

        Educational Note:
            Dependency Injection pattern - we can pass in a JSONLoader,
            making testing easier (can inject a mock loader).
        """
        self.loader = json_loader if json_loader else JSONLoader()

    def create_enemy(
        self,
        enemy_id: str,
        x: int = 0,
        y: int = 0,
        floor_level: int = 1
    ) -> Optional[Entity]:
        """
        Create an enemy entity from JSON definition.

        Args:
            enemy_id: Enemy type identifier (e.g., "corrupted_packet")
            x: Spawn X coordinate
            y: Spawn Y coordinate
            floor_level: Current floor level (for scaling)

        Returns:
            Enemy Entity with all components, or None if definition not found

        Educational Note:
            This method demonstrates the Factory pattern:
            1. Load data (from JSON)
            2. Create base object (Entity)
            3. Configure object (add components from data)
            4. Return configured object

        Example:
            >>> factory = EntityFactory()
            >>> enemy = factory.create_enemy("corrupted_packet", x=15, y=10)
            >>> if enemy:
            ...     print(f"Created: {enemy.get_component(NameComponent).name}")
        """
        # Load enemy definition from JSON
        enemy_data = self.loader.load_enemy(enemy_id)
        if enemy_data is None:
            return None

        # Create base entity
        entity = Entity()
        entity.add_tag("enemy")

        # Add position component
        position = PositionComponent(x=x, y=y)
        entity.add_component(position)

        # Add name component
        name_comp = NameComponent(
            name=enemy_data.get("name", "Unknown Enemy"),
            description=enemy_data.get("description", "")
        )
        entity.add_component(name_comp)

        # Add render component from visual data
        visual = enemy_data.get("visual", {})
        render = RenderComponent(
            char=visual.get("ascii_char", "?"),
            color=visual.get("color", "white"),
            render_order=visual.get("render_order", 3)
        )
        entity.add_component(render)

        # Add components from component definitions
        components_data = enemy_data.get("components", {})

        # Health component
        if "health" in components_data:
            health_data = components_data["health"]
            health = HealthComponent(
                current_hp=health_data.get("current_hp", 10),
                max_hp=health_data.get("max_hp", 10)
            )
            # Apply floor level scaling if specified
            if floor_level > 1:
                scaling = enemy_data.get("metadata", {}).get("hp_scaling", 1.1)
                scaled_hp = int(health.max_hp * (scaling ** (floor_level - 1)))
                health.set_max_hp(scaled_hp)
                health.restore_to_full()
            entity.add_component(health)

        # Combat component (placeholder for future)
        # Will be implemented in a future step

        # AI component (placeholder for future)
        # Will be implemented in a future step

        # Signal component - enemies can drop signals
        signals = SignalComponent(max_signal_types=5, max_per_signal=3)
        # Add some default signals based on enemy type
        metadata = enemy_data.get("metadata", {})
        if "signal_drops" in metadata:
            for drop in metadata["signal_drops"]:
                signals.add_signal(drop["signal_type"], drop.get("quantity", 1))
        entity.add_component(signals)

        return entity

    def create_item(
        self,
        item_id: str,
        x: int = 0,
        y: int = 0
    ) -> Optional[Entity]:
        """
        Create an item entity from JSON definition.

        Args:
            item_id: Item type identifier (e.g., "signal_boost")
            x: Spawn X coordinate
            y: Spawn Y coordinate

        Returns:
            Item Entity with all components, or None if definition not found

        Educational Note:
            Items are entities too! They just have different component combinations
            than enemies or the player. This is the power of ECS - entities are
            just bags of components.

        Example:
            >>> factory = EntityFactory()
            >>> item = factory.create_item("signal_boost", x=5, y=5)
            >>> # Item can be picked up, used, etc.
        """
        # Load item definition from JSON
        item_data = self.loader.load_item(item_id)
        if item_data is None:
            return None

        # Create base entity
        entity = Entity()
        entity.add_tag("item")

        # Add position component
        position = PositionComponent(x=x, y=y)
        entity.add_component(position)

        # Add name component
        name_comp = NameComponent(
            name=item_data.get("name", "Unknown Item"),
            description=item_data.get("description", "")
        )
        entity.add_component(name_comp)

        # Add render component from visual data
        visual = item_data.get("visual", {})
        render = RenderComponent(
            char=visual.get("ascii_char", "?"),
            color=visual.get("color", "white"),
            render_order=visual.get("render_order", 1)
        )
        entity.add_component(render)

        # Items can contain signals
        signals = SignalComponent()

        # Add signals from item definition
        if "signals" in item_data:
            for signal_type, quantity in item_data["signals"].items():
                signals.add_signal(signal_type, quantity)

        entity.add_component(signals)

        # TODO: Add item-specific components (consumable, equippable, etc.)
        # Will be implemented based on item properties

        return entity

    def create_enemy_batch(
        self,
        enemy_id: str,
        positions: List[tuple],
        floor_level: int = 1
    ) -> List[Entity]:
        """
        Create multiple enemies of the same type at different positions.

        Args:
            enemy_id: Enemy type identifier
            positions: List of (x, y) tuples for spawn locations
            floor_level: Current floor level

        Returns:
            List of enemy entities

        Educational Note:
            Batch creation is more efficient than individual creation for
            spawning groups of the same enemy type. We can reuse the loaded
            JSON data rather than loading it multiple times.

        Example:
            >>> positions = [(5, 5), (10, 10), (15, 3)]
            >>> enemies = factory.create_enemy_batch("corrupted_packet", positions)
            >>> print(f"Created {len(enemies)} enemies")
        """
        # Pre-load enemy data once
        enemy_data = self.loader.load_enemy(enemy_id)
        if enemy_data is None:
            return []

        enemies = []
        for x, y in positions:
            enemy = self.create_enemy(enemy_id, x, y, floor_level)
            if enemy:
                enemies.append(enemy)

        return enemies

    def create_from_spawn_data(
        self,
        spawn_config: Dict[str, Any],
        floor_level: int = 1
    ) -> List[Entity]:
        """
        Create entities from spawn configuration (used by floor generator).

        Args:
            spawn_config: Spawn configuration from floor JSON
            floor_level: Current floor level

        Returns:
            List of spawned entities

        Educational Note:
            This method processes spawn configurations from floor JSON files,
            creating the appropriate number of each entity type. It handles
            randomization and weighted spawning.

        Example:
            >>> spawn_config = {
            ...     "enemy_type": "corrupted_packet",
            ...     "count_min": 3,
            ...     "count_max": 5,
            ...     "positions": [(5, 5), (10, 10), (7, 8)]
            ... }
            >>> entities = factory.create_from_spawn_data(spawn_config)
        """
        import random

        entity_type = spawn_config.get("enemy_type") or spawn_config.get("item_type")
        if not entity_type:
            return []

        # Determine spawn count
        count_min = spawn_config.get("count_min", 1)
        count_max = spawn_config.get("count_max", 1)
        spawn_count = random.randint(count_min, count_max)

        # Get positions (if provided)
        positions = spawn_config.get("positions", [])

        entities = []

        # Spawn enemies or items
        if "enemy_type" in spawn_config:
            if positions:
                # Use provided positions
                positions_to_use = random.sample(positions, min(spawn_count, len(positions)))
            else:
                # Positions will be assigned later by dungeon generator
                positions_to_use = [(0, 0)] * spawn_count

            for x, y in positions_to_use:
                enemy = self.create_enemy(entity_type, x, y, floor_level)
                if enemy:
                    entities.append(enemy)

        elif "item_type" in spawn_config:
            if positions:
                positions_to_use = random.sample(positions, min(spawn_count, len(positions)))
            else:
                positions_to_use = [(0, 0)] * spawn_count

            for x, y in positions_to_use:
                item = self.create_item(entity_type, x, y)
                if item:
                    entities.append(item)

        return entities


# Module-level convenience functions
_default_factory: Optional[EntityFactory] = None


def get_entity_factory() -> EntityFactory:
    """
    Get the global entity factory instance (singleton pattern).

    Returns:
        EntityFactory instance

    Educational Note:
        Lazy singleton - creates factory on first use.
        This ensures JSON loader is only created when needed.
    """
    global _default_factory
    if _default_factory is None:
        _default_factory = EntityFactory()
    return _default_factory


def create_enemy(enemy_id: str, x: int = 0, y: int = 0, floor_level: int = 1) -> Optional[Entity]:
    """
    Convenience function to create an enemy using the global factory.

    Args:
        enemy_id: Enemy type identifier
        x: Spawn X coordinate
        y: Spawn Y coordinate
        floor_level: Current floor level

    Returns:
        Enemy Entity or None

    Example:
        >>> from src.data_loader.entity_factory import create_enemy
        >>> enemy = create_enemy("corrupted_packet", x=10, y=5)
    """
    factory = get_entity_factory()
    return factory.create_enemy(enemy_id, x, y, floor_level)


def create_item(item_id: str, x: int = 0, y: int = 0) -> Optional[Entity]:
    """
    Convenience function to create an item using the global factory.

    Args:
        item_id: Item type identifier
        x: Spawn X coordinate
        y: Spawn Y coordinate

    Returns:
        Item Entity or None

    Example:
        >>> from src.data_loader.entity_factory import create_item
        >>> item = create_item("signal_boost", x=5, y=5)
    """
    factory = get_entity_factory()
    return factory.create_item(item_id, x, y)
