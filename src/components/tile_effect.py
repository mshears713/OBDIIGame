"""
TileEffectComponent - Defines effects applied by tiles

This component is attached to tile entities to specify effects applied
to entities standing on or entering the tile.

Educational Note:
    Tile effects add environmental interaction to the game. In the automotive
    ECU theme, tiles represent different parts of the system with varying
    properties (corrupted memory, secure zones, signal boosters, etc.).
"""

from src.components.base import Component
from typing import Dict, Any, List


class TileEffectComponent(Component):
    """
    Component defining effects a tile applies to entities.

    Attributes:
        effect_type: Type of effect (damage, heal, status, signal, etc.)
        trigger: When effect activates ("enter", "step", "exit")
        value: Effect magnitude
        duration: Effect duration in turns (0 = instant)
        properties: Additional effect-specific properties

    Example:
        >>> # Damage tile (corrupted memory)
        >>> hazard = TileEffectComponent(
        ...     effect_type="damage",
        ...     trigger="step",
        ...     value=5
        ... )
        >>>
        >>> # Healing tile (diagnostic station)
        >>> heal_tile = TileEffectComponent(
        ...     effect_type="heal",
        ...     trigger="step",
        ...     value=10
        ... )
    """

    def __init__(
        self,
        effect_type: str = "none",
        trigger: str = "step",
        value: int = 0,
        duration: int = 0,
        properties: Dict[str, Any] = None
    ):
        """
        Initialize tile effect component.

        Args:
            effect_type: Type of effect to apply
            trigger: When to apply effect
            value: Effect magnitude
            duration: Effect duration
            properties: Additional properties
        """
        super().__init__()
        self.effect_type = effect_type
        self.trigger = trigger
        self.value = value
        self.duration = duration
        self.properties = properties if properties else {}

    def to_dict(self) -> Dict[str, Any]:
        """Serialize tile effect to dictionary."""
        return {
            'component_type': self.component_type,
            'effect_type': self.effect_type,
            'trigger': self.trigger,
            'value': self.value,
            'duration': self.duration,
            'properties': self.properties
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TileEffectComponent':
        """Deserialize tile effect from dictionary."""
        return cls(
            effect_type=data.get('effect_type', 'none'),
            trigger=data.get('trigger', 'step'),
            value=data.get('value', 0),
            duration=data.get('duration', 0),
            properties=data.get('properties', {})
        )
