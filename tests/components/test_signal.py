"""
Tests for SignalComponent

Educational Note:
    These tests demonstrate signal component functionality and serve as
    documentation for how the signal crafting system works.
"""

import pytest
from src.components.signal import SignalComponent


class TestSignalComponentBasics:
    """Test basic signal component initialization and properties."""

    def test_initialization_default(self):
        """Test default initialization creates empty signal inventory."""
        signal = SignalComponent()

        assert signal.component_type == "SignalComponent"
        assert signal.get_total_signal_count() == 0
        assert signal.get_signal_types() == []
        assert signal.max_signal_types == 0  # Unlimited
        assert signal.max_per_signal == 999

    def test_initialization_with_limits(self):
        """Test initialization with capacity limits."""
        signal = SignalComponent(max_signal_types=5, max_per_signal=10)

        assert signal.max_signal_types == 5
        assert signal.max_per_signal == 10


class TestAddSignal:
    """Test adding signals to the component."""

    def test_add_single_signal(self):
        """Test adding a single signal."""
        signal = SignalComponent()

        added = signal.add_signal("sensor_reading", 1)

        assert added == 1
        assert signal.get_signal_count("sensor_reading") == 1
        assert signal.has_signal("sensor_reading", 1) is True

    def test_add_multiple_signals(self):
        """Test adding multiple signals at once."""
        signal = SignalComponent()

        added = signal.add_signal("dtc_code", 5)

        assert added == 5
        assert signal.get_signal_count("dtc_code") == 5

    def test_add_to_existing_signal(self):
        """Test adding to an existing signal type increases count."""
        signal = SignalComponent()

        signal.add_signal("ecu_query", 3)
        added = signal.add_signal("ecu_query", 2)

        assert added == 2
        assert signal.get_signal_count("ecu_query") == 5

    def test_add_different_signal_types(self):
        """Test adding multiple different signal types."""
        signal = SignalComponent()

        signal.add_signal("sensor_reading", 2)
        signal.add_signal("dtc_code", 3)
        signal.add_signal("corrupted_packet", 1)

        assert len(signal.get_signal_types()) == 3
        assert signal.get_total_signal_count() == 6

    def test_add_signal_respects_per_signal_limit(self):
        """Test that adding signals respects max_per_signal limit."""
        signal = SignalComponent(max_per_signal=10)

        # Add up to limit
        added = signal.add_signal("sensor_reading", 8)
        assert added == 8

        # Try to add more than limit allows
        added = signal.add_signal("sensor_reading", 5)
        assert added == 2  # Only 2 can be added to reach max of 10
        assert signal.get_signal_count("sensor_reading") == 10

    def test_add_signal_respects_type_limit(self):
        """Test that adding new signal types respects max_signal_types limit."""
        signal = SignalComponent(max_signal_types=2)

        # Add two different types
        signal.add_signal("type_a", 1)
        signal.add_signal("type_b", 1)
        assert len(signal.get_signal_types()) == 2

        # Try to add a third type
        added = signal.add_signal("type_c", 1)
        assert added == 0  # Can't add new type - at limit
        assert len(signal.get_signal_types()) == 2

    def test_add_zero_or_negative_quantity(self):
        """Test that adding zero or negative quantities does nothing."""
        signal = SignalComponent()

        added = signal.add_signal("sensor_reading", 0)
        assert added == 0

        added = signal.add_signal("sensor_reading", -5)
        assert added == 0

        assert signal.get_signal_count("sensor_reading") == 0


class TestRemoveSignal:
    """Test removing signals from the component."""

    def test_remove_signal(self):
        """Test removing signals decreases count."""
        signal = SignalComponent()
        signal.add_signal("dtc_code", 5)

        removed = signal.remove_signal("dtc_code", 2)

        assert removed == 2
        assert signal.get_signal_count("dtc_code") == 3

    def test_remove_all_signals_of_type(self):
        """Test removing all signals of a type cleans up the entry."""
        signal = SignalComponent()
        signal.add_signal("ecu_query", 3)

        removed = signal.remove_signal("ecu_query", 3)

        assert removed == 3
        assert signal.get_signal_count("ecu_query") == 0
        assert "ecu_query" not in signal.get_signal_types()

    def test_remove_more_than_available(self):
        """Test removing more than available only removes what exists."""
        signal = SignalComponent()
        signal.add_signal("sensor_reading", 5)

        removed = signal.remove_signal("sensor_reading", 10)

        assert removed == 5  # Only removed available amount
        assert signal.get_signal_count("sensor_reading") == 0

    def test_remove_nonexistent_signal(self):
        """Test removing a signal type that doesn't exist does nothing."""
        signal = SignalComponent()

        removed = signal.remove_signal("nonexistent", 5)

        assert removed == 0

    def test_remove_zero_or_negative_quantity(self):
        """Test that removing zero or negative quantities does nothing."""
        signal = SignalComponent()
        signal.add_signal("dtc_code", 5)

        removed = signal.remove_signal("dtc_code", 0)
        assert removed == 0

        removed = signal.remove_signal("dtc_code", -3)
        assert removed == 0

        assert signal.get_signal_count("dtc_code") == 5


class TestSignalQueries:
    """Test querying signal information."""

    def test_has_signal_returns_true_when_sufficient(self):
        """Test has_signal returns True when quantity is sufficient."""
        signal = SignalComponent()
        signal.add_signal("sensor_reading", 5)

        assert signal.has_signal("sensor_reading", 1) is True
        assert signal.has_signal("sensor_reading", 5) is True

    def test_has_signal_returns_false_when_insufficient(self):
        """Test has_signal returns False when quantity is insufficient."""
        signal = SignalComponent()
        signal.add_signal("sensor_reading", 3)

        assert signal.has_signal("sensor_reading", 4) is False
        assert signal.has_signal("sensor_reading", 10) is False

    def test_has_signal_returns_false_for_nonexistent(self):
        """Test has_signal returns False for nonexistent signal types."""
        signal = SignalComponent()

        assert signal.has_signal("nonexistent", 1) is False

    def test_get_signal_count_for_existing_signal(self):
        """Test getting count for an existing signal."""
        signal = SignalComponent()
        signal.add_signal("dtc_code", 7)

        assert signal.get_signal_count("dtc_code") == 7

    def test_get_signal_count_for_nonexistent_signal(self):
        """Test getting count for nonexistent signal returns 0."""
        signal = SignalComponent()

        assert signal.get_signal_count("nonexistent") == 0

    def test_get_all_signals(self):
        """Test getting all signals returns correct dictionary."""
        signal = SignalComponent()
        signal.add_signal("type_a", 3)
        signal.add_signal("type_b", 2)
        signal.add_signal("type_c", 5)

        all_signals = signal.get_all_signals()

        assert all_signals == {
            "type_a": 3,
            "type_b": 2,
            "type_c": 5
        }

    def test_get_all_signals_returns_copy(self):
        """Test that get_all_signals returns a copy, not reference."""
        signal = SignalComponent()
        signal.add_signal("sensor_reading", 5)

        all_signals = signal.get_all_signals()
        all_signals["sensor_reading"] = 999  # Modify the returned dict

        # Original should be unchanged
        assert signal.get_signal_count("sensor_reading") == 5

    def test_get_signal_types(self):
        """Test getting list of signal types."""
        signal = SignalComponent()
        signal.add_signal("type_a", 1)
        signal.add_signal("type_b", 1)
        signal.add_signal("type_c", 1)

        types = signal.get_signal_types()

        assert len(types) == 3
        assert "type_a" in types
        assert "type_b" in types
        assert "type_c" in types

    def test_get_total_signal_count(self):
        """Test getting total signal count across all types."""
        signal = SignalComponent()
        signal.add_signal("type_a", 5)
        signal.add_signal("type_b", 3)
        signal.add_signal("type_c", 2)

        assert signal.get_total_signal_count() == 10

    def test_get_total_signal_count_empty(self):
        """Test total count is 0 when no signals."""
        signal = SignalComponent()

        assert signal.get_total_signal_count() == 0


class TestSignalOperations:
    """Test advanced signal operations."""

    def test_clear_signals(self):
        """Test clearing all signals."""
        signal = SignalComponent()
        signal.add_signal("type_a", 5)
        signal.add_signal("type_b", 3)

        signal.clear_signals()

        assert signal.get_total_signal_count() == 0
        assert signal.get_signal_types() == []

    def test_transfer_signal_success(self):
        """Test successful signal transfer between components."""
        source = SignalComponent()
        target = SignalComponent()

        source.add_signal("sensor_reading", 10)

        transferred = source.transfer_signal("sensor_reading", 5, target)

        assert transferred == 5
        assert source.get_signal_count("sensor_reading") == 5
        assert target.get_signal_count("sensor_reading") == 5

    def test_transfer_signal_insufficient_source(self):
        """Test transfer when source has fewer signals than requested."""
        source = SignalComponent()
        target = SignalComponent()

        source.add_signal("dtc_code", 3)

        transferred = source.transfer_signal("dtc_code", 10, target)

        assert transferred == 3  # Only transferred available amount
        assert source.get_signal_count("dtc_code") == 0
        assert target.get_signal_count("dtc_code") == 3

    def test_transfer_signal_respects_target_limit(self):
        """Test transfer respects target capacity limits."""
        source = SignalComponent()
        target = SignalComponent(max_per_signal=5)

        source.add_signal("sensor_reading", 10)
        target.add_signal("sensor_reading", 3)  # Already has 3

        transferred = source.transfer_signal("sensor_reading", 10, target)

        assert transferred == 2  # Only 2 can be added to reach target max of 5
        assert source.get_signal_count("sensor_reading") == 8
        assert target.get_signal_count("sensor_reading") == 5

    def test_transfer_nonexistent_signal(self):
        """Test transferring a signal that doesn't exist."""
        source = SignalComponent()
        target = SignalComponent()

        transferred = source.transfer_signal("nonexistent", 5, target)

        assert transferred == 0


class TestRecipeValidation:
    """Test recipe requirement validation."""

    def test_can_afford_simple_recipe(self):
        """Test checking if signals meet simple recipe requirements."""
        signal = SignalComponent()
        signal.add_signal("sensor_reading", 5)
        signal.add_signal("error_correction", 2)

        recipe_inputs = [
            {"signal_type": "sensor_reading", "quantity": 3, "consumed": True},
            {"signal_type": "error_correction", "quantity": 1, "consumed": False}
        ]

        assert signal.can_afford_recipe(recipe_inputs) is True

    def test_can_afford_recipe_exact_quantities(self):
        """Test with exact quantities required."""
        signal = SignalComponent()
        signal.add_signal("dtc_code", 2)
        signal.add_signal("corrupted_packet", 1)

        recipe_inputs = [
            {"signal_type": "dtc_code", "quantity": 2, "consumed": True},
            {"signal_type": "corrupted_packet", "quantity": 1, "consumed": True}
        ]

        assert signal.can_afford_recipe(recipe_inputs) is True

    def test_cannot_afford_recipe_insufficient_quantity(self):
        """Test recipe fails when insufficient quantity."""
        signal = SignalComponent()
        signal.add_signal("sensor_reading", 2)

        recipe_inputs = [
            {"signal_type": "sensor_reading", "quantity": 5, "consumed": True}
        ]

        assert signal.can_afford_recipe(recipe_inputs) is False

    def test_cannot_afford_recipe_missing_signal_type(self):
        """Test recipe fails when signal type is missing."""
        signal = SignalComponent()
        signal.add_signal("sensor_reading", 10)

        recipe_inputs = [
            {"signal_type": "sensor_reading", "quantity": 2, "consumed": True},
            {"signal_type": "missing_type", "quantity": 1, "consumed": True}
        ]

        assert signal.can_afford_recipe(recipe_inputs) is False

    def test_can_afford_empty_recipe(self):
        """Test that empty recipe requirements are always affordable."""
        signal = SignalComponent()

        recipe_inputs = []

        assert signal.can_afford_recipe(recipe_inputs) is True

    def test_can_afford_recipe_default_quantity(self):
        """Test recipe with default quantity (1 if not specified)."""
        signal = SignalComponent()
        signal.add_signal("ecu_query", 3)

        recipe_inputs = [
            {"signal_type": "ecu_query", "consumed": True}  # No quantity specified
        ]

        assert signal.can_afford_recipe(recipe_inputs) is True


class TestSerialization:
    """Test signal component serialization for save/load."""

    def test_to_dict_empty(self):
        """Test serializing empty signal component."""
        signal = SignalComponent()

        data = signal.to_dict()

        assert data['component_type'] == 'SignalComponent'
        assert data['signals'] == {}
        assert data['max_signal_types'] == 0
        assert data['max_per_signal'] == 999

    def test_to_dict_with_signals(self):
        """Test serializing signal component with signals."""
        signal = SignalComponent(max_signal_types=10, max_per_signal=50)
        signal.add_signal("sensor_reading", 5)
        signal.add_signal("dtc_code", 3)

        data = signal.to_dict()

        assert data['signals'] == {
            "sensor_reading": 5,
            "dtc_code": 3
        }
        assert data['max_signal_types'] == 10
        assert data['max_per_signal'] == 50

    def test_from_dict_empty(self):
        """Test deserializing empty signal component."""
        data = {
            'component_type': 'SignalComponent',
            'signals': {},
            'max_signal_types': 0,
            'max_per_signal': 999
        }

        signal = SignalComponent.from_dict(data)

        assert signal.get_total_signal_count() == 0
        assert signal.max_signal_types == 0
        assert signal.max_per_signal == 999

    def test_from_dict_with_signals(self):
        """Test deserializing signal component with signals."""
        data = {
            'signals': {
                "sensor_reading": 7,
                "ecu_query": 3,
                "corrupted_packet": 2
            },
            'max_signal_types': 5,
            'max_per_signal': 20
        }

        signal = SignalComponent.from_dict(data)

        assert signal.get_signal_count("sensor_reading") == 7
        assert signal.get_signal_count("ecu_query") == 3
        assert signal.get_signal_count("corrupted_packet") == 2
        assert signal.get_total_signal_count() == 12
        assert signal.max_signal_types == 5
        assert signal.max_per_signal == 20

    def test_roundtrip_serialization(self):
        """Test that serialization and deserialization preserve data."""
        original = SignalComponent(max_signal_types=8, max_per_signal=30)
        original.add_signal("type_a", 5)
        original.add_signal("type_b", 3)
        original.add_signal("type_c", 7)

        data = original.to_dict()
        restored = SignalComponent.from_dict(data)

        assert original.get_all_signals() == restored.get_all_signals()
        assert original.max_signal_types == restored.max_signal_types
        assert original.max_per_signal == restored.max_per_signal


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_large_quantities(self):
        """Test handling very large signal quantities."""
        signal = SignalComponent(max_per_signal=0)  # Unlimited

        signal.add_signal("sensor_reading", 1_000_000)

        assert signal.get_signal_count("sensor_reading") == 1_000_000

    def test_many_different_signal_types(self):
        """Test handling many different signal types."""
        signal = SignalComponent()

        # Add 100 different signal types
        for i in range(100):
            signal.add_signal(f"signal_type_{i}", 1)

        assert len(signal.get_signal_types()) == 100
        assert signal.get_total_signal_count() == 100

    def test_signal_type_with_special_characters(self):
        """Test signal types can have special characters."""
        signal = SignalComponent()

        signal.add_signal("signal-with-dashes", 1)
        signal.add_signal("signal_with_underscores", 1)
        signal.add_signal("signal.with.dots", 1)

        assert len(signal.get_signal_types()) == 3

    def test_operations_on_empty_component(self):
        """Test that operations on empty component don't raise errors."""
        signal = SignalComponent()

        # All these should work without errors
        assert signal.get_signal_count("anything") == 0
        assert signal.has_signal("anything") is False
        assert signal.get_all_signals() == {}
        assert signal.get_signal_types() == []
        assert signal.get_total_signal_count() == 0

        removed = signal.remove_signal("anything", 5)
        assert removed == 0

        signal.clear_signals()  # Should not raise error
