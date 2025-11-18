"""
Unit tests for InputComponent

Tests cover:
- Initialization
- Enabling/disabling input
- Input state checking
- Serialization and deserialization
"""

import pytest
from src.components.input import InputComponent


class TestInputComponent:
    """Test suite for InputComponent."""

    def test_initialization_with_default(self):
        """Test default initialization (accepts input)."""
        input_comp = InputComponent()

        assert input_comp.accepts_input is True
        assert input_comp.can_accept_input() is True

    def test_initialization_disabled(self):
        """Test initialization with input disabled."""
        input_comp = InputComponent(accepts_input=False)

        assert input_comp.accepts_input is False
        assert input_comp.can_accept_input() is False

    def test_enable_input(self):
        """Test enabling input."""
        input_comp = InputComponent(accepts_input=False)

        input_comp.enable_input()

        assert input_comp.accepts_input is True
        assert input_comp.can_accept_input() is True

    def test_disable_input(self):
        """Test disabling input."""
        input_comp = InputComponent(accepts_input=True)

        input_comp.disable_input()

        assert input_comp.accepts_input is False
        assert input_comp.can_accept_input() is False

    def test_can_accept_input_true(self):
        """Test can_accept_input when enabled."""
        input_comp = InputComponent(accepts_input=True)

        assert input_comp.can_accept_input() is True

    def test_can_accept_input_false(self):
        """Test can_accept_input when disabled."""
        input_comp = InputComponent(accepts_input=False)

        assert input_comp.can_accept_input() is False

    def test_toggle_input(self):
        """Test toggling input on and off."""
        input_comp = InputComponent()

        # Start enabled
        assert input_comp.can_accept_input() is True

        # Disable
        input_comp.disable_input()
        assert input_comp.can_accept_input() is False

        # Enable
        input_comp.enable_input()
        assert input_comp.can_accept_input() is True

    def test_to_dict(self):
        """Test serialization to dictionary."""
        input_comp = InputComponent(accepts_input=True)

        data = input_comp.to_dict()

        assert data['component_type'] == 'InputComponent'
        assert data['accepts_input'] is True

    def test_to_dict_disabled(self):
        """Test serialization with input disabled."""
        input_comp = InputComponent(accepts_input=False)

        data = input_comp.to_dict()

        assert data['component_type'] == 'InputComponent'
        assert data['accepts_input'] is False

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {
            'component_type': 'InputComponent',
            'accepts_input': True
        }

        input_comp = InputComponent.from_dict(data)

        assert input_comp.accepts_input is True

    def test_from_dict_disabled(self):
        """Test deserialization with input disabled."""
        data = {
            'component_type': 'InputComponent',
            'accepts_input': False
        }

        input_comp = InputComponent.from_dict(data)

        assert input_comp.accepts_input is False

    def test_from_dict_with_default(self):
        """Test deserialization with missing field."""
        data = {'component_type': 'InputComponent'}

        input_comp = InputComponent.from_dict(data)

        assert input_comp.accepts_input is True  # Default

    def test_serialization_round_trip(self):
        """Test that serialization preserves state."""
        original = InputComponent(accepts_input=False)

        data = original.to_dict()
        restored = InputComponent.from_dict(data)

        assert restored.accepts_input == original.accepts_input

    def test_cutscene_scenario(self):
        """Test disabling input during cutscene."""
        player_input = InputComponent()

        # Normal gameplay
        assert player_input.can_accept_input() is True

        # Cutscene starts - disable input
        player_input.disable_input()
        assert player_input.can_accept_input() is False

        # Cutscene ends - re-enable input
        player_input.enable_input()
        assert player_input.can_accept_input() is True

    def test_stun_effect_scenario(self):
        """Test disabling input during stun."""
        player_input = InputComponent()

        # Player is stunned
        player_input.disable_input()
        assert player_input.can_accept_input() is False

        # Stun wears off
        player_input.enable_input()
        assert player_input.can_accept_input() is True

    def test_turn_based_scenario(self):
        """Test disabling input when not player's turn."""
        player_input = InputComponent()

        # Player's turn
        assert player_input.can_accept_input() is True

        # Enemy's turn - disable
        player_input.disable_input()
        assert player_input.can_accept_input() is False

        # Player's turn again
        player_input.enable_input()
        assert player_input.can_accept_input() is True

    def test_multiple_enable_disable_cycles(self):
        """Test multiple enable/disable cycles."""
        input_comp = InputComponent()

        for _ in range(5):
            input_comp.disable_input()
            assert input_comp.can_accept_input() is False

            input_comp.enable_input()
            assert input_comp.can_accept_input() is True

    def test_marker_component_usage(self):
        """Test usage as a marker component."""
        # InputComponent acts as a tag to identify player-controlled entities
        player_input = InputComponent()

        # Component exists = player-controlled
        assert player_input is not None
        assert player_input.can_accept_input() is True
