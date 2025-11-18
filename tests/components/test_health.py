"""
Tests for HealthComponent

Educational Note:
    These tests verify health mechanics work correctly including:
    - Damage application
    - Healing
    - Death detection
    - HP capping (min/max bounds)
"""

import pytest
from src.components.health import HealthComponent


class TestHealthComponent:
    """Test HealthComponent functionality."""

    def test_initialization(self):
        """Test health component creates with correct values."""
        health = HealthComponent(current_hp=75, max_hp=100)
        assert health.current_hp == 75
        assert health.max_hp == 100
        assert health.is_alive()

    def test_initialization_defaults(self):
        """Test default HP values."""
        health = HealthComponent()
        assert health.current_hp == 100
        assert health.max_hp == 100

    def test_take_damage(self):
        """Test damage reduces HP."""
        health = HealthComponent(current_hp=100, max_hp=100)
        actual = health.take_damage(30)

        assert actual == 30
        assert health.current_hp == 70
        assert health.is_alive()

    def test_take_fatal_damage(self):
        """Test damage that kills entity."""
        health = HealthComponent(current_hp=50, max_hp=100)
        actual = health.take_damage(60)

        assert actual == 50  # Only dealt remaining HP
        assert health.current_hp == 0
        assert health.is_dead
        assert not health.is_alive()

    def test_take_damage_when_dead(self):
        """Test damage to already dead entity does nothing."""
        health = HealthComponent(current_hp=0, max_hp=100)
        actual = health.take_damage(50)

        assert actual == 0
        assert health.current_hp == 0

    def test_heal(self):
        """Test healing restores HP."""
        health = HealthComponent(current_hp=50, max_hp=100)
        actual = health.heal(30)

        assert actual == 30
        assert health.current_hp == 80

    def test_heal_over_max(self):
        """Test healing doesn't exceed max HP."""
        health = HealthComponent(current_hp=90, max_hp=100)
        actual = health.heal(50)

        assert actual == 10  # Only healed to max
        assert health.current_hp == 100

    def test_heal_when_dead(self):
        """Test healing dead entity does nothing."""
        health = HealthComponent(current_hp=0, max_hp=100)
        actual = health.heal(50)

        assert actual == 0
        assert health.current_hp == 0
        assert health.is_dead

    def test_get_hp_percentage(self):
        """Test HP percentage calculation."""
        health = HealthComponent(current_hp=75, max_hp=100)
        assert health.get_hp_percentage() == 0.75

        health.take_damage(25)
        assert health.get_hp_percentage() == 0.50

    def test_set_max_hp_increase(self):
        """Test increasing max HP."""
        health = HealthComponent(current_hp=80, max_hp=100)
        health.set_max_hp(120)

        assert health.max_hp == 120
        assert health.current_hp == 80  # Current unchanged

    def test_set_max_hp_decrease(self):
        """Test decreasing max HP caps current HP."""
        health = HealthComponent(current_hp=80, max_hp=100)
        health.set_max_hp(70)

        assert health.max_hp == 70
        assert health.current_hp == 70  # Capped to new max

    def test_restore_to_full(self):
        """Test full HP restoration."""
        health = HealthComponent(current_hp=30, max_hp=100)
        health.restore_to_full()

        assert health.current_hp == 100
        assert health.is_alive()

    def test_serialization(self):
        """Test health component serialization."""
        health = HealthComponent(current_hp=75, max_hp=100)
        data = health.to_dict()

        assert data['current_hp'] == 75
        assert data['max_hp'] == 100
        assert data['component_type'] == 'HealthComponent'

    def test_deserialization(self):
        """Test health component deserialization."""
        data = {'current_hp': 60, 'max_hp': 120}
        health = HealthComponent.from_dict(data)

        assert health.current_hp == 60
        assert health.max_hp == 120


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
