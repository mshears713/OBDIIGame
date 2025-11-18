"""
HealthComponent - Tracks entity health and damage state

This component manages an entity's hit points (HP) and death state.

Educational Notes:
------------------
Health is a fundamental game mechanic in most combat games. This component
tracks both current and maximum HP, allowing for:
- Damage application (reduce current HP)
- Healing (increase current HP, capped at max)
- Death detection (current HP <= 0)
- Health UI display (show HP bars, percentages)

By separating health into a component, we can:
- Add health to any entity (player, enemies, even destructible objects)
- Systems can query and modify health without knowing entity type
- Save/load health state easily
"""

from src.components.base import Component
from typing import Dict, Any


class HealthComponent(Component):
    """
    Component tracking entity hit points and alive status.

    Attributes:
        current_hp: Current hit points (0 = dead)
        max_hp: Maximum hit points
        is_dead: Cached death state (updated when HP changes)

    Educational Note:
        We store both current and max HP to enable:
        - Health bars (current / max as percentage)
        - Healing (restore current toward max)
        - Temporary max HP boosts (buffs)
        - Damage over time effects

        The is_dead flag is cached for performance - checking it is faster
        than comparing current_hp <= 0 repeatedly.

    Example:
        >>> # Create player with 100 HP
        >>> health = HealthComponent(current_hp=100, max_hp=100)
        >>> assert health.is_alive()
        >>>
        >>> # Take damage
        >>> health.take_damage(30)
        >>> assert health.current_hp == 70
        >>>
        >>> # Heal
        >>> health.heal(20)
        >>> assert health.current_hp == 90
        >>>
        >>> # Take fatal damage
        >>> health.take_damage(100)
        >>> assert health.is_alive() is False
    """

    def __init__(self, current_hp: int = 100, max_hp: int = 100):
        """
        Initialize health component.

        Args:
            current_hp: Starting hit points (default 100)
            max_hp: Maximum hit points (default 100)

        Educational Note:
            current_hp should generally start equal to max_hp for healthy
            entities. However, you might start with less for wounded enemies
            or challenge modes.
        """
        super().__init__()
        self.max_hp = max_hp
        self.current_hp = current_hp
        self.is_dead = current_hp <= 0

    def take_damage(self, amount: int) -> int:
        """
        Apply damage to this entity.

        Args:
            amount: Damage points to apply (positive value)

        Returns:
            Actual damage dealt (might be less if already dead or overkill)

        Educational Note:
            Returns actual damage dealt to support:
            - Overkill prevention (can't deal more damage than current HP)
            - Damage logging/statistics
            - Combat feedback ("dealt 25 damage")

            We clamp current_hp to 0 minimum (no negative HP).

        Example:
            >>> health = HealthComponent(current_hp=50, max_hp=100)
            >>> actual = health.take_damage(30)
            >>> assert actual == 30
            >>> assert health.current_hp == 20
            >>>
            >>> # Overkill: only 20 HP left, but 50 damage dealt
            >>> actual = health.take_damage(50)
            >>> assert actual == 20  # Only dealt remaining HP
            >>> assert health.current_hp == 0
            >>> assert health.is_dead
        """
        if self.is_dead:
            return 0

        # Calculate actual damage (can't go below 0)
        actual_damage = min(amount, self.current_hp)

        self.current_hp -= actual_damage

        # Update death state
        if self.current_hp <= 0:
            self.current_hp = 0
            self.is_dead = True

        return actual_damage

    def heal(self, amount: int) -> int:
        """
        Restore hit points.

        Args:
            amount: HP to restore (positive value)

        Returns:
            Actual HP restored (capped at max_hp)

        Educational Note:
            Healing is capped at max_hp - can't heal beyond maximum.
            Returns actual healing done for feedback/logging.

            Dead entities can't be healed (would need resurrection mechanic).

        Example:
            >>> health = HealthComponent(current_hp=50, max_hp=100)
            >>> actual = health.heal(30)
            >>> assert actual == 30
            >>> assert health.current_hp == 80
            >>>
            >>> # Over-healing: only 20 HP missing, but 50 healing
            >>> actual = health.heal(50)
            >>> assert actual == 20  # Only healed to max
            >>> assert health.current_hp == 100
        """
        if self.is_dead:
            return 0

        # Calculate actual healing (can't exceed max)
        actual_healing = min(amount, self.max_hp - self.current_hp)

        self.current_hp += actual_healing

        return actual_healing

    def is_alive(self) -> bool:
        """
        Check if entity is alive.

        Returns:
            True if alive (HP > 0), False if dead

        Educational Note:
            This is the primary way to check if an entity should still
            act in the game. Dead entities typically:
            - Don't take turns
            - Don't block movement
            - Change appearance (corpse sprite)
            - Drop items/loot

        Example:
            >>> health = HealthComponent(current_hp=10, max_hp=100)
            >>> if health.is_alive():
            >>>     # Entity can act
            >>>     process_turn(entity)
        """
        return not self.is_dead

    def get_hp_percentage(self) -> float:
        """
        Get current HP as percentage of max HP.

        Returns:
            HP percentage (0.0 to 1.0)

        Educational Note:
            Useful for:
            - Health bars (width = percentage * bar_width)
            - AI decisions ("retreat if HP < 30%")
            - Color coding (green > 70%, yellow > 30%, red < 30%)

        Example:
            >>> health = HealthComponent(current_hp=75, max_hp=100)
            >>> assert health.get_hp_percentage() == 0.75
            >>>
            >>> # Use for health bar
            >>> bar_width = 20
            >>> filled = int(health.get_hp_percentage() * bar_width)
            >>> health_bar = '#' * filled + '-' * (bar_width - filled)
            >>> # Result: "###############-----" (15 filled, 5 empty)
        """
        if self.max_hp == 0:
            return 0.0
        return self.current_hp / self.max_hp

    def set_max_hp(self, new_max_hp: int) -> None:
        """
        Change maximum HP (and adjust current HP if needed).

        Args:
            new_max_hp: New maximum HP value

        Educational Note:
            Changing max HP is useful for:
            - Level up (increase max HP)
            - Equipment (armor adds max HP)
            - Buffs/debuffs (temporary max HP changes)

            When max HP decreases, current HP is capped to new maximum.
            When max HP increases, current HP stays the same (no free healing).

        Example:
            >>> health = HealthComponent(current_hp=80, max_hp=100)
            >>>
            >>> # Level up: increase max HP
            >>> health.set_max_hp(120)
            >>> assert health.max_hp == 120
            >>> assert health.current_hp == 80  # Current unchanged
            >>>
            >>> # Debuff: reduce max HP
            >>> health.set_max_hp(70)
            >>> assert health.max_hp == 70
            >>> assert health.current_hp == 70  # Capped to new max
        """
        self.max_hp = new_max_hp

        # Cap current HP if it exceeds new maximum
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

        # Update death state
        if self.current_hp <= 0:
            self.is_dead = True

    def restore_to_full(self) -> None:
        """
        Fully restore HP to maximum.

        Educational Note:
            Convenience method for:
            - Resting at safe locations
            - Full healing potions
            - Respawning after death
            - Level up bonuses

        Example:
            >>> health = HealthComponent(current_hp=20, max_hp=100)
            >>> health.restore_to_full()
            >>> assert health.current_hp == 100
        """
        self.current_hp = self.max_hp
        self.is_dead = False

    def to_dict(self) -> Dict[str, Any]:
        """Serialize health component to dictionary."""
        return {
            'component_type': self.component_type,
            'current_hp': self.current_hp,
            'max_hp': self.max_hp,
            'is_dead': self.is_dead
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HealthComponent':
        """
        Deserialize health component from dictionary.

        Args:
            data: Dictionary containing health data

        Returns:
            New HealthComponent instance
        """
        health = cls(
            current_hp=data.get('current_hp', 100),
            max_hp=data.get('max_hp', 100)
        )
        # Explicitly restore death state
        health.is_dead = data.get('is_dead', False)
        return health
