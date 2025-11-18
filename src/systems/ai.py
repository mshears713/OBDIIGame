"""
AI System - Processes enemy AI behaviors

This system handles enemy decision-making and actions during their turns.
It reads AIComponent data and executes appropriate behaviors.

Educational Notes:
------------------
The AI system is a core part of the game loop. Each turn:
1. Iterate through all entities with AIComponent
2. Determine what action the AI should take based on:
   - Behavior type (wander, chase, flee, etc.)
   - Player distance
   - Aggro/chase ranges
   - Intelligence level
3. Execute the action (move, attack, wait, etc.)

AI systems make enemies feel alive and challenging. Good AI:
- Is predictable enough to be learnable
- Is random enough to be interesting
- Provides appropriate challenge
- Gives player agency (can avoid/manipulate)
"""

import random
from typing import List, Optional, Tuple
from src.entities.entity import Entity
from src.components import (
    AIComponent,
    PositionComponent,
    CombatComponent,
    HealthComponent
)
from src.models import Map


class AISystem:
    """
    System for processing entity AI behaviors.

    This system implements different AI behaviors:
    - **Wander:** Random movement
    - **Chase:** Move toward target (usually player)
    - **Guard:** Stay in place, attack if in range
    - **Flee:** Move away from target
    - **Patrol:** Follow predetermined path

    Educational Note:
        AI systems operate on entities with specific component combinations.
        For example, chase AI needs:
        - AIComponent (behavior config)
        - PositionComponent (where entity is)
        - Target position (where to move toward)

        The system doesn't know about specific entity types (goblin, orc),
        it just processes components. This is the power of ECS.

    Example:
        >>> ai_system = AISystem(game_map, movement_system)
        >>> # Process all enemies
        >>> for enemy in enemies:
        ...     if enemy.has_component(AIComponent):
        ...         ai_system.process(enemy, player)
    """

    def __init__(self, game_map: Map, movement_system=None):
        """
        Initialize AI system.

        Args:
            game_map: The game map (for pathfinding, collision)
            movement_system: Movement system (for executing moves)

        Educational Note:
            Dependency Injection - we pass in required systems/data
            rather than creating them here. This makes testing easier.
        """
        self.game_map = game_map
        self.movement_system = movement_system

    def process(
        self,
        entity: Entity,
        player: Entity,
        all_entities: Optional[List[Entity]] = None,
        combat_system=None,
        message_log: Optional[List[str]] = None
    ) -> bool:
        """
        Process AI for one entity.

        Args:
            entity: Entity to process (must have AIComponent)
            player: Player entity (potential target)
            all_entities: All entities in game (for collision checks)

        Returns:
            True if entity took an action, False otherwise

        Educational Note:
            This is the main AI processing method. Called once per enemy
            per turn. It:
            1. Gets AI component
            2. Calculates distance to player
            3. Determines behavior
            4. Executes action
            5. Returns whether turn was consumed

        Example:
            >>> action_taken = ai_system.process(goblin, player)
            >>> if action_taken:
            ...     print("Goblin acted")
        """
        ai = entity.get_component(AIComponent)
        if not ai:
            return False

        position = entity.get_component(PositionComponent)
        if not position:
            return False

        # Get player position
        player_pos = player.get_component(PositionComponent)
        if not player_pos:
            return False

        # Calculate distance to player
        distance = self._calculate_distance(
            position.x, position.y,
            player_pos.x, player_pos.y
        )

        # Determine if player is in aggro range
        in_aggro_range = distance <= ai.aggro_range
        in_chase_range = distance <= ai.chase_range

        # Update target based on distance
        if in_aggro_range and not ai.has_target():
            ai.set_target(player.entity_id)
        elif not in_chase_range and ai.has_target():
            ai.clear_target()

        # Execute behavior
        if ai.behavior == "wander":
            return self._behavior_wander(entity, ai, position)

        elif ai.behavior == "chase":
            if ai.has_target():
                return self._behavior_chase(entity, ai, position, player_pos, distance, player, combat_system, message_log)
            else:
                return self._behavior_wander(entity, ai, position)

        elif ai.behavior == "guard":
            return self._behavior_guard(entity, ai, position, player_pos, distance)

        elif ai.behavior == "flee":
            return self._behavior_flee(entity, ai, position, player_pos)

        elif ai.behavior == "patrol":
            return self._behavior_patrol(entity, ai, position)

        return False

    def _behavior_wander(
        self,
        entity: Entity,
        ai: AIComponent,
        position: PositionComponent
    ) -> bool:
        """
        Execute wander behavior - random movement.

        Args:
            entity: Entity wandering
            ai: AI component
            position: Entity position

        Returns:
            True if moved, False otherwise

        Educational Note:
            Wander AI picks a random direction and tries to move there.
            This creates unpredictable movement without being completely
            chaotic - enemies still follow game rules (no walking through walls).

            Low-intelligence enemies might only move 50% of turns, making
            them easier to avoid.
        """
        # Intelligence affects movement frequency
        if ai.intelligence == "low" and random.random() < 0.5:
            return False  # Low intelligence = 50% chance to not move

        # Pick random direction
        directions = [
            (0, -1),   # North
            (0, 1),    # South
            (-1, 0),   # West
            (1, 0),    # East
            (-1, -1),  # Northwest
            (1, -1),   # Northeast
            (-1, 1),   # Southwest
            (1, 1)     # Southeast
        ]

        dx, dy = random.choice(directions)

        # Try to move
        if self.movement_system:
            return self.movement_system.try_move(entity, dx, dy)

        return False

    def _behavior_chase(
        self,
        entity: Entity,
        ai: AIComponent,
        position: PositionComponent,
        target_pos: PositionComponent,
        distance: int,
        target_entity: Optional[Entity] = None,
        combat_system=None,
        message_log: Optional[List[str]] = None
    ) -> bool:
        """
        Execute chase behavior - pursue target.

        Args:
            entity: Entity chasing
            ai: AI component
            position: Entity position
            target_pos: Target position
            distance: Distance to target

        Returns:
            True if action taken, False otherwise

        Educational Note:
            Chase AI moves toward the target (usually player).

            For simple chase, we just move in the general direction.
            More advanced AI uses pathfinding (A* algorithm) to navigate
            around obstacles.

            If adjacent to target, try to attack instead of move.
        """
        # Check if adjacent (can attack)
        if distance == 1:
            # Attack player if combat system available
            if combat_system and target_entity:
                combat_system.melee_attack(entity, target_entity, message_log)
                return True
            # No combat system - just wait
            return True

        # Calculate direction to target
        dx = 0
        dy = 0

        if target_pos.x > position.x:
            dx = 1
        elif target_pos.x < position.x:
            dx = -1

        if target_pos.y > position.y:
            dy = 1
        elif target_pos.y < position.y:
            dy = -1

        # Try to move toward target
        if self.movement_system and (dx != 0 or dy != 0):
            # Try diagonal first
            if dx != 0 and dy != 0:
                if self.movement_system.try_move(entity, dx, dy):
                    return True

            # Try horizontal
            if dx != 0:
                if self.movement_system.try_move(entity, dx, 0):
                    return True

            # Try vertical
            if dy != 0:
                if self.movement_system.try_move(entity, 0, dy):
                    return True

        return False

    def _behavior_guard(
        self,
        entity: Entity,
        ai: AIComponent,
        position: PositionComponent,
        target_pos: PositionComponent,
        distance: int
    ) -> bool:
        """
        Execute guard behavior - stay in place, attack if in range.

        Args:
            entity: Entity guarding
            ai: AI component
            position: Entity position
            target_pos: Target position
            distance: Distance to target

        Returns:
            True if action taken, False otherwise

        Educational Note:
            Guard AI doesn't move, but will attack if target is in range.
            This creates stationary threats that players must navigate around.

            Guards might face the player or track their movement visually.
        """
        # Guards don't move, but will attack if adjacent
        if distance == 1:
            # Attack logic handled by combat system
            return True

        # Just wait
        return True

    def _behavior_flee(
        self,
        entity: Entity,
        ai: AIComponent,
        position: PositionComponent,
        target_pos: PositionComponent
    ) -> bool:
        """
        Execute flee behavior - run away from target.

        Args:
            entity: Entity fleeing
            ai: AI component
            position: Entity position
            target_pos: Target position

        Returns:
            True if moved, False otherwise

        Educational Note:
            Flee AI moves away from the target. This is the opposite of chase.

            Flee behavior makes low-health enemies retreat, creating
            interesting tactical situations (chase down fleeing enemies
            or let them escape?).
        """
        # Calculate direction away from target
        dx = 0
        dy = 0

        if target_pos.x > position.x:
            dx = -1  # Target is east, flee west
        elif target_pos.x < position.x:
            dx = 1   # Target is west, flee east

        if target_pos.y > position.y:
            dy = -1  # Target is south, flee north
        elif target_pos.y < position.y:
            dy = 1   # Target is north, flee south

        # Try to move away
        if self.movement_system and (dx != 0 or dy != 0):
            # Try diagonal first
            if dx != 0 and dy != 0:
                if self.movement_system.try_move(entity, dx, dy):
                    return True

            # Try horizontal
            if dx != 0:
                if self.movement_system.try_move(entity, dx, 0):
                    return True

            # Try vertical
            if dy != 0:
                if self.movement_system.try_move(entity, 0, dy):
                    return True

        return False

    def _behavior_patrol(
        self,
        entity: Entity,
        ai: AIComponent,
        position: PositionComponent
    ) -> bool:
        """
        Execute patrol behavior - follow predefined path.

        Args:
            entity: Entity patrolling
            ai: AI component
            position: Entity position

        Returns:
            True if moved, False otherwise

        Educational Note:
            Patrol AI follows a predetermined path, cycling through points.
            This creates predictable but mobile threats.

            Players can learn patrol patterns and time their movements.
        """
        # Get next patrol point
        next_point = ai.get_next_patrol_point()
        if not next_point:
            # No patrol route, fall back to guard
            return True

        target_x, target_y = next_point

        # If at patrol point, move to next
        if position.x == target_x and position.y == target_y:
            return True

        # Move toward patrol point (simple chase logic)
        dx = 0
        dy = 0

        if target_x > position.x:
            dx = 1
        elif target_x < position.x:
            dx = -1

        if target_y > position.y:
            dy = 1
        elif target_y < position.y:
            dy = -1

        # Try to move
        if self.movement_system and (dx != 0 or dy != 0):
            if self.movement_system.try_move(entity, dx, dy):
                return True

        return False

    def _calculate_distance(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int
    ) -> int:
        """
        Calculate distance between two points.

        Args:
            x1, y1: First point
            x2, y2: Second point

        Returns:
            Chebyshev distance (max of abs differences)

        Educational Note:
            We use Chebyshev distance (chess-board distance) because:
            - It matches how entities move (8 directions)
            - Simple to calculate (no square roots)
            - Matches tactical grid layout

            Alternatives:
            - Manhattan distance: |dx| + |dy| (4-directional)
            - Euclidean distance: sqrt(dx² + dy²) (true distance)
        """
        return max(abs(x2 - x1), abs(y2 - y1))

    def process_all(
        self,
        entities: List[Entity],
        player: Entity
    ) -> None:
        """
        Process AI for all entities with AIComponent.

        Args:
            entities: All entities in the game
            player: Player entity

        Educational Note:
            Convenience method to process all AI in one call.
            Filters entities to only those with AI component.

        Example:
            >>> ai_system.process_all(all_entities, player)
            >>> # All enemies have now taken their turns
        """
        for entity in entities:
            if entity == player:
                continue  # Skip player

            if entity.has_component(AIComponent):
                self.process(entity, player, entities)
