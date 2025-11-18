"""
Unit tests for CombatComponent

Tests cover:
- Initialization with default and custom values
- Damage calculation (normal and critical)
- Defense and damage reduction
- Attack range checking
- Stat modifications
- Serialization and deserialization
"""

import pytest
from src.components.combat import CombatComponent


class TestCombatComponent:
    """Test suite for CombatComponent."""

    def test_initialization_with_defaults(self):
        """Test default initialization."""
        combat = CombatComponent()

        assert combat.damage == 1
        assert combat.defense == 0
        assert combat.attack_range == 1
        assert combat.accuracy == 1.0
        assert combat.critical_chance == 0.0
        assert combat.critical_multiplier == 2.0

    def test_initialization_with_custom_values(self):
        """Test initialization with custom combat stats."""
        combat = CombatComponent(
            damage=10,
            defense=5,
            attack_range=3,
            accuracy=0.9,
            critical_chance=0.2,
            critical_multiplier=2.5
        )

        assert combat.damage == 10
        assert combat.defense == 5
        assert combat.attack_range == 3
        assert combat.accuracy == 0.9
        assert combat.critical_chance == 0.2
        assert combat.critical_multiplier == 2.5

    def test_get_damage_output_normal(self):
        """Test normal damage output calculation."""
        combat = CombatComponent(damage=10)
        damage = combat.get_damage_output(is_critical=False)

        assert damage == 10

    def test_get_damage_output_critical(self):
        """Test critical damage output calculation."""
        combat = CombatComponent(damage=10, critical_multiplier=2.0)
        damage = combat.get_damage_output(is_critical=True)

        assert damage == 20

    def test_get_damage_output_critical_custom_multiplier(self):
        """Test critical damage with custom multiplier."""
        combat = CombatComponent(damage=10, critical_multiplier=3.0)
        damage = combat.get_damage_output(is_critical=True)

        assert damage == 30

    def test_calculate_damage_reduction_partial(self):
        """Test partial damage reduction."""
        combat = CombatComponent(defense=5)
        reduced = combat.calculate_damage_reduction(10)

        assert reduced == 5

    def test_calculate_damage_reduction_minimum(self):
        """Test minimum damage of 1."""
        combat = CombatComponent(defense=10)
        reduced = combat.calculate_damage_reduction(5)

        assert reduced == 1  # At least 1 damage gets through

    def test_calculate_damage_reduction_high_defense(self):
        """Test that at least 1 damage gets through high defense."""
        combat = CombatComponent(defense=100)
        reduced = combat.calculate_damage_reduction(10)

        assert reduced == 1

    def test_calculate_damage_reduction_zero_damage(self):
        """Test zero damage edge case.

        Fixed in Phase 5 Step 48: ensure damage reduction never returns negative.
        """
        combat = CombatComponent(defense=5)
        reduced = combat.calculate_damage_reduction(0)

        # Fixed: returns 0 for zero incoming damage
        assert reduced == 0

    def test_is_melee_true(self):
        """Test melee detection."""
        combat = CombatComponent(attack_range=1)
        assert combat.is_melee() is True
        assert combat.is_ranged() is False

    def test_is_ranged_true(self):
        """Test ranged detection."""
        combat = CombatComponent(attack_range=5)
        assert combat.is_ranged() is True
        assert combat.is_melee() is False

    def test_can_attack_at_range_melee(self):
        """Test melee attack range checking."""
        combat = CombatComponent(attack_range=1)

        assert combat.can_attack_at_range(1) is True
        assert combat.can_attack_at_range(2) is False
        assert combat.can_attack_at_range(0) is False

    def test_can_attack_at_range_ranged(self):
        """Test ranged attack range checking."""
        combat = CombatComponent(attack_range=5)

        assert combat.can_attack_at_range(1) is True
        assert combat.can_attack_at_range(3) is True
        assert combat.can_attack_at_range(5) is True
        assert combat.can_attack_at_range(6) is False
        assert combat.can_attack_at_range(0) is False

    def test_modify_damage_positive(self):
        """Test increasing damage."""
        combat = CombatComponent(damage=5)
        combat.modify_damage(3)

        assert combat.damage == 8

    def test_modify_damage_negative(self):
        """Test decreasing damage."""
        combat = CombatComponent(damage=10)
        combat.modify_damage(-3)

        assert combat.damage == 7

    def test_modify_damage_below_zero(self):
        """Test that damage doesn't go below 0."""
        combat = CombatComponent(damage=5)
        combat.modify_damage(-10)

        assert combat.damage == 0

    def test_modify_defense_positive(self):
        """Test increasing defense."""
        combat = CombatComponent(defense=2)
        combat.modify_defense(5)

        assert combat.defense == 7

    def test_modify_defense_negative(self):
        """Test decreasing defense."""
        combat = CombatComponent(defense=10)
        combat.modify_defense(-3)

        assert combat.defense == 7

    def test_modify_defense_below_zero(self):
        """Test that defense doesn't go below 0."""
        combat = CombatComponent(defense=5)
        combat.modify_defense(-10)

        assert combat.defense == 0

    def test_warrior_archetype(self):
        """Test warrior combat stats."""
        warrior = CombatComponent(damage=10, defense=5, attack_range=1)

        assert warrior.damage == 10
        assert warrior.defense == 5
        assert warrior.is_melee()

    def test_archer_archetype(self):
        """Test archer combat stats."""
        archer = CombatComponent(damage=6, defense=2, attack_range=5)

        assert archer.damage == 6
        assert archer.defense == 2
        assert archer.is_ranged()
        assert archer.can_attack_at_range(4)

    def test_tank_archetype(self):
        """Test tank combat stats."""
        tank = CombatComponent(damage=3, defense=10, attack_range=1)

        assert tank.damage == 3
        assert tank.defense == 10
        assert tank.is_melee()

    def test_to_dict(self):
        """Test serialization to dictionary."""
        combat = CombatComponent(
            damage=10,
            defense=5,
            attack_range=3,
            accuracy=0.95,
            critical_chance=0.15,
            critical_multiplier=2.5
        )

        data = combat.to_dict()

        assert data['component_type'] == 'CombatComponent'
        assert data['damage'] == 10
        assert data['defense'] == 5
        assert data['attack_range'] == 3
        assert data['accuracy'] == 0.95
        assert data['critical_chance'] == 0.15
        assert data['critical_multiplier'] == 2.5

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {
            'component_type': 'CombatComponent',
            'damage': 15,
            'defense': 8,
            'attack_range': 2,
            'accuracy': 0.9,
            'critical_chance': 0.25,
            'critical_multiplier': 3.0
        }

        combat = CombatComponent.from_dict(data)

        assert combat.damage == 15
        assert combat.defense == 8
        assert combat.attack_range == 2
        assert combat.accuracy == 0.9
        assert combat.critical_chance == 0.25
        assert combat.critical_multiplier == 3.0

    def test_from_dict_with_defaults(self):
        """Test deserialization with missing fields uses defaults."""
        data = {'component_type': 'CombatComponent'}

        combat = CombatComponent.from_dict(data)

        assert combat.damage == 1
        assert combat.defense == 0
        assert combat.attack_range == 1
        assert combat.accuracy == 1.0
        assert combat.critical_chance == 0.0
        assert combat.critical_multiplier == 2.0

    def test_serialization_round_trip(self):
        """Test that serialization preserves all data."""
        original = CombatComponent(
            damage=12,
            defense=6,
            attack_range=4,
            accuracy=0.85,
            critical_chance=0.3,
            critical_multiplier=2.8
        )

        data = original.to_dict()
        restored = CombatComponent.from_dict(data)

        assert restored.damage == original.damage
        assert restored.defense == original.defense
        assert restored.attack_range == original.attack_range
        assert restored.accuracy == original.accuracy
        assert restored.critical_chance == original.critical_chance
        assert restored.critical_multiplier == original.critical_multiplier

    def test_damage_with_equipment_buffs(self):
        """Test damage modification from equipment."""
        combat = CombatComponent(damage=5)

        # Equip weapon (+3 damage)
        combat.modify_damage(3)
        assert combat.damage == 8

        # Add buff (+2 damage)
        combat.modify_damage(2)
        assert combat.damage == 10

        # Remove weapon
        combat.modify_damage(-3)
        assert combat.damage == 7

    def test_defense_with_armor_buffs(self):
        """Test defense modification from armor."""
        combat = CombatComponent(defense=2)

        # Equip armor (+5 defense)
        combat.modify_defense(5)
        assert combat.defense == 7

        # Add shield (+3 defense)
        combat.modify_defense(3)
        assert combat.defense == 10

        # Remove armor
        combat.modify_defense(-5)
        assert combat.defense == 5
