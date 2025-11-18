"""
StatusEffectComponent - Manages status effects on entities

Status effects are temporary or permanent modifiers that affect entity behavior,
stats, or capabilities (buffs, debuffs, conditions).

Educational Note:
    In automotive ECU systems, status effects represent system states:
    - Errors/faults (debuffs)
    - Optimizations (buffs)
    - Diagnostic modes
    - Safe modes
"""

from src.components.base import Component
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class StatusEffect:
    """
    Represents a single status effect.

    Attributes:
        effect_id: Unique identifier
        name: Display name
        effect_type: Type classification
        duration: Remaining turns (-1 = permanent)
        value: Effect magnitude
        stacks: Number of stacks
        properties: Additional properties
    """
    effect_id: str
    name: str
    effect_type: str  # buff, debuff, neutral
    duration: int  # -1 = permanent, 0 = expired, >0 = turns remaining
    value: float = 0.0
    stacks: int = 1
    properties: Dict[str, Any] = None

    def __post_init__(self):
        if self.properties is None:
            self.properties = {}

    def tick(self) -> bool:
        """
        Decrease duration by 1 turn.

        Returns:
            True if effect is still active, False if expired
        """
        if self.duration > 0:
            self.duration -= 1
        return self.duration != 0

    def is_active(self) -> bool:
        """Check if effect is still active."""
        return self.duration != 0


class StatusEffectComponent(Component):
    """
    Component managing status effects on an entity.

    Educational Note:
        Status effects add tactical depth - players must manage buffs/debuffs.
        Some effects stack, others don't. Some can be cleansed, others can't.

    Example:
        >>> status = StatusEffectComponent()
        >>> status.add_effect("poisoned", "Poisoned", "debuff", duration=5, value=2)
        >>> status.add_effect("shielded", "Shielded", "buff", duration=10)
    """

    def __init__(self):
        """Initialize status effect component."""
        super().__init__()
        self.effects: Dict[str, StatusEffect] = {}

    def add_effect(
        self,
        effect_id: str,
        name: str,
        effect_type: str,
        duration: int,
        value: float = 0.0,
        max_stacks: int = 1,
        properties: Dict[str, Any] = None
    ) -> bool:
        """
        Add or refresh a status effect.

        Args:
            effect_id: Unique effect identifier
            name: Display name
            effect_type: buff, debuff, or neutral
            duration: Effect duration in turns
            value: Effect magnitude
            max_stacks: Maximum stacks allowed
            properties: Additional properties

        Returns:
            True if effect was added/refreshed
        """
        if effect_id in self.effects:
            # Effect already exists - refresh or stack
            existing = self.effects[effect_id]

            # Refresh duration to higher value
            if duration > existing.duration:
                existing.duration = duration

            # Stack if allowed
            if existing.stacks < max_stacks:
                existing.stacks += 1

            return True
        else:
            # Add new effect
            effect = StatusEffect(
                effect_id=effect_id,
                name=name,
                effect_type=effect_type,
                duration=duration,
                value=value,
                stacks=1,
                properties=properties or {}
            )
            self.effects[effect_id] = effect
            return True

    def remove_effect(self, effect_id: str) -> bool:
        """
        Remove a status effect.

        Args:
            effect_id: Effect to remove

        Returns:
            True if effect was removed
        """
        if effect_id in self.effects:
            del self.effects[effect_id]
            return True
        return False

    def has_effect(self, effect_id: str) -> bool:
        """Check if entity has a specific effect."""
        return effect_id in self.effects and self.effects[effect_id].is_active()

    def get_effect(self, effect_id: str) -> Optional[StatusEffect]:
        """Get a specific status effect."""
        return self.effects.get(effect_id)

    def get_effects_by_type(self, effect_type: str) -> List[StatusEffect]:
        """Get all effects of a specific type."""
        return [e for e in self.effects.values() if e.effect_type == effect_type and e.is_active()]

    def tick_effects(self) -> List[str]:
        """
        Tick all effects (decrease duration).

        Returns:
            List of effect IDs that expired
        """
        expired = []

        for effect_id, effect in list(self.effects.items()):
            if not effect.tick():
                expired.append(effect_id)
                del self.effects[effect_id]

        return expired

    def clear_effects(self, effect_type: Optional[str] = None) -> int:
        """
        Clear all effects or effects of a specific type.

        Args:
            effect_type: Type to clear (None = all)

        Returns:
            Number of effects cleared
        """
        if effect_type is None:
            count = len(self.effects)
            self.effects.clear()
            return count
        else:
            cleared = [eid for eid, e in self.effects.items() if e.effect_type == effect_type]
            for eid in cleared:
                del self.effects[eid]
            return len(cleared)

    def get_stat_modifier(self, stat_name: str) -> float:
        """
        Calculate total modifier for a stat from all effects.

        Args:
            stat_name: Stat name to calculate modifier for

        Returns:
            Combined modifier value

        Example:
            >>> # Two effects both modify "damage_reduction"
            >>> modifier = status.get_stat_modifier("damage_reduction")
        """
        total = 0.0

        for effect in self.effects.values():
            if effect.is_active() and stat_name in effect.properties:
                total += effect.properties[stat_name] * effect.stacks

        return total

    def to_dict(self) -> Dict[str, Any]:
        """Serialize status effects to dictionary."""
        return {
            'component_type': self.component_type,
            'effects': {
                eid: {
                    'effect_id': e.effect_id,
                    'name': e.name,
                    'effect_type': e.effect_type,
                    'duration': e.duration,
                    'value': e.value,
                    'stacks': e.stacks,
                    'properties': e.properties
                }
                for eid, e in self.effects.items()
            }
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StatusEffectComponent':
        """Deserialize status effects from dictionary."""
        component = cls()

        effects_data = data.get('effects', {})
        for effect_data in effects_data.values():
            effect = StatusEffect(
                effect_id=effect_data['effect_id'],
                name=effect_data['name'],
                effect_type=effect_data['effect_type'],
                duration=effect_data['duration'],
                value=effect_data.get('value', 0.0),
                stacks=effect_data.get('stacks', 1),
                properties=effect_data.get('properties', {})
            )
            component.effects[effect.effect_id] = effect

        return component
