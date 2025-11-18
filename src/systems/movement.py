"""
Movement System

This module handles entity movement validation and execution.

Educational Notes:
------------------
The movement system is responsible for:
1. Validating movement (is destination walkable? in bounds?)
2. Executing movement (update PositionComponent)
3. Preventing illegal moves (walking through walls)

In ECS architecture, systems operate on entities with specific components.
The movement system processes entities that have PositionComponent and
need to move.

Key Design Principles:
- Validate before moving (check before changing state)
- Return success/failure (caller knows if move worked)
- Keep state in components (system is stateless)
"""

from typing import Optional, Tuple
from src.entities.entity import Entity
from src.components import PositionComponent
from src.models import Map


class MovementSystem:
    """
    System for validating and executing entity movement.

    Educational Note:
        This system handles all movement logic. By centralizing movement
        in one place, we ensure consistent behavior for all entities
        (player, enemies, items being pushed, etc.).

        The system is stateless - all state lives in components and the map.
        This makes testing easier and prevents bugs from stale state.
    """

    def __init__(self, game_map: Map):
        """
        Initialize movement system.

        Args:
            game_map: The dungeon map for collision checking

        Educational Note:
            The system needs the map to check walkability. We pass it
            during initialization rather than with every move call to
            avoid repetition.
        """
        self.game_map = game_map

    def can_move_to(self, x: int, y: int) -> bool:
        """
        Check if a position is valid for movement.

        Args:
            x: Target X coordinate
            y: Target Y coordinate

        Returns:
            True if position is walkable, False otherwise

        Educational Note:
            This method encapsulates all movement validation:
            - Is position in bounds?
            - Is tile walkable?
            - (Future: Is position occupied by another entity?)

            By separating validation from execution, we can:
            - Preview moves before executing
            - AI can check multiple positions
            - UI can highlight valid moves

        Example:
            >>> system = MovementSystem(dungeon_map)
            >>> if system.can_move_to(10, 15):
            >>>     # Position is valid, safe to move there
            >>>     pass
        """
        return self.game_map.is_walkable(x, y)

    def try_move(self, entity: Entity, dx: int, dy: int) -> bool:
        """
        Attempt to move an entity by delta values.

        Args:
            entity: Entity to move
            dx: Change in X (-1, 0, 1)
            dy: Change in Y (-1, 0, 1)

        Returns:
            True if move succeeded, False if move failed

        Educational Note:
            This is the main movement method. It:
            1. Gets entity's current position
            2. Calculates target position
            3. Validates target position
            4. Updates position if valid

            Returns boolean success indicator so caller can:
            - Show feedback ("You bump into a wall")
            - Make sounds (footstep vs. bump)
            - Consume turn (successful move ends turn)

        Example:
            >>> system = MovementSystem(dungeon_map)
            >>> player = create_player(x=10, y=10)
            >>>
            >>> # Try to move right
            >>> success = system.try_move(player, dx=1, dy=0)
            >>> if success:
            >>>     print("Player moved!")
            >>> else:
            >>>     print("Can't move there!")
        """
        # Get entity's position component
        position = entity.get_component(PositionComponent)
        if not position:
            # Entity has no position component - can't move
            return False

        # Calculate target position
        target_x = position.x + dx
        target_y = position.y + dy

        # Validate target position
        if not self.can_move_to(target_x, target_y):
            return False

        # Move is valid - update position
        position.move(dx, dy)
        return True

    def move_to(self, entity: Entity, x: int, y: int) -> bool:
        """
        Move entity to absolute coordinates.

        Args:
            entity: Entity to move
            x: Target X coordinate
            y: Target Y coordinate

        Returns:
            True if move succeeded, False if move failed

        Educational Note:
            This method moves to absolute coordinates rather than relative.
            Useful for:
            - Teleportation
            - Spawning entities
            - Knockback effects (calculate target, then move_to)

        Example:
            >>> system = MovementSystem(dungeon_map)
            >>> player = create_player()
            >>>
            >>> # Teleport to specific location
            >>> success = system.move_to(player, x=25, y=30)
        """
        # Get entity's position component
        position = entity.get_component(PositionComponent)
        if not position:
            return False

        # Validate target position
        if not self.can_move_to(x, y):
            return False

        # Move is valid - set position
        position.set_position(x, y)
        return True

    def get_position(self, entity: Entity) -> Optional[Tuple[int, int]]:
        """
        Get entity's current position.

        Args:
            entity: Entity to query

        Returns:
            (x, y) tuple if entity has position, None otherwise

        Educational Note:
            Convenience method for getting position. While callers could
            get the PositionComponent directly, this method provides a
            simpler interface for common operations.

        Example:
            >>> system = MovementSystem(dungeon_map)
            >>> player = create_player(x=10, y=15)
            >>> x, y = system.get_position(player)
            >>> assert x == 10 and y == 15
        """
        position = entity.get_component(PositionComponent)
        if position:
            return position.get_position()
        return None

    def distance_between(self, entity1: Entity, entity2: Entity) -> Optional[float]:
        """
        Calculate distance between two entities.

        Args:
            entity1: First entity
            entity2: Second entity

        Returns:
            Euclidean distance, or None if either entity lacks position

        Educational Note:
            Distance calculations are fundamental for:
            - AI aggro ranges ("attack if player within 5 tiles")
            - Ranged weapon ranges
            - Area of effect abilities
            - Pathfinding heuristics

        Example:
            >>> system = MovementSystem(dungeon_map)
            >>> player = create_player(x=0, y=0)
            >>> enemy = create_enemy(x=3, y=4)
            >>> distance = system.distance_between(player, enemy)
            >>> assert distance == 5.0  # 3-4-5 triangle
        """
        pos1 = entity1.get_component(PositionComponent)
        pos2 = entity2.get_component(PositionComponent)

        if not pos1 or not pos2:
            return None

        return pos1.distance_to(pos2)

    def are_adjacent(self, entity1: Entity, entity2: Entity,
                     include_diagonal: bool = True) -> bool:
        """
        Check if two entities are adjacent.

        Args:
            entity1: First entity
            entity2: Second entity
            include_diagonal: Whether diagonal counts as adjacent

        Returns:
            True if entities are adjacent, False otherwise

        Educational Note:
            Adjacency is important for:
            - Melee combat (must be adjacent to attack)
            - Item pickup (must be adjacent to pick up)
            - Door interaction (must be adjacent to open/close)

        Example:
            >>> system = MovementSystem(dungeon_map)
            >>> player = create_player(x=5, y=5)
            >>> enemy = create_enemy(x=6, y=5)  # Right neighbor
            >>> assert system.are_adjacent(player, enemy) is True
        """
        pos1 = entity1.get_component(PositionComponent)
        pos2 = entity2.get_component(PositionComponent)

        if not pos1 or not pos2:
            return False

        return pos1.is_adjacent_to(pos2, include_diagonal=include_diagonal)
