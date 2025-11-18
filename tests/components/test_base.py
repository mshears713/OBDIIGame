"""
Unit Tests for Base Component Class

Tests the abstract Component base class and its serialization methods.
"""

import pytest
from src.components.base import Component


# Create a concrete test component for testing
class TestHealthComponent(Component):
    """Simple test component with health data."""

    def __init__(self, current_hp: int = 100, max_hp: int = 100):
        super().__init__()
        self.current_hp = current_hp
        self.max_hp = max_hp


class TestComponent:
    """Test suite for Component base class."""

    def test_component_type_auto_set(self):
        """Test that component_type is automatically set from class name."""
        health = TestHealthComponent()
        assert health.component_type == "TestHealthComponent"

    def test_component_initialization_with_params(self):
        """Test component initialization with custom parameters."""
        health = TestHealthComponent(current_hp=50, max_hp=100)
        assert health.current_hp == 50
        assert health.max_hp == 100

    def test_to_dict_serialization(self):
        """Test serializing component to dictionary."""
        health = TestHealthComponent(current_hp=75, max_hp=100)
        data = health.to_dict()

        assert data['component_type'] == 'TestHealthComponent'
        assert data['current_hp'] == 75
        assert data['max_hp'] == 100

    def test_from_dict_deserialization(self):
        """Test deserializing component from dictionary."""
        data = {'current_hp': 60, 'max_hp': 100}
        health = TestHealthComponent.from_dict(data)

        assert health.current_hp == 60
        assert health.max_hp == 100
        assert health.component_type == 'TestHealthComponent'

    def test_from_dict_ignores_component_type(self):
        """Test that from_dict ignores component_type field if present."""
        data = {
            'component_type': 'SomeOtherComponent',  # Should be ignored
            'current_hp': 80,
            'max_hp': 100
        }
        health = TestHealthComponent.from_dict(data)

        # component_type should be set correctly based on class, not data
        assert health.component_type == 'TestHealthComponent'
        assert health.current_hp == 80

    def test_repr_output(self):
        """Test string representation of component."""
        health = TestHealthComponent(current_hp=90, max_hp=100)
        repr_str = repr(health)

        assert 'TestHealthComponent' in repr_str
        assert 'current_hp=90' in repr_str
        assert 'max_hp=100' in repr_str

    def test_serialization_roundtrip(self):
        """Test that serialize -> deserialize preserves data."""
        original = TestHealthComponent(current_hp=45, max_hp=100)

        # Serialize
        data = original.to_dict()

        # Deserialize
        restored = TestHealthComponent.from_dict(data)

        assert restored.current_hp == original.current_hp
        assert restored.max_hp == original.max_hp
        assert restored.component_type == original.component_type
