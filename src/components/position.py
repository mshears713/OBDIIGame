"""
PositionComponent - Spatial location component for entities

This component represents an entity's position in 2D space within the dungeon.

Educational Notes:
------------------
The PositionComponent is one of the most fundamental components in a 2D game.
It allows systems to:
- Determine where to render entities (RenderSystem)
- Calculate distances between entities (AI, Combat systems)
- Validate movement (MovementSystem)
- Detect collisions (CollisionSystem)

This component stores only position data - no logic for movement or collision.
Those behaviors are handled by separate systems operating on this component.
"""

from src.components.base import Component
from typing import Dict, Any, Tuple


class PositionComponent(Component):
    """
    Component storing an entity's position in 2D dungeon space.

    Attributes:
        x: X coordinate (column) in the dungeon grid
        y: Y coordinate (row) in the dungeon grid

    Educational Note:
        We use (x, y) convention where:
        - x = 0 is the leftmost column
        - y = 0 is the topmost row
        - Increasing x moves right
        - Increasing y moves down

        This matches standard 2D array indexing: array[y][x]

    Example:
        >>> position = PositionComponent(x=10, y=5)
        >>> # Entity is at column 10, row 5
        >>> position.move(dx=1, dy=0)  # Move one tile right
        >>> assert position.x == 11
    """

    def __init__(self, x: int = 0, y: int = 0):
        """
        Initialize position component.

        Args:
            x: Initial X coordinate (default 0)
            y: Initial Y coordinate (default 0)

        Educational Note:
            Providing default values (0, 0) allows creating a position without
            arguments, which can be useful during entity construction.
        """
        super().__init__()
        self.x = x
        self.y = y

    def get_position(self) -> Tuple[int, int]:
        """
        Get the current position as a tuple.

        Returns:
            (x, y) tuple of current coordinates

        Educational Note:
            Returning a tuple is convenient for unpacking:
                x, y = position.get_position()

            It's also useful for functions that expect coordinate tuples.

        Example:
            >>> pos = PositionComponent(x=5, y=10)
            >>> coords = pos.get_position()
            >>> print(f"Entity at {coords}")
            Entity at (5, 10)
        """
        return (self.x, self.y)

    def set_position(self, x: int, y: int) -> None:
        """
        Set the position to new coordinates.

        Args:
            x: New X coordinate
            y: New Y coordinate

        Educational Note:
            This method provides a clean interface for teleporting or spawning
            entities at specific locations. For gradual movement, use move().

        Example:
            >>> pos = PositionComponent()
            >>> pos.set_position(15, 20)
            >>> assert pos.x == 15 and pos.y == 20
        """
        self.x = x
        self.y = y

    def move(self, dx: int, dy: int) -> None:
        """
        Move the entity by a relative offset.

        Args:
            dx: Change in X coordinate (positive = right, negative = left)
            dy: Change in Y coordinate (positive = down, negative = up)

        Educational Note:
            Relative movement is common in games. Players press arrow keys
            which translate to delta values:
                Up: dx=0, dy=-1
                Down: dx=0, dy=1
                Left: dx=-1, dy=0
                Right: dx=1, dy=0

            Note: This method doesn't validate boundaries or collisions.
            The MovementSystem should handle those checks before calling move().

        Example:
            >>> pos = PositionComponent(x=10, y=10)
            >>> pos.move(dx=2, dy=-3)  # Move 2 right, 3 up
            >>> assert pos.x == 12 and pos.y == 7
        """
        self.x += dx
        self.y += dy

    def distance_to(self, other: 'PositionComponent') -> float:
        """
        Calculate Euclidean distance to another position.

        Args:
            other: Another PositionComponent to measure distance to

        Returns:
            Euclidean distance as a float

        Educational Note:
            Euclidean distance is the straight-line distance between two points:
                distance = sqrt((x2-x1)² + (y2-y1)²)

            Useful for:
            - AI aggro range ("attack if player within 5 tiles")
            - Area-of-effect calculations
            - Pathfinding heuristics

        Example:
            >>> pos1 = PositionComponent(x=0, y=0)
            >>> pos2 = PositionComponent(x=3, y=4)
            >>> dist = pos1.distance_to(pos2)
            >>> assert dist == 5.0  # 3-4-5 right triangle
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx * dx + dy * dy) ** 0.5

    def manhattan_distance_to(self, other: 'PositionComponent') -> int:
        """
        Calculate Manhattan (taxicab) distance to another position.

        Args:
            other: Another PositionComponent to measure distance to

        Returns:
            Manhattan distance as an integer

        Educational Note:
            Manhattan distance is the sum of horizontal and vertical distances:
                distance = |x2-x1| + |y2-y1|

            Also called "taxicab distance" because it's like driving on a city
            grid - you can't cut diagonally through buildings.

            Useful for:
            - Grid-based movement where diagonal moves aren't allowed
            - Simpler/faster calculation than Euclidean distance
            - More intuitive for tile-based movement

        Example:
            >>> pos1 = PositionComponent(x=0, y=0)
            >>> pos2 = PositionComponent(x=3, y=4)
            >>> dist = pos1.manhattan_distance_to(pos2)
            >>> assert dist == 7  # 3 + 4
        """
        return abs(self.x - other.x) + abs(self.y - other.y)

    def is_adjacent_to(self, other: 'PositionComponent',
                       include_diagonal: bool = True) -> bool:
        """
        Check if this position is adjacent to another position.

        Args:
            other: Another PositionComponent to check adjacency with
            include_diagonal: Whether diagonal positions count as adjacent

        Returns:
            True if positions are adjacent, False otherwise

        Educational Note:
            Adjacency is important for:
            - Melee combat (can only attack adjacent enemies)
            - Item pickup (must be next to item)
            - Door opening (must be adjacent to door)

            With diagonals: 8 adjacent tiles (Moore neighborhood)
            Without diagonals: 4 adjacent tiles (Von Neumann neighborhood)

        Example:
            >>> pos1 = PositionComponent(x=5, y=5)
            >>> pos2 = PositionComponent(x=6, y=5)  # Right neighbor
            >>> assert pos1.is_adjacent_to(pos2) is True
            >>>
            >>> pos3 = PositionComponent(x=6, y=6)  # Diagonal
            >>> assert pos1.is_adjacent_to(pos3, include_diagonal=True) is True
            >>> assert pos1.is_adjacent_to(pos3, include_diagonal=False) is False
        """
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)

        if include_diagonal:
            # Adjacent if within 1 tile in any direction (including diagonal)
            return dx <= 1 and dy <= 1 and (dx != 0 or dy != 0)
        else:
            # Adjacent only in cardinal directions (no diagonal)
            return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)

    def __eq__(self, other: object) -> bool:
        """
        Check if two positions are equal.

        Args:
            other: Another object to compare with

        Returns:
            True if other is a PositionComponent with same coordinates

        Educational Note:
            Implementing __eq__ allows using == to compare positions.
            Useful for checking if an entity reached a target location.

        Example:
            >>> pos1 = PositionComponent(x=5, y=10)
            >>> pos2 = PositionComponent(x=5, y=10)
            >>> assert pos1 == pos2
        """
        if not isinstance(other, PositionComponent):
            return False
        return self.x == other.x and self.y == other.y

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize position to dictionary.

        Returns:
            Dictionary with component_type, x, and y

        Educational Note:
            Override from base Component class for explicit control.
            The base implementation would work, but this is more explicit.
        """
        return {
            'component_type': self.component_type,
            'x': self.x,
            'y': self.y
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PositionComponent':
        """
        Deserialize position from dictionary.

        Args:
            data: Dictionary containing x and y coordinates

        Returns:
            New PositionComponent instance

        Example:
            >>> data = {'x': 15, 'y': 20}
            >>> pos = PositionComponent.from_dict(data)
            >>> assert pos.x == 15 and pos.y == 20
        """
        return cls(x=data.get('x', 0), y=data.get('y', 0))
