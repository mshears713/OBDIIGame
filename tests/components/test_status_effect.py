"""
Unit tests for StatusEffectComponent

Tests cover:
- StatusEffect dataclass
- Adding and removing effects
- Effect stacking
- Effect duration and ticking
- Stat modifiers
- Serialization and deserialization
"""

import pytest
from src.components.status_effect import StatusEffectComponent, StatusEffect


class TestStatusEffect:
    """Test suite for StatusEffect dataclass."""

    def test_status_effect_creation(self):
        """Test creating a status effect."""
        effect = StatusEffect(
            effect_id="poison",
            name="Poisoned",
            effect_type="debuff",
            duration=5,
            value=2.0
        )

        assert effect.effect_id == "poison"
        assert effect.name == "Poisoned"
        assert effect.effect_type == "debuff"
        assert effect.duration == 5
        assert effect.value == 2.0
        assert effect.stacks == 1

    def test_status_effect_with_properties(self):
        """Test status effect with custom properties."""
        props = {"damage_per_turn": 3, "armor_reduction": 2}
        effect = StatusEffect(
            effect_id="corroded",
            name="Corroded",
            effect_type="debuff",
            duration=10,
            properties=props
        )

        assert effect.properties == props
        assert effect.properties["damage_per_turn"] == 3

    def test_status_effect_tick(self):
        """Test ticking effect duration."""
        effect = StatusEffect(
            effect_id="buff",
            name="Strength",
            effect_type="buff",
            duration=3
        )

        # First tick
        is_active = effect.tick()
        assert is_active is True
        assert effect.duration == 2

        # Second tick
        is_active = effect.tick()
        assert is_active is True
        assert effect.duration == 1

        # Third tick - expires
        is_active = effect.tick()
        assert is_active is False
        assert effect.duration == 0

    def test_status_effect_permanent(self):
        """Test permanent effect (-1 duration)."""
        effect = StatusEffect(
            effect_id="permanent",
            name="Blessed",
            effect_type="buff",
            duration=-1
        )

        # Tick doesn't change permanent effects
        is_active = effect.tick()
        assert is_active is True
        assert effect.duration == -1

    def test_status_effect_is_active(self):
        """Test is_active check."""
        active_effect = StatusEffect(
            effect_id="active",
            name="Active",
            effect_type="buff",
            duration=5
        )

        expired_effect = StatusEffect(
            effect_id="expired",
            name="Expired",
            effect_type="buff",
            duration=0
        )

        assert active_effect.is_active() is True
        assert expired_effect.is_active() is False


class TestStatusEffectComponent:
    """Test suite for StatusEffectComponent."""

    def test_initialization(self):
        """Test component initialization."""
        status = StatusEffectComponent()

        assert status.effects == {}

    def test_add_effect(self):
        """Test adding a new effect."""
        status = StatusEffectComponent()

        result = status.add_effect(
            effect_id="burn",
            name="Burning",
            effect_type="debuff",
            duration=5,
            value=3.0
        )

        assert result is True
        assert "burn" in status.effects
        assert status.has_effect("burn") is True

    def test_add_multiple_effects(self):
        """Test adding multiple different effects."""
        status = StatusEffectComponent()

        status.add_effect("poison", "Poisoned", "debuff", duration=5)
        status.add_effect("shield", "Shielded", "buff", duration=10)
        status.add_effect("slow", "Slowed", "debuff", duration=3)

        assert len(status.effects) == 3
        assert status.has_effect("poison")
        assert status.has_effect("shield")
        assert status.has_effect("slow")

    def test_add_effect_refresh_duration(self):
        """Test that re-adding effect refreshes duration."""
        status = StatusEffectComponent()

        # Add effect with 5 turn duration
        status.add_effect("regen", "Regenerating", "buff", duration=5)
        assert status.effects["regen"].duration == 5

        # Re-add with longer duration - should refresh
        status.add_effect("regen", "Regenerating", "buff", duration=10)
        assert status.effects["regen"].duration == 10

        # Re-add with shorter duration - should keep longer
        status.add_effect("regen", "Regenerating", "buff", duration=3)
        assert status.effects["regen"].duration == 10

    def test_add_effect_stacking(self):
        """Test effect stacking."""
        status = StatusEffectComponent()

        # Add effect with max_stacks=3
        status.add_effect("strength", "Strong", "buff", duration=10, max_stacks=3)
        assert status.effects["strength"].stacks == 1

        # Add again - should stack
        status.add_effect("strength", "Strong", "buff", duration=10, max_stacks=3)
        assert status.effects["strength"].stacks == 2

        # Add again - should stack
        status.add_effect("strength", "Strong", "buff", duration=10, max_stacks=3)
        assert status.effects["strength"].stacks == 3

        # Add again - should not stack beyond max
        status.add_effect("strength", "Strong", "buff", duration=10, max_stacks=3)
        assert status.effects["strength"].stacks == 3

    def test_remove_effect(self):
        """Test removing an effect."""
        status = StatusEffectComponent()

        status.add_effect("freeze", "Frozen", "debuff", duration=5)

        result = status.remove_effect("freeze")

        assert result is True
        assert "freeze" not in status.effects
        assert status.has_effect("freeze") is False

    def test_remove_effect_not_found(self):
        """Test removing non-existent effect."""
        status = StatusEffectComponent()

        result = status.remove_effect("nonexistent")

        assert result is False

    def test_has_effect(self):
        """Test checking if effect exists."""
        status = StatusEffectComponent()

        status.add_effect("haste", "Hasted", "buff", duration=5)

        assert status.has_effect("haste") is True
        assert status.has_effect("slow") is False

    def test_get_effect(self):
        """Test getting a specific effect."""
        status = StatusEffectComponent()

        status.add_effect("armor", "Armored", "buff", duration=10, value=5.0)

        effect = status.get_effect("armor")

        assert effect is not None
        assert effect.effect_id == "armor"
        assert effect.value == 5.0

    def test_get_effect_not_found(self):
        """Test getting non-existent effect."""
        status = StatusEffectComponent()

        effect = status.get_effect("missing")

        assert effect is None

    def test_get_effects_by_type(self):
        """Test getting effects by type."""
        status = StatusEffectComponent()

        status.add_effect("poison", "Poisoned", "debuff", duration=5)
        status.add_effect("burn", "Burning", "debuff", duration=3)
        status.add_effect("shield", "Shielded", "buff", duration=10)
        status.add_effect("haste", "Hasted", "buff", duration=8)

        debuffs = status.get_effects_by_type("debuff")
        buffs = status.get_effects_by_type("buff")

        assert len(debuffs) == 2
        assert len(buffs) == 2

    def test_tick_effects(self):
        """Test ticking all effects."""
        status = StatusEffectComponent()

        status.add_effect("short", "Short", "buff", duration=2)
        status.add_effect("medium", "Medium", "buff", duration=5)
        status.add_effect("long", "Long", "buff", duration=10)

        # First tick
        expired = status.tick_effects()
        assert len(expired) == 0
        assert len(status.effects) == 3

        # Tick until short expires
        status.tick_effects()  # short = 0, expires

        assert len(status.effects) == 2
        assert "short" not in status.effects
        assert "medium" in status.effects
        assert "long" in status.effects

    def test_tick_effects_returns_expired(self):
        """Test that tick_effects returns list of expired effect IDs."""
        status = StatusEffectComponent()

        status.add_effect("effect1", "Effect 1", "buff", duration=1)
        status.add_effect("effect2", "Effect 2", "buff", duration=2)

        # First tick - effect1 expires
        expired = status.tick_effects()

        assert "effect1" in expired
        assert len(expired) == 1

    def test_clear_effects_all(self):
        """Test clearing all effects."""
        status = StatusEffectComponent()

        status.add_effect("poison", "Poisoned", "debuff", duration=5)
        status.add_effect("burn", "Burning", "debuff", duration=3)
        status.add_effect("shield", "Shielded", "buff", duration=10)

        count = status.clear_effects()

        assert count == 3
        assert len(status.effects) == 0

    def test_clear_effects_by_type(self):
        """Test clearing effects of specific type."""
        status = StatusEffectComponent()

        status.add_effect("poison", "Poisoned", "debuff", duration=5)
        status.add_effect("burn", "Burning", "debuff", duration=3)
        status.add_effect("shield", "Shielded", "buff", duration=10)

        count = status.clear_effects(effect_type="debuff")

        assert count == 2
        assert len(status.effects) == 1
        assert status.has_effect("shield")
        assert not status.has_effect("poison")
        assert not status.has_effect("burn")

    def test_get_stat_modifier(self):
        """Test calculating stat modifiers."""
        status = StatusEffectComponent()

        # Add effect that modifies damage
        status.add_effect(
            "strength",
            "Strength",
            "buff",
            duration=10,
            properties={"damage": 5}
        )

        # Add another effect that modifies damage
        status.add_effect(
            "rage",
            "Rage",
            "buff",
            duration=5,
            properties={"damage": 3}
        )

        modifier = status.get_stat_modifier("damage")

        assert modifier == 8  # 5 + 3

    def test_get_stat_modifier_with_stacks(self):
        """Test stat modifiers with stacking effects."""
        status = StatusEffectComponent()

        # Add stackable effect
        status.add_effect(
            "armor",
            "Armor",
            "buff",
            duration=10,
            max_stacks=3,
            properties={"defense": 2}
        )

        # Stack it twice more
        status.add_effect(
            "armor",
            "Armor",
            "buff",
            duration=10,
            max_stacks=3,
            properties={"defense": 2}
        )

        status.add_effect(
            "armor",
            "Armor",
            "buff",
            duration=10,
            max_stacks=3,
            properties={"defense": 2}
        )

        modifier = status.get_stat_modifier("defense")

        assert modifier == 6  # 2 * 3 stacks

    def test_get_stat_modifier_no_matching_effects(self):
        """Test stat modifier when no effects modify that stat."""
        status = StatusEffectComponent()

        status.add_effect(
            "speed",
            "Speed",
            "buff",
            duration=5,
            properties={"movement": 2}
        )

        modifier = status.get_stat_modifier("damage")

        assert modifier == 0.0

    def test_to_dict(self):
        """Test serialization to dictionary."""
        status = StatusEffectComponent()

        status.add_effect(
            "poison",
            "Poisoned",
            "debuff",
            duration=5,
            value=2.0,
            properties={"damage_per_turn": 2}
        )

        data = status.to_dict()

        assert data['component_type'] == 'StatusEffectComponent'
        assert 'poison' in data['effects']
        assert data['effects']['poison']['name'] == "Poisoned"
        assert data['effects']['poison']['duration'] == 5

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {
            'component_type': 'StatusEffectComponent',
            'effects': {
                'burn': {
                    'effect_id': 'burn',
                    'name': 'Burning',
                    'effect_type': 'debuff',
                    'duration': 3,
                    'value': 1.5,
                    'stacks': 2,
                    'properties': {'fire_damage': 3}
                }
            }
        }

        status = StatusEffectComponent.from_dict(data)

        assert 'burn' in status.effects
        effect = status.effects['burn']
        assert effect.name == 'Burning'
        assert effect.duration == 3
        assert effect.stacks == 2
        assert effect.properties['fire_damage'] == 3

    def test_serialization_round_trip(self):
        """Test that serialization preserves all data."""
        original = StatusEffectComponent()

        original.add_effect("effect1", "Effect 1", "buff", duration=10, value=5.0)
        original.add_effect("effect2", "Effect 2", "debuff", duration=5, max_stacks=2)
        original.add_effect("effect2", "Effect 2", "debuff", duration=5, max_stacks=2)  # Stack

        data = original.to_dict()
        restored = StatusEffectComponent.from_dict(data)

        assert len(restored.effects) == len(original.effects)
        assert restored.has_effect("effect1")
        assert restored.has_effect("effect2")
        assert restored.effects["effect2"].stacks == 2

    def test_combat_scenario(self):
        """Test realistic combat status effect scenario."""
        status = StatusEffectComponent()

        # Player gets poisoned
        status.add_effect("poison", "Poisoned", "debuff", duration=5, value=2.0)

        # Player uses shield
        status.add_effect("shield", "Shielded", "buff", duration=3, value=5.0)

        # Player gets hit with slow
        status.add_effect("slow", "Slowed", "debuff", duration=4)

        assert len(status.effects) == 3

        # Cure poison
        status.remove_effect("poison")

        assert len(status.effects) == 2

        # Time passes (2 turns)
        status.tick_effects()
        status.tick_effects()

        # Shield should expire, slow should have 2 turns left
        status.tick_effects()

        assert not status.has_effect("shield")
        assert status.has_effect("slow")
