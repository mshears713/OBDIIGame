"""
Unit tests for NameComponent

Tests cover:
- Initialization with default and custom values
- Getting and setting names
- Getting and setting descriptions
- Serialization and deserialization
"""

import pytest
from src.components.name import NameComponent


class TestNameComponent:
    """Test suite for NameComponent."""

    def test_initialization_with_defaults(self):
        """Test default initialization."""
        name_comp = NameComponent()

        assert name_comp.name == "Unknown"
        assert name_comp.description == ""

    def test_initialization_with_custom_values(self):
        """Test initialization with custom name and description."""
        name_comp = NameComponent(
            name="Test Entity",
            description="A test entity for testing purposes"
        )

        assert name_comp.name == "Test Entity"
        assert name_comp.description == "A test entity for testing purposes"

    def test_get_name(self):
        """Test get_name method."""
        name_comp = NameComponent(name="Player")
        assert name_comp.get_name() == "Player"

    def test_set_name(self):
        """Test set_name method."""
        name_comp = NameComponent(name="Old Name")
        name_comp.set_name("New Name")

        assert name_comp.name == "New Name"
        assert name_comp.get_name() == "New Name"

    def test_get_description(self):
        """Test get_description method."""
        desc = "A brave warrior"
        name_comp = NameComponent(name="Hero", description=desc)

        assert name_comp.get_description() == desc

    def test_set_description(self):
        """Test set_description method."""
        name_comp = NameComponent(name="Item")
        name_comp.set_description("A magical sword")

        assert name_comp.description == "A magical sword"
        assert name_comp.get_description() == "A magical sword"

    def test_name_change_scenarios(self):
        """Test various name change scenarios."""
        name_comp = NameComponent(name="???")

        # Identification
        name_comp.set_name("Potion of Healing")
        assert name_comp.get_name() == "Potion of Healing"

        # Shapeshifting
        name_comp.set_name("Doppelganger")
        assert name_comp.get_name() == "Doppelganger"

    def test_empty_name(self):
        """Test empty name handling."""
        name_comp = NameComponent(name="")

        assert name_comp.get_name() == ""

    def test_long_name(self):
        """Test long name handling."""
        long_name = "A" * 100
        name_comp = NameComponent(name=long_name)

        assert name_comp.get_name() == long_name
        assert len(name_comp.name) == 100

    def test_to_dict(self):
        """Test serialization to dictionary."""
        name_comp = NameComponent(
            name="Goblin",
            description="A small, green creature"
        )

        data = name_comp.to_dict()

        assert data['component_type'] == 'NameComponent'
        assert data['name'] == "Goblin"
        assert data['description'] == "A small, green creature"

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {
            'component_type': 'NameComponent',
            'name': 'Dragon',
            'description': 'A fearsome dragon'
        }

        name_comp = NameComponent.from_dict(data)

        assert name_comp.name == "Dragon"
        assert name_comp.description == "A fearsome dragon"

    def test_from_dict_with_missing_fields(self):
        """Test deserialization with missing optional fields."""
        data = {
            'component_type': 'NameComponent'
        }

        name_comp = NameComponent.from_dict(data)

        assert name_comp.name == "Unknown"
        assert name_comp.description == ""

    def test_serialization_round_trip(self):
        """Test that serialization and deserialization preserve data."""
        original = NameComponent(
            name="Test",
            description="Test description"
        )

        data = original.to_dict()
        restored = NameComponent.from_dict(data)

        assert restored.name == original.name
        assert restored.description == original.description

    def test_special_characters_in_name(self):
        """Test names with special characters."""
        name_comp = NameComponent(name="Test-Entity_123!@#")

        assert name_comp.get_name() == "Test-Entity_123!@#"

    def test_unicode_in_name(self):
        """Test unicode characters in name."""
        name_comp = NameComponent(name="Dragon 龍")

        assert name_comp.get_name() == "Dragon 龍"

    def test_multiline_description(self):
        """Test multiline descriptions."""
        desc = "Line 1\nLine 2\nLine 3"
        name_comp = NameComponent(name="Item", description=desc)

        assert name_comp.get_description() == desc
        assert "\n" in name_comp.description
