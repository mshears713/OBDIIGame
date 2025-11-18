"""
Core Data Models for Dungeon Representation

This module defines immutable data structures for dungeon tiles and maps using
Python's dataclass feature, which reduces boilerplate and improves readability.

Educational Notes:
- Dataclasses (Python 3.7+) automatically generate __init__, __repr__, __eq__
  and other special methods, reducing code while maintaining clarity
- Type hints improve code documentation and enable static type checking
- Immutable data (frozen=True) prevents accidental modifications and bugs
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum, auto


class TileType(Enum):
    """
    Enumeration of possible tile types in the dungeon.

    Educational Note:
        Using Enum instead of raw strings/integers provides type safety and
        prevents typos. The auto() function automatically assigns unique values.

        Enums are excellent for representing fixed sets of related constants,
        making code more maintainable and self-documenting.
    """
    FLOOR = auto()  # Walkable floor tile
    WALL = auto()   # Solid wall blocking movement and vision
    DOOR = auto()   # Passable door (can be opened/closed in future phases)
    STAIRS_DOWN = auto()  # Stairs leading to next floor
    STAIRS_UP = auto()    # Stairs leading to previous floor
    HAZARD = auto()       # Dangerous tile (electrical interference, etc.)


@dataclass(frozen=True)
class Tile:
    """
    Immutable representation of a single dungeon tile.

    This class encapsulates all properties of a single cell in the dungeon grid,
    including its type, traversability, and visual representation.

    Attributes:
        tile_type: The type of tile (floor, wall, etc.)
        walkable: Can entities move through this tile?
        blocks_sight: Does this tile block line of sight?
        ascii_char: Character used to render this tile
        name: Human-readable name for this tile type
        description: Flavor text describing the tile (for educational tooltips)

    Educational Notes:
        - frozen=True makes this dataclass immutable (like a tuple)
        - Immutability prevents bugs from accidental state changes
        - All fields have type hints for better IDE support and documentation
        - Default values allow creating tiles with minimal parameters

    Example:
        >>> floor_tile = Tile.create_floor()
        >>> print(floor_tile.ascii_char)
        '.'
        >>> wall_tile = Tile.create_wall()
        >>> print(wall_tile.walkable)
        False
    """
    tile_type: TileType
    walkable: bool
    blocks_sight: bool
    ascii_char: str
    name: str = ""
    description: str = ""

    # Factory methods for common tile types
    # Educational Note: Factory methods provide convenient, self-documenting
    # ways to create common object configurations

    @staticmethod
    def create_floor() -> 'Tile':
        """Create a standard floor tile (walkable, doesn't block sight)."""
        return Tile(
            tile_type=TileType.FLOOR,
            walkable=True,
            blocks_sight=False,
            ascii_char='.',
            name="Floor",
            description="A standard floor tile in the ECU system."
        )

    @staticmethod
    def create_wall() -> 'Tile':
        """Create a standard wall tile (blocks movement and sight)."""
        return Tile(
            tile_type=TileType.WALL,
            walkable=False,
            blocks_sight=True,
            ascii_char='#',
            name="Wall",
            description="A solid wall blocking passage through the system."
        )

    @staticmethod
    def create_door() -> 'Tile':
        """Create a door tile (walkable, doesn't block sight)."""
        return Tile(
            tile_type=TileType.DOOR,
            walkable=True,
            blocks_sight=False,
            ascii_char='+',
            name="Door",
            description="A doorway connecting different areas."
        )

    @staticmethod
    def create_stairs_down() -> 'Tile':
        """Create stairs leading to the next floor."""
        return Tile(
            tile_type=TileType.STAIRS_DOWN,
            walkable=True,
            blocks_sight=False,
            ascii_char='>',
            name="Stairs Down",
            description="Stairs leading deeper into the ECU system."
        )

    @staticmethod
    def create_stairs_up() -> 'Tile':
        """Create stairs leading to the previous floor."""
        return Tile(
            tile_type=TileType.STAIRS_UP,
            walkable=True,
            blocks_sight=False,
            ascii_char='<',
            name="Stairs Up",
            description="Stairs leading back to the previous level."
        )

    @staticmethod
    def create_hazard() -> 'Tile':
        """Create a hazardous tile (walkable but dangerous)."""
        return Tile(
            tile_type=TileType.HAZARD,
            walkable=True,
            blocks_sight=False,
            ascii_char='^',
            name="Hazard",
            description="Electrical interference - dangerous to traverse!"
        )


@dataclass
class Map:
    """
    Mutable representation of a dungeon floor containing a 2D grid of tiles.

    The Map class manages the entire dungeon layout, providing methods to
    access and query tiles at specific coordinates.

    Attributes:
        width: Width of the map in tiles
        height: Height of the map in tiles
        tiles: 2D list of Tile objects [y][x] (row-major order)
        floor_id: Unique identifier for this floor
        floor_name: Human-readable name of the floor
        theme: Visual/mechanical theme (e.g., "can_bus", "fuel_injection")

    Educational Notes:
        - Unlike Tile, Map is mutable (not frozen) because we need to modify
          tiles during dungeon generation and gameplay
        - The tiles list uses field(default_factory=list) to avoid the common
          mutable default argument pitfall
        - 2D arrays are stored as list[list[Tile]] for simplicity; more advanced
          implementations might use numpy for performance

    Example:
        >>> dungeon_map = Map(width=50, height=30, floor_id=1)
        >>> dungeon_map.initialize_empty()
        >>> tile = dungeon_map.get_tile(5, 10)
    """
    width: int
    height: int
    tiles: List[List[Tile]] = field(default_factory=list)
    floor_id: int = 1
    floor_name: str = "Unnamed Floor"
    theme: str = "default"

    def __post_init__(self):
        """
        Initialize the tiles list if not provided.

        Educational Note:
            __post_init__ is a special dataclass method that runs after the
            automatically generated __init__. It's useful for validation or
            initialization that depends on the values of fields.
        """
        if not self.tiles:
            # If no tiles provided, create an empty list structure
            # We'll fill this in initialize_empty() or during generation
            self.tiles = []

    def initialize_empty(self, fill_tile: Optional[Tile] = None) -> None:
        """
        Initialize the map with empty tiles (walls by default).

        Args:
            fill_tile: The tile to fill the map with (defaults to wall)

        Educational Note:
            This method demonstrates list comprehension for creating 2D arrays.
            We create height rows, each containing width columns.
            Using a factory method ensures each position gets a unique Tile
            instance (important even though Tiles are frozen).
        """
        if fill_tile is None:
            fill_tile = Tile.create_wall()

        # Create 2D grid: list of rows, each row is a list of tiles
        # tiles[y][x] means tiles[row][column]
        self.tiles = [
            [fill_tile for x in range(self.width)]
            for y in range(self.height)
        ]

    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        """
        Safely retrieve a tile at the given coordinates.

        Args:
            x: X coordinate (column)
            y: Y coordinate (row)

        Returns:
            The Tile at (x, y), or None if coordinates are out of bounds

        Educational Note:
            Boundary checking prevents index errors and crashes. Always validate
            coordinates when working with grid-based games. Returning None
            allows callers to handle invalid coordinates gracefully.
        """
        if not self.is_in_bounds(x, y):
            return None
        return self.tiles[y][x]

    def set_tile(self, x: int, y: int, tile: Tile) -> bool:
        """
        Set a tile at the given coordinates.

        Args:
            x: X coordinate (column)
            y: Y coordinate (row)
            tile: The Tile to place at this position

        Returns:
            True if successful, False if coordinates out of bounds

        Educational Note:
            Returning a boolean success indicator allows callers to detect
            and handle errors without catching exceptions. This is a common
            pattern for operations that might fail for expected reasons.
        """
        if not self.is_in_bounds(x, y):
            return False
        self.tiles[y][x] = tile
        return True

    def is_in_bounds(self, x: int, y: int) -> bool:
        """
        Check if coordinates are within map boundaries.

        Args:
            x: X coordinate to check
            y: Y coordinate to check

        Returns:
            True if coordinates are valid, False otherwise

        Educational Note:
            Extracting boundary checking into a separate method follows the
            DRY (Don't Repeat Yourself) principle and makes the code more
            maintainable. If boundary logic changes, we only update one place.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def is_walkable(self, x: int, y: int) -> bool:
        """
        Check if a tile at given coordinates is walkable.

        Args:
            x: X coordinate to check
            y: Y coordinate to check

        Returns:
            True if tile exists and is walkable, False otherwise

        Educational Note:
            This convenience method encapsulates common game logic queries.
            By centralizing this check, we ensure consistent behavior across
            all systems that need to validate movement.
        """
        tile = self.get_tile(x, y)
        return tile is not None and tile.walkable

    def is_blocked_sight(self, x: int, y: int) -> bool:
        """
        Check if a tile blocks line of sight.

        Args:
            x: X coordinate to check
            y: Y coordinate to check

        Returns:
            True if tile blocks sight, False if sight passes through

        Educational Note:
            Sight blocking is important for fog-of-war and stealth mechanics.
            Separating this from walkability allows for interesting gameplay:
            glass walls block movement but not sight, for example.
        """
        tile = self.get_tile(x, y)
        # Out of bounds blocks sight (can't see through the void)
        if tile is None:
            return True
        return tile.blocks_sight

    def get_dimensions(self) -> tuple[int, int]:
        """
        Get the map dimensions as a tuple.

        Returns:
            (width, height) tuple

        Educational Note:
            Returning dimensions as a tuple is convenient for unpacking:
            w, h = map.get_dimensions()
        """
        return (self.width, self.height)
