"""
CombatComponent - Defines entity combat statistics

This component stores offensive and defensive combat stats: damage dealt,
damage reduction, attack range, and special combat modifiers.

Educational Notes:
------------------
Combat stats are fundamental to most games. This component stores:
- **Damage:** How much damage attacks deal
- **Defense:** Damage reduction/armor value
- **Attack Range:** Melee (1) or ranged (>1)
- **Modifiers:** Critical hit chance, accuracy, etc.

By separating combat stats from health:
- Entities can have health without being able to attack (items, NPCs)
- Entities can attack without health (traps, turrets)
- Easy to modify stats with equipment/buffs
- Save/load combat state independently
"""

from src.components.base import Component
from typing import Dict, Any


class CombatComponent(Component):
    """
    Component storing entity combat statistics.

    Attributes:
        damage: Base damage dealt by attacks
        defense: Damage reduction (armor/resistance)
        attack_range: Attack range in tiles (1 = melee, >1 = ranged)
        accuracy: Hit chance modifier (0.0 to 1.0, 1.0 = always hit)
        critical_chance: Chance to deal critical damage (0.0 to 1.0)
        critical_multiplier: Damage multiplier on critical hit

    Educational Note:
        Combat stats enable diverse entity types:
        - High damage, low defense (glass cannon)
        - Low damage, high defense (tank)
        - Ranged attackers (archers, mages)
        - Critical-focused (rogues, assassins)

        Stats can be modified by equipment, buffs, and level-ups.

    Example:
        >>> # Melee warrior: high damage, medium defense
        >>> warrior = CombatComponent(damage=10, defense=5, attack_range=1)
        >>>
        >>> # Archer: medium damage, ranged, low defense
        >>> archer = CombatComponent(damage=6, defense=2, attack_range=5)
        >>>
        >>> # Tank: low damage, very high defense
        >>> tank = CombatComponent(damage=3, defense=10, attack_range=1)
    """

    def __init__(
        self,
        damage: int = 1,
        defense: int = 0,
        attack_range: int = 1,
        accuracy: float = 1.0,
        critical_chance: float = 0.0,
        critical_multiplier: float = 2.0
    ):
        """
        Initialize combat component.

        Args:
            damage: Base attack damage
            defense: Damage reduction
            attack_range: Attack range in tiles
            accuracy: Hit chance (1.0 = 100%)
            critical_chance: Crit chance (0.1 = 10%)
            critical_multiplier: Crit damage multiplier

        Educational Note:
            Default values create a basic melee attacker:
            - 1 damage (weak but functional)
            - 0 defense (no armor)
            - 1 range (melee only)
            - 100% accuracy
            - No crits
        """
        super().__init__()

        self.damage = damage
        self.defense = defense
        self.attack_range = attack_range
        self.accuracy = accuracy
        self.critical_chance = critical_chance
        self.critical_multiplier = critical_multiplier

    def get_damage_output(self, is_critical: bool = False) -> int:
        """
        Calculate damage output for an attack.

        Args:
            is_critical: Whether this is a critical hit

        Returns:
            Damage value to apply

        Educational Note:
            Damage calculation can be simple or complex:
            - Simple: Just return base damage
            - Medium: Add randomness (damage ± variance)
            - Complex: Factor in strength, skills, equipment, etc.

            This method handles critical hits for now.

        Example:
            >>> combat = CombatComponent(damage=10, critical_multiplier=2.0)
            >>> normal_damage = combat.get_damage_output(is_critical=False)
            >>> # normal_damage = 10
            >>> crit_damage = combat.get_damage_output(is_critical=True)
            >>> # crit_damage = 20
        """
        damage_value = self.damage

        if is_critical:
            damage_value = int(damage_value * self.critical_multiplier)

        return damage_value

    def calculate_damage_reduction(self, incoming_damage: int) -> int:
        """
        Calculate how much damage is blocked by defense.

        Args:
            incoming_damage: Damage before defense

        Returns:
            Damage after defense applied

        Educational Note:
            Defense can work different ways:
            - Flat reduction: damage - defense (used here)
            - Percentage reduction: damage * (1 - defense%)
            - Damage resistance: damage / (1 + defense)

            Flat reduction is simple but can reduce damage to 0.
            We ensure at least 1 damage gets through if any hits.

        Example:
            >>> combat = CombatComponent(defense=5)
            >>> reduced = combat.calculate_damage_reduction(10)
            >>> # reduced = 5 (10 - 5)
            >>> reduced = combat.calculate_damage_reduction(3)
            >>> # reduced = 1 (minimum 1 damage)
        """
        reduced_damage = incoming_damage - self.defense

        # Ensure at least 1 damage if any damage is dealt
        if incoming_damage > 0:
            reduced_damage = max(1, reduced_damage)

        return reduced_damage

    def is_melee(self) -> bool:
        """
        Check if this entity uses melee attacks.

        Returns:
            True if attack range is 1 (melee), False otherwise

        Educational Note:
            Distinguishing melee vs ranged affects gameplay:
            - Melee must be adjacent to attack
            - Ranged can attack from distance
            - Some abilities only work at certain ranges
        """
        return self.attack_range == 1

    def is_ranged(self) -> bool:
        """
        Check if this entity uses ranged attacks.

        Returns:
            True if attack range > 1 (ranged), False otherwise
        """
        return self.attack_range > 1

    def can_attack_at_range(self, distance: int) -> bool:
        """
        Check if entity can attack at given distance.

        Args:
            distance: Distance to target in tiles

        Returns:
            True if target is within attack range, False otherwise

        Educational Note:
            Range checking prevents invalid attacks:
            - Melee can only attack adjacent (distance 1)
            - Ranged has max range (e.g., archer range 5)
            - Some attacks have minimum range too

        Example:
            >>> melee = CombatComponent(attack_range=1)
            >>> melee.can_attack_at_range(1)  # True
            >>> melee.can_attack_at_range(2)  # False
            >>>
            >>> archer = CombatComponent(attack_range=5)
            >>> archer.can_attack_at_range(3)  # True
            >>> archer.can_attack_at_range(6)  # False
        """
        return 1 <= distance <= self.attack_range

    def modify_damage(self, modifier: int) -> None:
        """
        Modify base damage (equipment, buffs).

        Args:
            modifier: Amount to add to damage (can be negative)

        Educational Note:
            Temporary damage modifications from:
            - Equipment (+5 damage from sword)
            - Buffs (+3 damage from "Strength" spell)
            - Debuffs (-2 damage from "Weakness" curse)

        Example:
            >>> combat = CombatComponent(damage=5)
            >>> combat.modify_damage(3)  # Equipped +3 damage weapon
            >>> assert combat.damage == 8
        """
        self.damage = max(0, self.damage + modifier)

    def modify_defense(self, modifier: int) -> None:
        """
        Modify defense value (equipment, buffs).

        Args:
            modifier: Amount to add to defense (can be negative)

        Educational Note:
            Defense modifications from:
            - Armor (+5 defense from plate mail)
            - Shields (+2 defense)
            - Buffs (+3 defense from "Protection" spell)

        Example:
            >>> combat = CombatComponent(defense=2)
            >>> combat.modify_defense(5)  # Equipped +5 armor
            >>> assert combat.defense == 7
        """
        self.defense = max(0, self.defense + modifier)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize combat component to dictionary."""
        return {
            'component_type': self.component_type,
            'damage': self.damage,
            'defense': self.defense,
            'attack_range': self.attack_range,
            'accuracy': self.accuracy,
            'critical_chance': self.critical_chance,
            'critical_multiplier': self.critical_multiplier
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CombatComponent':
        """
        Deserialize combat component from dictionary.

        Args:
            data: Dictionary containing combat data

        Returns:
            New CombatComponent instance
        """
        return cls(
            damage=data.get('damage', 1),
            defense=data.get('defense', 0),
            attack_range=data.get('attack_range', 1),
            accuracy=data.get('accuracy', 1.0),
            critical_chance=data.get('critical_chance', 0.0),
            critical_multiplier=data.get('critical_multiplier', 2.0)
        )
