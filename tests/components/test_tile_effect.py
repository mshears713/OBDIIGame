"""
Unit tests for TileEffectComponent

Tests cover:
- Component initialization
- Trigger type management
- Properties and metadata
- Serialization and deserialization
"""

import pytest
from src.components.tile_effect import TileEffectComponent


class TestTileEffectComponent:
    """Test suite for TileEffectComponent."""

    def test_initialization_with_defaults(self):
        """Test default initialization."""
        tile_effect = TileEffectComponent()

        assert tile_effect.effect_type == "none"
        assert tile_effect.trigger == "step"
        assert tile_effect.value == 0
        assert tile_effect.duration == 0
        assert tile_effect.properties == {}

    def test_initialization_with_custom_values(self):
        """Test initialization with custom parameters."""
        props = {"element": "fire", "visual": "flames"}
        tile_effect = TileEffectComponent(
            effect_type="damage",
            trigger="enter",
            value=5,
            duration=3,
            properties=props
        )

        assert tile_effect.effect_type == "damage"
        assert tile_effect.trigger == "enter"
        assert tile_effect.value == 5
        assert tile_effect.duration == 3
        assert tile_effect.properties == props

    def test_damage_effect(self):
        """Test damage effect configuration."""
        tile_effect = TileEffectComponent(
            effect_type="damage",
            trigger="step",
            value=3
        )

        assert tile_effect.effect_type == "damage"
        assert tile_effect.value == 3

    def test_healing_effect(self):
        """Test healing effect configuration."""
        tile_effect = TileEffectComponent(
            effect_type="heal",
            trigger="step",
            value=2
        )

        assert tile_effect.effect_type == "heal"
        assert tile_effect.value == 2

    def test_status_effect(self):
        """Test status effect configuration."""
        props = {"status_id": "poison", "duration": 5}
        tile_effect = TileEffectComponent(
            effect_type="status",
            trigger="enter",
            properties=props
        )

        assert tile_effect.effect_type == "status"
        assert tile_effect.properties["status_id"] == "poison"
        assert tile_effect.properties["duration"] == 5

    def test_trigger_types(self):
        """Test different trigger types."""
        enter_effect = TileEffectComponent(trigger="enter")
        step_effect = TileEffectComponent(trigger="step")
        exit_effect = TileEffectComponent(trigger="exit")

        assert enter_effect.trigger == "enter"
        assert step_effect.trigger == "step"
        assert exit_effect.trigger == "exit"

    def test_properties_storage(self):
        """Test storing custom properties."""
        props = {
            "element": "ice",
            "visual_effect": "frost",
            "sound": "crackle",
            "intensity": 7
        }

        tile_effect = TileEffectComponent(
            effect_type="damage",
            properties=props
        )

        assert tile_effect.properties["element"] == "ice"
        assert tile_effect.properties["visual_effect"] == "frost"
        assert tile_effect.properties["sound"] == "crackle"
        assert tile_effect.properties["intensity"] == 7

    def test_to_dict(self):
        """Test serialization to dictionary."""
        props = {"damage_type": "fire", "radius": 1}
        tile_effect = TileEffectComponent(
            effect_type="damage",
            trigger="enter",
            value=10,
            duration=2,
            properties=props
        )

        data = tile_effect.to_dict()

        assert data['component_type'] == 'TileEffectComponent'
        assert data['effect_type'] == "damage"
        assert data['trigger'] == "enter"
        assert data['value'] == 10
        assert data['duration'] == 2
        assert data['properties'] == props

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {
            'component_type': 'TileEffectComponent',
            'effect_type': 'heal',
            'trigger': 'step',
            'value': 5,
            'duration': 1,
            'properties': {'heal_type': 'gradual'}
        }

        tile_effect = TileEffectComponent.from_dict(data)

        assert tile_effect.effect_type == "heal"
        assert tile_effect.trigger == "step"
        assert tile_effect.value == 5
        assert tile_effect.duration == 1
        assert tile_effect.properties['heal_type'] == 'gradual'

    def test_from_dict_with_defaults(self):
        """Test deserialization with missing fields."""
        data = {'component_type': 'TileEffectComponent'}

        tile_effect = TileEffectComponent.from_dict(data)

        assert tile_effect.effect_type == "none"
        assert tile_effect.trigger == "step"
        assert tile_effect.value == 0
        assert tile_effect.duration == 0
        assert tile_effect.properties == {}

    def test_serialization_round_trip(self):
        """Test that serialization preserves all data."""
        props = {"element": "lightning", "chance": 0.5}
        original = TileEffectComponent(
            effect_type="damage",
            trigger="exit",
            value=15,
            duration=4,
            properties=props
        )

        data = original.to_dict()
        restored = TileEffectComponent.from_dict(data)

        assert restored.effect_type == original.effect_type
        assert restored.trigger == original.trigger
        assert restored.value == original.value
        assert restored.duration == original.duration
        assert restored.properties == original.properties

    def test_automotive_themed_effects(self):
        """Test automotive ECU themed tile effects."""
        # Corrupted data tile
        corrupted = TileEffectComponent(
            effect_type="damage",
            trigger="step",
            value=2,
            properties={"description": "Corrupted data packets"}
        )

        # Diagnostic port (healing)
        diagnostic = TileEffectComponent(
            effect_type="heal",
            trigger="step",
            value=3,
            properties={"description": "System diagnostic port"}
        )

        # Error state tile
        error = TileEffectComponent(
            effect_type="status",
            trigger="enter",
            properties={
                "status_id": "error_state",
                "duration": 5,
                "description": "ECU error condition"
            }
        )

        assert corrupted.effect_type == "damage"
        assert diagnostic.effect_type == "heal"
        assert error.effect_type == "status"

    def test_hazard_tiles(self):
        """Test various hazard tile configurations."""
        # Lava/fire hazard
        lava = TileEffectComponent(
            effect_type="damage",
            trigger="step",
            value=5,
            properties={"element": "fire", "visual": "lava"}
        )

        # Spike trap
        spikes = TileEffectComponent(
            effect_type="damage",
            trigger="enter",
            value=10,
            properties={"trap_type": "spikes", "avoidable": False}
        )

        # Poison gas
        gas = TileEffectComponent(
            effect_type="status",
            trigger="step",
            properties={
                "status_id": "poisoned",
                "duration": 3,
                "stacks": 1
            }
        )

        assert lava.value == 5
        assert spikes.trigger == "enter"
        assert gas.properties["status_id"] == "poisoned"

    def test_beneficial_tiles(self):
        """Test beneficial tile effects."""
        # Healing fountain
        fountain = TileEffectComponent(
            effect_type="heal",
            trigger="step",
            value=5,
            properties={"renewable": True}
        )

        # Buff shrine
        shrine = TileEffectComponent(
            effect_type="status",
            trigger="enter",
            properties={
                "status_id": "blessed",
                "duration": 20,
                "buff_type": "defense"
            }
        )

        assert fountain.effect_type == "heal"
        assert shrine.properties["status_id"] == "blessed"

    def test_complex_properties(self):
        """Test complex nested properties."""
        tile_effect = TileEffectComponent(
            effect_type="damage",
            trigger="step",
            value=3,
            properties={
                "damage": {
                    "type": "fire",
                    "min": 2,
                    "max": 5
                },
                "visual": {
                    "color": "red",
                    "animation": "flicker"
                },
                "conditions": {
                    "immunity": ["fire_resistance"],
                    "amplified_by": ["oil_covered"]
                }
            }
        )

        assert tile_effect.properties["damage"]["type"] == "fire"
        assert tile_effect.properties["visual"]["color"] == "red"
        assert "fire_resistance" in tile_effect.properties["conditions"]["immunity"]

    def test_empty_properties(self):
        """Test tile effect with no properties."""
        tile_effect = TileEffectComponent(
            effect_type="damage",
            trigger="step",
            value=1
        )

        assert tile_effect.properties == {}

    def test_zero_value_effect(self):
        """Test effect with zero value (status only)."""
        tile_effect = TileEffectComponent(
            effect_type="status",
            trigger="enter",
            value=0,
            properties={"status_id": "slowed"}
        )

        assert tile_effect.value == 0
        assert tile_effect.properties["status_id"] == "slowed"

    def test_negative_value_effect(self):
        """Test effect with negative value."""
        tile_effect = TileEffectComponent(
            effect_type="damage",
            trigger="step",
            value=-5  # Could represent healing or reverse effect
        )

        assert tile_effect.value == -5
