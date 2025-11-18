"""
Unit Tests for Entity Class

Tests the Entity class and its component management functionality.
"""

import pytest
from src.entities.entity import Entity
from src.components.base import Component


# Create test components for testing
class MockPositionComponent(Component):
    """Mock component for position data."""

    def __init__(self, x: int = 0, y: int = 0):
        super().__init__()
        self.x = x
        self.y = y


class MockHealthComponent(Component):
    """Mock component for health data."""

    def __init__(self, current_hp: int = 100, max_hp: int = 100):
        super().__init__()
        self.current_hp = current_hp
        self.max_hp = max_hp


class MockRenderComponent(Component):
    """Mock component for rendering data."""

    def __init__(self, char: str = '@', color: str = 'white'):
        super().__init__()
        self.char = char
        self.color = color


class TestEntity:
    """Test suite for Entity class."""

    def setup_method(self):
        """Reset entity ID counter before each test."""
        Entity.reset_id_counter(1)

    def test_entity_creation_with_auto_id(self):
        """Test creating entity with auto-generated ID."""
        entity = Entity()
        assert entity.entity_id == 1
        assert len(entity.components) == 0
        assert len(entity.tags) == 0

    def test_entity_creation_with_custom_id(self):
        """Test creating entity with custom ID."""
        entity = Entity(entity_id=42)
        assert entity.entity_id == 42

    def test_entity_auto_id_increments(self):
        """Test that auto-generated IDs increment."""
        entity1 = Entity()
        entity2 = Entity()
        entity3 = Entity()

        assert entity1.entity_id == 1
        assert entity2.entity_id == 2
        assert entity3.entity_id == 3

    def test_entity_creation_with_tags(self):
        """Test creating entity with initial tags."""
        entity = Entity(tags=['enemy', 'aggressive'])
        assert 'enemy' in entity.tags
        assert 'aggressive' in entity.tags

    def test_add_component(self):
        """Test adding a component to entity."""
        entity = Entity()
        position = MockPositionComponent(x=5, y=10)

        entity.add_component(position)

        assert len(entity.components) == 1
        assert 'MockPositionComponent' in entity.components

    def test_add_multiple_components(self):
        """Test adding multiple different components."""
        entity = Entity()

        entity.add_component(MockPositionComponent(x=5, y=10))
        entity.add_component(MockHealthComponent(current_hp=50, max_hp=100))
        entity.add_component(MockRenderComponent(char='@', color='red'))

        assert len(entity.components) == 3
        assert entity.has_component(MockPositionComponent)
        assert entity.has_component(MockHealthComponent)
        assert entity.has_component(MockRenderComponent)

    def test_add_component_overwrites_same_type(self):
        """Test that adding same component type overwrites previous."""
        entity = Entity()

        # Add first position
        entity.add_component(MockPositionComponent(x=5, y=10))

        # Add second position (should overwrite)
        entity.add_component(MockPositionComponent(x=15, y=20))

        assert len(entity.components) == 1
        pos = entity.get_component(MockPositionComponent)
        assert pos.x == 15
        assert pos.y == 20

    def test_get_component_exists(self):
        """Test retrieving a component that exists."""
        entity = Entity()
        position = MockPositionComponent(x=7, y=13)
        entity.add_component(position)

        retrieved = entity.get_component(MockPositionComponent)

        assert retrieved is not None
        assert retrieved.x == 7
        assert retrieved.y == 13

    def test_get_component_not_exists(self):
        """Test retrieving a component that doesn't exist returns None."""
        entity = Entity()

        retrieved = entity.get_component(MockPositionComponent)

        assert retrieved is None

    def test_has_component_true(self):
        """Test has_component returns True when component exists."""
        entity = Entity()
        entity.add_component(MockHealthComponent())

        assert entity.has_component(MockHealthComponent) is True

    def test_has_component_false(self):
        """Test has_component returns False when component doesn't exist."""
        entity = Entity()

        assert entity.has_component(MockHealthComponent) is False

    def test_has_components_all_present(self):
        """Test has_components returns True when all components present."""
        entity = Entity()
        entity.add_component(MockPositionComponent())
        entity.add_component(MockRenderComponent())

        assert entity.has_components(MockPositionComponent, MockRenderComponent) is True

    def test_has_components_some_missing(self):
        """Test has_components returns False when some components missing."""
        entity = Entity()
        entity.add_component(MockPositionComponent())

        # Has position but not render
        assert entity.has_components(MockPositionComponent, MockRenderComponent) is False

    def test_has_components_all_missing(self):
        """Test has_components returns False when all components missing."""
        entity = Entity()

        assert entity.has_components(MockPositionComponent, MockRenderComponent) is False

    def test_remove_component_exists(self):
        """Test removing a component that exists."""
        entity = Entity()
        entity.add_component(MockPositionComponent())

        result = entity.remove_component(MockPositionComponent)

        assert result is True
        assert entity.has_component(MockPositionComponent) is False
        assert len(entity.components) == 0

    def test_remove_component_not_exists(self):
        """Test removing a component that doesn't exist returns False."""
        entity = Entity()

        result = entity.remove_component(MockPositionComponent)

        assert result is False

    def test_add_tag(self):
        """Test adding a tag to entity."""
        entity = Entity()
        entity.add_tag('enemy')

        assert 'enemy' in entity.tags

    def test_add_duplicate_tag_ignored(self):
        """Test adding duplicate tag doesn't create duplicates."""
        entity = Entity()
        entity.add_tag('enemy')
        entity.add_tag('enemy')

        assert entity.tags.count('enemy') == 1

    def test_remove_tag_exists(self):
        """Test removing a tag that exists."""
        entity = Entity(tags=['enemy', 'aggressive'])

        result = entity.remove_tag('aggressive')

        assert result is True
        assert 'aggressive' not in entity.tags
        assert 'enemy' in entity.tags  # Other tag still present

    def test_remove_tag_not_exists(self):
        """Test removing a tag that doesn't exist returns False."""
        entity = Entity()

        result = entity.remove_tag('nonexistent')

        assert result is False

    def test_has_tag_true(self):
        """Test has_tag returns True when tag exists."""
        entity = Entity(tags=['player'])

        assert entity.has_tag('player') is True

    def test_has_tag_false(self):
        """Test has_tag returns False when tag doesn't exist."""
        entity = Entity()

        assert entity.has_tag('player') is False

    def test_to_dict_empty_entity(self):
        """Test serializing empty entity."""
        entity = Entity(entity_id=5)
        data = entity.to_dict()

        assert data['entity_id'] == 5
        assert data['tags'] == []
        assert data['components'] == {}

    def test_to_dict_with_components(self):
        """Test serializing entity with components."""
        entity = Entity(entity_id=10, tags=['enemy'])
        entity.add_component(MockPositionComponent(x=3, y=7))
        entity.add_component(MockHealthComponent(current_hp=50, max_hp=100))

        data = entity.to_dict()

        assert data['entity_id'] == 10
        assert 'enemy' in data['tags']
        assert 'MockPositionComponent' in data['components']
        assert 'MockHealthComponent' in data['components']
        assert data['components']['MockPositionComponent']['x'] == 3
        assert data['components']['MockHealthComponent']['current_hp'] == 50

    def test_from_dict_empty_entity(self):
        """Test deserializing empty entity."""
        data = {'entity_id': 7, 'tags': ['item'], 'components': {}}

        registry = {}
        entity = Entity.from_dict(data, registry)

        assert entity.entity_id == 7
        assert 'item' in entity.tags
        assert len(entity.components) == 0

    def test_from_dict_with_components(self):
        """Test deserializing entity with components."""
        data = {
            'entity_id': 15,
            'tags': ['player'],
            'components': {
                'MockPositionComponent': {
                    'component_type': 'MockPositionComponent',
                    'x': 12,
                    'y': 8
                },
                'MockHealthComponent': {
                    'component_type': 'MockHealthComponent',
                    'current_hp': 75,
                    'max_hp': 100
                }
            }
        }

        registry = {
            'MockPositionComponent': MockPositionComponent,
            'MockHealthComponent': MockHealthComponent
        }

        entity = Entity.from_dict(data, registry)

        assert entity.entity_id == 15
        assert 'player' in entity.tags
        assert entity.has_component(MockPositionComponent)
        assert entity.has_component(MockHealthComponent)

        pos = entity.get_component(MockPositionComponent)
        assert pos.x == 12
        assert pos.y == 8

        health = entity.get_component(MockHealthComponent)
        assert health.current_hp == 75
        assert health.max_hp == 100

    def test_serialization_roundtrip(self):
        """Test that serialize -> deserialize preserves entity state."""
        original = Entity(entity_id=20, tags=['enemy', 'boss'])
        original.add_component(MockPositionComponent(x=25, y=30))
        original.add_component(MockHealthComponent(current_hp=200, max_hp=200))

        # Serialize
        data = original.to_dict()

        # Deserialize
        registry = {
            'MockPositionComponent': MockPositionComponent,
            'MockHealthComponent': MockHealthComponent
        }
        restored = Entity.from_dict(data, registry)

        # Verify entity properties
        assert restored.entity_id == original.entity_id
        assert set(restored.tags) == set(original.tags)

        # Verify components
        orig_pos = original.get_component(MockPositionComponent)
        rest_pos = restored.get_component(MockPositionComponent)
        assert rest_pos.x == orig_pos.x
        assert rest_pos.y == orig_pos.y

        orig_health = original.get_component(MockHealthComponent)
        rest_health = restored.get_component(MockHealthComponent)
        assert rest_health.current_hp == orig_health.current_hp
        assert rest_health.max_hp == orig_health.max_hp

    def test_repr_output(self):
        """Test string representation of entity."""
        entity = Entity(entity_id=100, tags=['test'])
        entity.add_component(MockPositionComponent())

        repr_str = repr(entity)

        assert 'Entity(id=100' in repr_str
        assert 'test' in repr_str
        assert 'MockPositionComponent' in repr_str

    def test_reset_id_counter(self):
        """Test resetting entity ID counter."""
        Entity()  # ID will be 1
        Entity()  # ID will be 2

        Entity.reset_id_counter(100)

        entity = Entity()
        assert entity.entity_id == 100

    def test_custom_id_updates_counter(self):
        """Test that providing custom ID updates the counter."""
        Entity.reset_id_counter(1)

        # Create entity with high ID
        Entity(entity_id=50)

        # Next auto-generated ID should be after 50
        entity = Entity()
        assert entity.entity_id == 51
