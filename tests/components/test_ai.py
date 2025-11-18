"""
Unit tests for AIComponent

Tests cover:
- Initialization with default and custom values
- Target management
- Behavior changes
- Patrol routes
- Serialization and deserialization
"""

import pytest
from src.components.ai import AIComponent, AIBehavior


class TestAIComponent:
    """Test suite for AIComponent."""

    def test_initialization_with_defaults(self):
        """Test default initialization."""
        ai = AIComponent()

        assert ai.behavior == "wander"
        assert ai.aggro_range == 4
        assert ai.chase_range == 8
        assert ai.intelligence == "low"
        assert ai.target_entity_id is None
        assert ai.state_data == {}
        assert ai.patrol_points == []
        assert ai.patrol_index == 0

    def test_initialization_with_custom_values(self):
        """Test initialization with custom AI parameters."""
        ai = AIComponent(
            behavior="chase",
            aggro_range=6,
            chase_range=12,
            intelligence="high",
            target_entity_id=42
        )

        assert ai.behavior == "chase"
        assert ai.aggro_range == 6
        assert ai.chase_range == 12
        assert ai.intelligence == "high"
        assert ai.target_entity_id == 42

    def test_set_target(self):
        """Test setting a target."""
        ai = AIComponent()
        ai.set_target(123)

        assert ai.target_entity_id == 123
        assert ai.has_target() is True

    def test_clear_target(self):
        """Test clearing a target."""
        ai = AIComponent(target_entity_id=456)
        ai.clear_target()

        assert ai.target_entity_id is None
        assert ai.has_target() is False

    def test_has_target_true(self):
        """Test has_target when target is set."""
        ai = AIComponent()
        ai.set_target(789)

        assert ai.has_target() is True

    def test_has_target_false(self):
        """Test has_target when no target."""
        ai = AIComponent()

        assert ai.has_target() is False

    def test_set_behavior(self):
        """Test changing behavior."""
        ai = AIComponent(behavior="wander")
        ai.set_behavior("chase")

        assert ai.behavior == "chase"

    def test_behavior_change_flee_on_low_health(self):
        """Test dynamic behavior change (flee when damaged)."""
        ai = AIComponent(behavior="chase")

        # Simulate low health trigger
        ai.set_behavior("flee")

        assert ai.behavior == "flee"

    def test_set_patrol_route(self):
        """Test setting patrol route."""
        ai = AIComponent()
        route = [(10, 5), (20, 5), (20, 15), (10, 15)]
        ai.set_patrol_route(route)

        assert ai.patrol_points == route
        assert ai.patrol_index == 0

    def test_get_next_patrol_point(self):
        """Test getting next patrol point."""
        ai = AIComponent()
        route = [(10, 5), (20, 5), (20, 15)]
        ai.set_patrol_route(route)

        # First call
        point = ai.get_next_patrol_point()
        assert point == (10, 5)
        assert ai.patrol_index == 1

        # Second call
        point = ai.get_next_patrol_point()
        assert point == (20, 5)
        assert ai.patrol_index == 2

        # Third call
        point = ai.get_next_patrol_point()
        assert point == (20, 15)
        assert ai.patrol_index == 0  # Wraps around

    def test_get_next_patrol_point_cycles(self):
        """Test that patrol points cycle correctly."""
        ai = AIComponent()
        route = [(0, 0), (10, 10)]
        ai.set_patrol_route(route)

        # Get all points in cycle
        p1 = ai.get_next_patrol_point()
        p2 = ai.get_next_patrol_point()
        p3 = ai.get_next_patrol_point()  # Should cycle back

        assert p1 == (0, 0)
        assert p2 == (10, 10)
        assert p3 == (0, 0)

    def test_get_next_patrol_point_empty_route(self):
        """Test getting patrol point with no route."""
        ai = AIComponent()

        point = ai.get_next_patrol_point()
        assert point is None

    def test_wander_behavior(self):
        """Test wander behavior configuration."""
        ai = AIComponent(behavior="wander", aggro_range=4)

        assert ai.behavior == "wander"
        assert ai.aggro_range == 4

    def test_chase_behavior(self):
        """Test chase behavior configuration."""
        ai = AIComponent(behavior="chase", chase_range=10)

        assert ai.behavior == "chase"
        assert ai.chase_range == 10

    def test_guard_behavior(self):
        """Test guard behavior configuration."""
        ai = AIComponent(behavior="guard", aggro_range=3)

        assert ai.behavior == "guard"
        assert ai.aggro_range == 3

    def test_flee_behavior(self):
        """Test flee behavior configuration."""
        ai = AIComponent(behavior="flee", chase_range=15)

        assert ai.behavior == "flee"
        assert ai.chase_range == 15

    def test_patrol_behavior(self):
        """Test patrol behavior configuration."""
        ai = AIComponent(behavior="patrol")
        ai.set_patrol_route([(0, 0), (10, 0), (10, 10), (0, 10)])

        assert ai.behavior == "patrol"
        assert len(ai.patrol_points) == 4

    def test_intelligence_levels(self):
        """Test different intelligence levels."""
        low_ai = AIComponent(intelligence="low")
        med_ai = AIComponent(intelligence="medium")
        high_ai = AIComponent(intelligence="high")

        assert low_ai.intelligence == "low"
        assert med_ai.intelligence == "medium"
        assert high_ai.intelligence == "high"

    def test_to_dict(self):
        """Test serialization to dictionary."""
        ai = AIComponent(
            behavior="chase",
            aggro_range=5,
            chase_range=10,
            intelligence="medium",
            target_entity_id=999
        )
        ai.set_patrol_route([(1, 1), (2, 2)])
        ai.state_data = {"alerted": True}

        data = ai.to_dict()

        assert data['component_type'] == 'AIComponent'
        assert data['behavior'] == "chase"
        assert data['aggro_range'] == 5
        assert data['chase_range'] == 10
        assert data['intelligence'] == "medium"
        assert data['target_entity_id'] == 999
        assert data['patrol_points'] == [(1, 1), (2, 2)]
        assert data['patrol_index'] == 0
        assert data['state_data'] == {"alerted": True}

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {
            'component_type': 'AIComponent',
            'behavior': 'guard',
            'aggro_range': 3,
            'chase_range': 6,
            'intelligence': 'high',
            'target_entity_id': 123,
            'patrol_points': [(5, 5), (10, 10)],
            'patrol_index': 1,
            'state_data': {'mode': 'alert'}
        }

        ai = AIComponent.from_dict(data)

        assert ai.behavior == "guard"
        assert ai.aggro_range == 3
        assert ai.chase_range == 6
        assert ai.intelligence == "high"
        assert ai.target_entity_id == 123
        assert ai.patrol_points == [(5, 5), (10, 10)]
        assert ai.patrol_index == 1
        assert ai.state_data == {'mode': 'alert'}

    def test_from_dict_with_defaults(self):
        """Test deserialization with missing fields uses defaults."""
        data = {'component_type': 'AIComponent'}

        ai = AIComponent.from_dict(data)

        assert ai.behavior == "wander"
        assert ai.aggro_range == 4
        assert ai.chase_range == 8
        assert ai.intelligence == "low"
        assert ai.target_entity_id is None
        assert ai.patrol_points == []
        assert ai.patrol_index == 0
        assert ai.state_data == {}

    def test_serialization_round_trip(self):
        """Test that serialization preserves all data."""
        original = AIComponent(
            behavior="patrol",
            aggro_range=7,
            chase_range=14,
            intelligence="medium",
            target_entity_id=555
        )
        original.set_patrol_route([(1, 1), (2, 2), (3, 3)])
        original.state_data = {"custom": "data"}
        original.patrol_index = 2

        data = original.to_dict()
        restored = AIComponent.from_dict(data)

        assert restored.behavior == original.behavior
        assert restored.aggro_range == original.aggro_range
        assert restored.chase_range == original.chase_range
        assert restored.intelligence == original.intelligence
        assert restored.target_entity_id == original.target_entity_id
        assert restored.patrol_points == original.patrol_points
        assert restored.patrol_index == original.patrol_index
        assert restored.state_data == original.state_data

    def test_target_switching(self):
        """Test switching between targets."""
        ai = AIComponent()

        ai.set_target(100)
        assert ai.target_entity_id == 100

        ai.set_target(200)
        assert ai.target_entity_id == 200

        ai.clear_target()
        assert ai.target_entity_id is None

    def test_state_data_usage(self):
        """Test using state_data for custom AI state."""
        ai = AIComponent()

        ai.state_data["last_seen_position"] = (10, 15)
        ai.state_data["turns_since_alert"] = 3
        ai.state_data["investigating"] = True

        assert ai.state_data["last_seen_position"] == (10, 15)
        assert ai.state_data["turns_since_alert"] == 3
        assert ai.state_data["investigating"] is True
