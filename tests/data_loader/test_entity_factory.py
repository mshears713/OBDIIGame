"""
Tests for EntityFactory

Educational Note:
    These tests verify that entities can be properly created from JSON definitions.
"""

import pytest
from src.data_loader.entity_factory import EntityFactory, get_entity_factory, create_enemy, create_item
from src.entities.entity import Entity
from src.components import (
    PositionComponent,
    RenderComponent,
    HealthComponent,
    NameComponent,
    SignalComponent
)


class TestEntityFactory:
    """Test entity factory initialization and basic functionality."""

    def test_factory_initialization(self):
        """Test creating an entity factory."""
        factory = EntityFactory()
        assert factory is not None
        assert factory.loader is not None

    def test_global_factory_singleton(self):
        """Test that get_entity_factory returns singleton."""
        factory1 = get_entity_factory()
        factory2 = get_entity_factory()
        assert factory1 is factory2


class TestEnemyCreation:
    """Test creating enemies from JSON definitions."""

    @pytest.fixture
    def factory(self):
        """Provide entity factory for tests."""
        return EntityFactory()

    def test_create_enemy_basic(self, factory):
        """Test creating a basic enemy."""
        Entity.reset_id_counter()
        enemy = factory.create_enemy("corrupted_packet", x=10, y=5)

        assert enemy is not None
        assert enemy.has_tag("enemy")

    def test_enemy_has_required_components(self, factory):
        """Test that created enemy has all required components."""
        enemy = factory.create_enemy("corrupted_packet", x=10, y=5)

        assert enemy.has_component(PositionComponent)
        assert enemy.has_component(RenderComponent)
        assert enemy.has_component(HealthComponent)
        assert enemy.has_component(NameComponent)
        assert enemy.has_component(SignalComponent)

    def test_enemy_position(self, factory):
        """Test that enemy is created at correct position."""
        enemy = factory.create_enemy("corrupted_packet", x=15, y=20)

        position = enemy.get_component(PositionComponent)
        assert position.x == 15
        assert position.y == 20

    def test_enemy_health_from_json(self, factory):
        """Test that enemy health is loaded from JSON."""
        enemy = factory.create_enemy("corrupted_packet")

        health = enemy.get_component(HealthComponent)
        assert health.max_hp == 10  # From JSON
        assert health.current_hp == 10

    def test_enemy_name_from_json(self, factory):
        """Test that enemy name is loaded from JSON."""
        enemy = factory.create_enemy("corrupted_packet")

        name = enemy.get_component(NameComponent)
        assert name.name == "Corrupted Data Packet"
        assert "CAN bus" in name.description

    def test_enemy_render_from_json(self, factory):
        """Test that enemy visual is loaded from JSON."""
        enemy = factory.create_enemy("corrupted_packet")

        render = enemy.get_component(RenderComponent)
        assert render.char == "p"
        assert render.color == "red"

    def test_enemy_signals(self, factory):
        """Test that enemy has signal drops from JSON."""
        enemy = factory.create_enemy("corrupted_packet")

        signals = enemy.get_component(SignalComponent)
        # Check signal drops from JSON
        assert signals.get_signal_count("corrupted_packet") == 1
        assert signals.get_signal_count("sensor_reading") == 1

    def test_enemy_floor_scaling(self, factory):
        """Test that enemy stats scale with floor level."""
        enemy_floor1 = factory.create_enemy("corrupted_packet", floor_level=1)
        enemy_floor3 = factory.create_enemy("corrupted_packet", floor_level=3)

        health1 = enemy_floor1.get_component(HealthComponent)
        health3 = enemy_floor3.get_component(HealthComponent)

        # Floor 3 should have more HP due to scaling
        assert health3.max_hp > health1.max_hp

    def test_create_nonexistent_enemy(self, factory):
        """Test creating an enemy that doesn't exist returns None."""
        enemy = factory.create_enemy("nonexistent_enemy")
        assert enemy is None

    def test_create_enemy_batch(self, factory):
        """Test creating multiple enemies at once."""
        positions = [(5, 5), (10, 10), (15, 15)]
        enemies = factory.create_enemy_batch("corrupted_packet", positions)

        assert len(enemies) == 3
        assert all(e.has_tag("enemy") for e in enemies)

        # Check positions
        pos0 = enemies[0].get_component(PositionComponent)
        assert (pos0.x, pos0.y) == (5, 5)

        pos2 = enemies[2].get_component(PositionComponent)
        assert (pos2.x, pos2.y) == (15, 15)


class TestItemCreation:
    """Test creating items from JSON definitions."""

    @pytest.fixture
    def factory(self):
        """Provide entity factory for tests."""
        return EntityFactory()

    def test_create_item_basic(self, factory):
        """Test creating a basic item."""
        Entity.reset_id_counter()
        item = factory.create_item("signal_boost", x=3, y=7)

        assert item is not None
        assert item.has_tag("item")

    def test_item_has_required_components(self, factory):
        """Test that created item has all required components."""
        item = factory.create_item("signal_boost")

        assert item.has_component(PositionComponent)
        assert item.has_component(RenderComponent)
        assert item.has_component(NameComponent)
        assert item.has_component(SignalComponent)

    def test_item_position(self, factory):
        """Test that item is created at correct position."""
        item = factory.create_item("signal_boost", x=12, y=8)

        position = item.get_component(PositionComponent)
        assert position.x == 12
        assert position.y == 8

    def test_item_name_from_json(self, factory):
        """Test that item name is loaded from JSON."""
        item = factory.create_item("signal_boost")

        name = item.get_component(NameComponent)
        assert name.name == "Signal Boost"
        assert "integrity" in name.description.lower()

    def test_item_render_from_json(self, factory):
        """Test that item visual is loaded from JSON."""
        item = factory.create_item("signal_boost")

        render = item.get_component(RenderComponent)
        assert render.char == "!"
        assert render.color == "cyan"

    def test_item_signals(self, factory):
        """Test that item contains signals from JSON."""
        item = factory.create_item("signal_boost")

        signals = item.get_component(SignalComponent)
        # Signal boost should contain error_correction signal
        assert signals.get_signal_count("error_correction") == 1

    def test_create_nonexistent_item(self, factory):
        """Test creating an item that doesn't exist returns None."""
        item = factory.create_item("nonexistent_item")
        assert item is None


class TestConvenienceFunctions:
    """Test module-level convenience functions."""

    def test_create_enemy_function(self):
        """Test create_enemy convenience function."""
        Entity.reset_id_counter()
        enemy = create_enemy("corrupted_packet", x=5, y=5)

        assert enemy is not None
        assert enemy.has_tag("enemy")

    def test_create_item_function(self):
        """Test create_item convenience function."""
        Entity.reset_id_counter()
        item = create_item("signal_boost", x=3, y=3)

        assert item is not None
        assert item.has_tag("item")


class TestSpawnDataProcessing:
    """Test creating entities from spawn configuration data."""

    @pytest.fixture
    def factory(self):
        """Provide entity factory for tests."""
        return EntityFactory()

    def test_create_from_spawn_data_enemy(self, factory):
        """Test creating enemies from spawn configuration."""
        import random
        random.seed(42)  # Deterministic testing

        spawn_config = {
            "enemy_type": "corrupted_packet",
            "count_min": 2,
            "count_max": 2,
            "positions": [(5, 5), (10, 10), (15, 15)]
        }

        entities = factory.create_from_spawn_data(spawn_config)

        assert len(entities) == 2
        assert all(e.has_tag("enemy") for e in entities)

    def test_create_from_spawn_data_item(self, factory):
        """Test creating items from spawn configuration."""
        import random
        random.seed(42)

        spawn_config = {
            "item_type": "signal_boost",
            "count_min": 1,
            "count_max": 1,
            "positions": [(3, 3)]
        }

        entities = factory.create_from_spawn_data(spawn_config)

        assert len(entities) == 1
        assert entities[0].has_tag("item")


class TestEdgeCases:
    """Test edge cases and error handling."""

    @pytest.fixture
    def factory(self):
        """Provide entity factory for tests."""
        return EntityFactory()

    def test_create_with_default_position(self, factory):
        """Test creating entity with default position (0, 0)."""
        enemy = factory.create_enemy("corrupted_packet")
        position = enemy.get_component(PositionComponent)
        assert position.x == 0
        assert position.y == 0

    def test_create_batch_with_empty_positions(self, factory):
        """Test creating batch with empty position list."""
        enemies = factory.create_enemy_batch("corrupted_packet", [])
        assert enemies == []

    def test_multiple_enemies_have_unique_ids(self, factory):
        """Test that multiple enemies get unique entity IDs."""
        Entity.reset_id_counter()
        enemy1 = factory.create_enemy("corrupted_packet")
        enemy2 = factory.create_enemy("corrupted_packet")

        assert enemy1.entity_id != enemy2.entity_id
