"""
Unit Tests for PositionComponent

Tests position storage, movement, and distance calculations.
"""

import pytest
from src.components.position import PositionComponent


class TestPositionComponent:
    """Test suite for PositionComponent."""

    def test_initialization_default(self):
        """Test creating position with default coordinates (0, 0)."""
        pos = PositionComponent()
        assert pos.x == 0
        assert pos.y == 0
        assert pos.component_type == "PositionComponent"

    def test_initialization_with_coordinates(self):
        """Test creating position with specific coordinates."""
        pos = PositionComponent(x=15, y=25)
        assert pos.x == 15
        assert pos.y == 25

    def test_get_position(self):
        """Test retrieving position as tuple."""
        pos = PositionComponent(x=7, y=13)
        coords = pos.get_position()
        assert coords == (7, 13)
        # Test unpacking
        x, y = pos.get_position()
        assert x == 7
        assert y == 13

    def test_set_position(self):
        """Test setting position to new coordinates."""
        pos = PositionComponent(x=5, y=5)
        pos.set_position(20, 30)
        assert pos.x == 20
        assert pos.y == 30

    def test_move_right(self):
        """Test moving entity to the right."""
        pos = PositionComponent(x=10, y=10)
        pos.move(dx=3, dy=0)
        assert pos.x == 13
        assert pos.y == 10

    def test_move_left(self):
        """Test moving entity to the left."""
        pos = PositionComponent(x=10, y=10)
        pos.move(dx=-2, dy=0)
        assert pos.x == 8
        assert pos.y == 10

    def test_move_down(self):
        """Test moving entity down."""
        pos = PositionComponent(x=10, y=10)
        pos.move(dx=0, dy=4)
        assert pos.x == 10
        assert pos.y == 14

    def test_move_up(self):
        """Test moving entity up."""
        pos = PositionComponent(x=10, y=10)
        pos.move(dx=0, dy=-5)
        assert pos.x == 10
        assert pos.y == 5

    def test_move_diagonal(self):
        """Test moving entity diagonally."""
        pos = PositionComponent(x=0, y=0)
        pos.move(dx=3, dy=4)
        assert pos.x == 3
        assert pos.y == 4

    def test_distance_to_same_position(self):
        """Test distance to same position is zero."""
        pos1 = PositionComponent(x=5, y=5)
        pos2 = PositionComponent(x=5, y=5)
        assert pos1.distance_to(pos2) == 0.0

    def test_distance_to_horizontal(self):
        """Test distance calculation for horizontal separation."""
        pos1 = PositionComponent(x=0, y=0)
        pos2 = PositionComponent(x=5, y=0)
        assert pos1.distance_to(pos2) == 5.0

    def test_distance_to_vertical(self):
        """Test distance calculation for vertical separation."""
        pos1 = PositionComponent(x=0, y=0)
        pos2 = PositionComponent(x=0, y=8)
        assert pos1.distance_to(pos2) == 8.0

    def test_distance_to_diagonal(self):
        """Test distance calculation for diagonal separation (3-4-5 triangle)."""
        pos1 = PositionComponent(x=0, y=0)
        pos2 = PositionComponent(x=3, y=4)
        assert pos1.distance_to(pos2) == 5.0

    def test_manhattan_distance_same_position(self):
        """Test Manhattan distance to same position is zero."""
        pos1 = PositionComponent(x=5, y=5)
        pos2 = PositionComponent(x=5, y=5)
        assert pos1.manhattan_distance_to(pos2) == 0

    def test_manhattan_distance_horizontal(self):
        """Test Manhattan distance for horizontal separation."""
        pos1 = PositionComponent(x=0, y=0)
        pos2 = PositionComponent(x=7, y=0)
        assert pos1.manhattan_distance_to(pos2) == 7

    def test_manhattan_distance_vertical(self):
        """Test Manhattan distance for vertical separation."""
        pos1 = PositionComponent(x=0, y=0)
        pos2 = PositionComponent(x=0, y=6)
        assert pos1.manhattan_distance_to(pos2) == 6

    def test_manhattan_distance_diagonal(self):
        """Test Manhattan distance for diagonal separation."""
        pos1 = PositionComponent(x=0, y=0)
        pos2 = PositionComponent(x=3, y=4)
        # Manhattan: |3-0| + |4-0| = 7
        assert pos1.manhattan_distance_to(pos2) == 7

    def test_is_adjacent_to_right(self):
        """Test adjacency check for right neighbor."""
        pos1 = PositionComponent(x=5, y=5)
        pos2 = PositionComponent(x=6, y=5)
        assert pos1.is_adjacent_to(pos2) is True

    def test_is_adjacent_to_left(self):
        """Test adjacency check for left neighbor."""
        pos1 = PositionComponent(x=5, y=5)
        pos2 = PositionComponent(x=4, y=5)
        assert pos1.is_adjacent_to(pos2) is True

    def test_is_adjacent_to_above(self):
        """Test adjacency check for neighbor above."""
        pos1 = PositionComponent(x=5, y=5)
        pos2 = PositionComponent(x=5, y=4)
        assert pos1.is_adjacent_to(pos2) is True

    def test_is_adjacent_to_below(self):
        """Test adjacency check for neighbor below."""
        pos1 = PositionComponent(x=5, y=5)
        pos2 = PositionComponent(x=5, y=6)
        assert pos1.is_adjacent_to(pos2) is True

    def test_is_adjacent_to_diagonal_with_diagonal_true(self):
        """Test adjacency check for diagonal neighbor (include_diagonal=True)."""
        pos1 = PositionComponent(x=5, y=5)
        pos2 = PositionComponent(x=6, y=6)
        assert pos1.is_adjacent_to(pos2, include_diagonal=True) is True

    def test_is_adjacent_to_diagonal_with_diagonal_false(self):
        """Test adjacency check for diagonal neighbor (include_diagonal=False)."""
        pos1 = PositionComponent(x=5, y=5)
        pos2 = PositionComponent(x=6, y=6)
        assert pos1.is_adjacent_to(pos2, include_diagonal=False) is False

    def test_is_adjacent_to_same_position(self):
        """Test adjacency to self is False."""
        pos1 = PositionComponent(x=5, y=5)
        pos2 = PositionComponent(x=5, y=5)
        assert pos1.is_adjacent_to(pos2) is False

    def test_is_adjacent_to_far_position(self):
        """Test adjacency to far position is False."""
        pos1 = PositionComponent(x=5, y=5)
        pos2 = PositionComponent(x=10, y=10)
        assert pos1.is_adjacent_to(pos2) is False

    def test_equality_same_coordinates(self):
        """Test that positions with same coordinates are equal."""
        pos1 = PositionComponent(x=7, y=13)
        pos2 = PositionComponent(x=7, y=13)
        assert pos1 == pos2

    def test_equality_different_coordinates(self):
        """Test that positions with different coordinates are not equal."""
        pos1 = PositionComponent(x=5, y=10)
        pos2 = PositionComponent(x=6, y=10)
        assert pos1 != pos2

    def test_equality_with_non_position(self):
        """Test equality comparison with non-PositionComponent object."""
        pos = PositionComponent(x=5, y=5)
        assert pos != "not a position"
        assert pos != 42
        assert pos != None

    def test_to_dict(self):
        """Test serialization to dictionary."""
        pos = PositionComponent(x=12, y=18)
        data = pos.to_dict()

        assert data['component_type'] == 'PositionComponent'
        assert data['x'] == 12
        assert data['y'] == 18

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {'x': 25, 'y': 35}
        pos = PositionComponent.from_dict(data)

        assert pos.x == 25
        assert pos.y == 35

    def test_from_dict_with_missing_values(self):
        """Test deserialization with missing values uses defaults."""
        data = {}
        pos = PositionComponent.from_dict(data)

        assert pos.x == 0
        assert pos.y == 0

    def test_serialization_roundtrip(self):
        """Test that serialize -> deserialize preserves data."""
        original = PositionComponent(x=42, y=73)

        # Serialize
        data = original.to_dict()

        # Deserialize
        restored = PositionComponent.from_dict(data)

        assert restored.x == original.x
        assert restored.y == original.y
        assert restored == original
