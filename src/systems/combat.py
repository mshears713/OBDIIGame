"""
Combat System - Handles combat between entities

This system processes attacks, damage calculation, and death handling.

Educational Notes:
------------------
Combat systems are central to most roguelikes. They handle:
- Attack resolution (hit/miss)
- Damage calculation
- Defense/armor application
- Critical hits
- Death handling
- Combat messaging

Key Design Decisions:
1. **Deterministic vs Random:** Do attacks always hit, or is there randomness?
2. **Damage Formula:** Simple subtraction, or complex calculations?
3. **Death Handling:** Instant removal, or corpse entities?
4. **Feedback:** How much information to show player?

This implementation uses a simple but effective system:
- Attacks check range first (must be adjacent for melee)
- Accuracy determines hit chance
- Damage is calculated, then reduced by defense
- Messages provide clear feedback
"""

import random
from typing import Optional, List, Tuple
from src.entities.entity import Entity
from src.components import (
    CombatComponent,
    HealthComponent,
    PositionComponent,
    NameComponent
)


class CombatSystem:
    """
    System for resolving combat between entities.

    This system handles all combat interactions:
    - Melee attacks
    - Ranged attacks (future)
    - Damage calculation
    - Death handling

    Educational Note:
        Combat systems operate on pairs of entities:
        - Attacker: Entity initiating the attack
        - Defender: Entity being attacked

        Both need specific components:
        - Attacker: CombatComponent (for attack stats), PositionComponent
        - Defender: HealthComponent (to take damage), PositionComponent

    Example:
        >>> combat_system = CombatSystem()
        >>> # Player attacks goblin
        >>> result = combat_system.attack(player, goblin)
        >>> if result.hit:
        ...     print(f"Dealt {result.damage} damage!")
    """

    def __init__(self):
        """Initialize combat system."""
        pass

    def attack(
        self,
        attacker: Entity,
        defender: Entity,
        messages: Optional[List[str]] = None
    ) -> bool:
        """
        Process an attack from attacker to defender.

        Args:
            attacker: Entity performing the attack
            defender: Entity being attacked
            messages: Optional list to append combat messages to

        Returns:
            True if attack was successful, False otherwise

        Educational Note:
            Attack resolution follows these steps:
            1. Validate entities (have required components)
            2. Check range (is defender in attack range?)
            3. Roll to hit (accuracy check)
            4. Calculate damage
            5. Apply damage to defender
            6. Check for death
            7. Generate feedback messages

        Example:
            >>> messages = []
            >>> success = combat_system.attack(player, goblin, messages)
            >>> for msg in messages:
            ...     print(msg)
            "You hit the Goblin for 5 damage!"
        """
        # Get required components
        attacker_combat = attacker.get_component(CombatComponent)
        attacker_pos = attacker.get_component(PositionComponent)
        attacker_name = attacker.get_component(NameComponent)

        defender_health = defender.get_component(HealthComponent)
        defender_pos = defender.get_component(PositionComponent)
        defender_name = defender.get_component(NameComponent)

        # Validate components
        if not all([attacker_combat, attacker_pos, defender_health, defender_pos]):
            return False

        # Get entity names for messages
        attacker_display_name = attacker_name.name if attacker_name else "Unknown"
        defender_display_name = defender_name.name if defender_name else "Unknown"

        # Check if defender is in range
        distance = self._calculate_distance(attacker_pos, defender_pos)
        if not attacker_combat.can_attack_at_range(distance):
            if messages is not None:
                messages.append(f"{attacker_display_name} cannot reach {defender_display_name}!")
            return False

        # Roll to hit (accuracy check)
        hit_roll = random.random()
        if hit_roll > attacker_combat.accuracy:
            # Miss
            if messages is not None:
                messages.append(f"{attacker_display_name} misses {defender_display_name}!")
            return False

        # Roll for critical hit
        is_critical = random.random() < attacker_combat.critical_chance

        # Calculate damage
        base_damage = attacker_combat.get_damage_output(is_critical=is_critical)

        # Get defender's combat component for defense (if it exists)
        defender_combat = defender.get_component(CombatComponent)
        if defender_combat:
            final_damage = defender_combat.calculate_damage_reduction(base_damage)
        else:
            final_damage = base_damage

        # Apply damage
        actual_damage = defender_health.take_damage(final_damage)

        # Generate message
        if messages is not None:
            if is_critical:
                messages.append(
                    f"{attacker_display_name} lands a CRITICAL HIT on {defender_display_name} "
                    f"for {actual_damage} damage!"
                )
            else:
                messages.append(
                    f"{attacker_display_name} hits {defender_display_name} "
                    f"for {actual_damage} damage!"
                )

            # Check for death
            if defender_health.is_dead:
                messages.append(f"{defender_display_name} has been destroyed!")

        return True

    def melee_attack(
        self,
        attacker: Entity,
        defender: Entity,
        messages: Optional[List[str]] = None
    ) -> bool:
        """
        Perform a melee attack (convenience method for attack with range check).

        Args:
            attacker: Entity performing melee attack
            defender: Entity being attacked
            messages: Optional list to append combat messages to

        Returns:
            True if attack was successful, False otherwise

        Educational Note:
            This is a convenience wrapper around attack() that specifically
            checks for melee range (adjacent tiles only).

        Example:
            >>> # Player tries to melee attack goblin
            >>> messages = []
            >>> if combat_system.melee_attack(player, goblin, messages):
            ...     print("Attack succeeded!")
        """
        # Get positions
        attacker_pos = attacker.get_component(PositionComponent)
        defender_pos = defender.get_component(PositionComponent)

        if not attacker_pos or not defender_pos:
            return False

        # Check if adjacent (melee range)
        distance = self._calculate_distance(attacker_pos, defender_pos)
        if distance != 1:
            if messages is not None:
                messages.append("Not in melee range!")
            return False

        # Perform attack
        return self.attack(attacker, defender, messages)

    def can_melee_attack(self, attacker: Entity, defender: Entity) -> bool:
        """
        Check if attacker can perform a melee attack on defender.

        Args:
            attacker: Entity that would attack
            defender: Entity that would be attacked

        Returns:
            True if melee attack is possible, False otherwise

        Educational Note:
            Useful for AI decision-making and UI hints.
            Checks:
            - Both entities have required components
            - Defender is alive
            - Defender is adjacent

        Example:
            >>> if combat_system.can_melee_attack(goblin, player):
            ...     # AI decides to attack
            ...     combat_system.melee_attack(goblin, player)
        """
        # Get required components
        attacker_combat = attacker.get_component(CombatComponent)
        attacker_pos = attacker.get_component(PositionComponent)
        defender_health = defender.get_component(HealthComponent)
        defender_pos = defender.get_component(PositionComponent)

        # Validate components and health
        if not all([attacker_combat, attacker_pos, defender_health, defender_pos]):
            return False

        if defender_health.is_dead:
            return False

        # Check if adjacent
        distance = self._calculate_distance(attacker_pos, defender_pos)
        return distance == 1

    def get_entity_at_position(
        self,
        x: int,
        y: int,
        entities: List[Entity],
        exclude: Optional[Entity] = None
    ) -> Optional[Entity]:
        """
        Find entity at given position.

        Args:
            x: X coordinate
            y: Y coordinate
            entities: List of all entities to search
            exclude: Optional entity to exclude from search

        Returns:
            Entity at position, or None if no entity there

        Educational Note:
            Used to find attack targets. When player moves into occupied
            tile, we check if there's an enemy there to attack.

        Example:
            >>> # Check if there's an enemy at (10, 5)
            >>> target = combat_system.get_entity_at_position(10, 5, all_entities)
            >>> if target and target.has_tag("enemy"):
            ...     combat_system.attack(player, target)
        """
        for entity in entities:
            if entity == exclude:
                continue

            pos = entity.get_component(PositionComponent)
            if pos and pos.x == x and pos.y == y:
                return entity

        return None

    def _calculate_distance(
        self,
        pos1: PositionComponent,
        pos2: PositionComponent
    ) -> int:
        """
        Calculate distance between two positions.

        Args:
            pos1: First position
            pos2: Second position

        Returns:
            Chebyshev distance (chess-board distance)

        Educational Note:
            We use Chebyshev distance (max of abs differences) because:
            - Matches 8-directional movement
            - Simple calculation
            - Matches tactical grid

            Distance 1 = adjacent (melee range)
            Distance > 1 = not adjacent
        """
        dx = abs(pos2.x - pos1.x)
        dy = abs(pos2.y - pos1.y)
        return max(dx, dy)

    def remove_dead_entities(self, entities: List[Entity]) -> Tuple[List[Entity], List[Entity]]:
        """
        Remove dead entities from entity list.

        Args:
            entities: List of all entities

        Returns:
            Tuple of (living_entities, dead_entities)

        Educational Note:
            Dead entities should be removed from the active entity list
            so they don't:
            - Take turns
            - Block movement
            - Appear in targeting

            We return both lists so you can:
            - Process death effects (drop items, XP)
            - Show death animations
            - Keep corpses for flavor

        Example:
            >>> living, dead = combat_system.remove_dead_entities(all_entities)
            >>> for corpse in dead:
            ...     # Drop items
            ...     drop_loot(corpse)
            >>> all_entities = living  # Update entity list
        """
        living = []
        dead = []

        for entity in entities:
            health = entity.get_component(HealthComponent)
            if health and health.is_dead:
                dead.append(entity)
            else:
                living.append(entity)

        return living, dead
