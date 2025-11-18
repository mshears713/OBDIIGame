"""
Procedural Dungeon Generation System

This module implements algorithms for generating randomized dungeon layouts
with rooms and corridors.

Educational Notes:
------------------
Procedural generation is the algorithmic creation of content. Instead of
hand-designing every dungeon, we write algorithms that create varied,
playable dungeons automatically.

Benefits of Procedural Generation:
1. Replayability: Every playthrough is different
2. Scalability: Generate infinite content without manual work
3. Learning: Understanding algorithms and randomization
4. Surprise: Even developers don't know exact layouts

This implementation uses a simple room-and-corridor algorithm:
1. Generate random rooms (rectangles)
2. Connect rooms with corridors
3. Ensure all rooms are reachable

More advanced algorithms include:
- Binary Space Partitioning (BSP)
- Cellular Automata
- Drunkard's Walk
- Maze generation algorithms
"""

import random
from typing import List, Tuple, Optional
from dataclasses import dataclass
from src.models import Map, Tile, TileType


@dataclass
class Room:
    """
    Represents a rectangular room in the dungeon.

    Attributes:
        x1: Left edge X coordinate
        y1: Top edge Y coordinate
        x2: Right edge X coordinate
        y2: Bottom edge Y coordinate

    Educational Note:
        Rooms are defined by their top-left (x1, y1) and bottom-right (x2, y2)
        corners. This makes it easy to check if a point is inside a room or
        if two rooms intersect.

    Example:
        >>> room = Room(x1=5, y1=5, x2=15, y2=10)
        >>> # This creates a room from (5,5) to (15,10)
        >>> # Width: 10 tiles, Height: 5 tiles
        >>> assert room.width() == 10
        >>> assert room.height() == 5
    """
    x1: int
    y1: int
    x2: int
    y2: int

    def width(self) -> int:
        """Calculate room width."""
        return self.x2 - self.x1

    def height(self) -> int:
        """Calculate room height."""
        return self.y2 - self.y1

    def center(self) -> Tuple[int, int]:
        """
        Calculate the center point of the room.

        Returns:
            (center_x, center_y) tuple

        Educational Note:
            Center points are useful for:
            - Connecting rooms with corridors
            - Spawning player/enemies in room center
            - Placing important items/features

        Example:
            >>> room = Room(x1=0, y1=0, x2=10, y2=10)
            >>> cx, cy = room.center()
            >>> assert cx == 5 and cy == 5
        """
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return (center_x, center_y)

    def intersects(self, other: 'Room') -> bool:
        """
        Check if this room intersects with another room.

        Args:
            other: Another Room to check intersection with

        Returns:
            True if rooms overlap, False otherwise

        Educational Note:
            Rectangle intersection is a fundamental algorithm in games and graphics.
            Two rectangles intersect if they overlap in both X and Y dimensions.

            This check prevents rooms from overlapping during generation, which
            would create invalid/weird dungeon layouts.

        Example:
            >>> room1 = Room(x1=0, y1=0, x2=10, y2=10)
            >>> room2 = Room(x1=5, y1=5, x2=15, y2=15)  # Overlaps
            >>> assert room1.intersects(room2) is True
            >>>
            >>> room3 = Room(x1=20, y1=20, x2=30, y2=30)  # Far away
            >>> assert room1.intersects(room3) is False
        """
        # Rooms intersect if they overlap in both X and Y
        return (
            self.x1 <= other.x2 and self.x2 >= other.x1 and
            self.y1 <= other.y2 and self.y2 >= other.y1
        )

    def inner_tiles(self) -> List[Tuple[int, int]]:
        """
        Get all tile coordinates inside this room (excluding walls).

        Returns:
            List of (x, y) tuples for floor tiles

        Educational Note:
            We typically want room interiors to be walkable floors.
            This method returns all coordinates that should be floor tiles,
            excluding the outer walls.

        Example:
            >>> room = Room(x1=5, y1=5, x2=8, y2=7)
            >>> tiles = room.inner_tiles()
            >>> # Returns tiles from (6,6) to (7,6) - the interior
        """
        tiles = []
        for y in range(self.y1 + 1, self.y2):
            for x in range(self.x1 + 1, self.x2):
                tiles.append((x, y))
        return tiles

    def all_tiles(self) -> List[Tuple[int, int]]:
        """
        Get all tile coordinates in this room (including walls).

        Returns:
            List of (x, y) tuples for all tiles

        Educational Note:
            Sometimes we want all tiles including walls, for example when
            checking if rooms are too close together (should have space
            between them for corridors).
        """
        tiles = []
        for y in range(self.y1, self.y2 + 1):
            for x in range(self.x1, self.x2 + 1):
                tiles.append((x, y))
        return tiles


class DungeonGenerator:
    """
    Generates procedural dungeons using room-and-corridor algorithm.

    This generator creates dungeons by:
    1. Attempting to place random rectangular rooms
    2. Connecting rooms with corridors (horizontal + vertical tunnels)
    3. Ensuring connectivity between all rooms

    Educational Note:
        The algorithm is intentionally simple for learning purposes.
        More sophisticated generators might use:
        - BSP (Binary Space Partitioning) for guaranteed room placement
        - Pathfinding algorithms for smarter corridors
        - Multiple room shapes (L-shaped, circular, irregular)
        - Varying corridor widths and styles
    """

    def __init__(
        self,
        width: int,
        height: int,
        max_rooms: int = 30,
        min_room_size: int = 6,
        max_room_size: int = 10,
        random_seed: Optional[int] = None
    ):
        """
        Initialize dungeon generator.

        Args:
            width: Dungeon width in tiles
            height: Dungeon height in tiles
            max_rooms: Maximum number of rooms to attempt
            min_room_size: Minimum room dimension (width or height)
            max_room_size: Maximum room dimension (width or height)
            random_seed: Optional seed for reproducible generation

        Educational Note:
            Providing a random seed makes generation deterministic, which is
            useful for:
            - Testing (same seed = same dungeon every time)
            - Sharing dungeons (share the seed number)
            - Debugging generation issues

            Setting random_seed=None uses system time, creating different
            dungeons each run.

        Example:
            >>> # Create generator with specific seed
            >>> gen = DungeonGenerator(width=50, height=30, random_seed=12345)
            >>> dungeon1 = gen.generate()
            >>>
            >>> # Same seed produces identical dungeon
            >>> gen2 = DungeonGenerator(width=50, height=30, random_seed=12345)
            >>> dungeon2 = gen2.generate()
            >>> # dungeon1 and dungeon2 are identical
        """
        self.width = width
        self.height = height
        self.max_rooms = max_rooms
        self.min_room_size = min_room_size
        self.max_room_size = max_room_size

        # Set random seed if provided
        if random_seed is not None:
            random.seed(random_seed)

        # Storage for generated rooms
        self.rooms: List[Room] = []

    def generate(self) -> Map:
        """
        Generate a complete dungeon map.

        Returns:
            Map object with procedurally generated dungeon

        Educational Note:
            This is the main entry point for dungeon generation.
            The algorithm:
            1. Create empty map (all walls)
            2. Try to place rooms randomly
            3. Connect each room to the previous one
            4. Place stairs in first and last rooms

        Example:
            >>> generator = DungeonGenerator(width=50, height=30)
            >>> dungeon_map = generator.generate()
            >>> # Returns a Map with rooms and corridors
        """
        # Create new map filled with walls
        dungeon_map = Map(width=self.width, height=self.height)
        dungeon_map.initialize_empty(fill_tile=Tile.create_wall())

        # Reset rooms list
        self.rooms = []

        # Attempt to place rooms
        for _ in range(self.max_rooms):
            # Generate random room dimensions
            room_width = random.randint(self.min_room_size, self.max_room_size)
            room_height = random.randint(self.min_room_size, self.max_room_size)

            # Generate random position (with boundary padding)
            x = random.randint(1, self.width - room_width - 1)
            y = random.randint(1, self.height - room_height - 1)

            # Create new room
            new_room = Room(x1=x, y1=y, x2=x + room_width, y2=y + room_height)

            # Check if room intersects with existing rooms
            intersects = any(new_room.intersects(other) for other in self.rooms)

            if not intersects:
                # Room is valid, carve it out
                self._carve_room(dungeon_map, new_room)

                # Connect to previous room with a corridor
                if len(self.rooms) > 0:
                    # Get centers of new room and previous room
                    new_x, new_y = new_room.center()
                    prev_x, prev_y = self.rooms[-1].center()

                    # Randomly choose corridor direction (horizontal first or vertical first)
                    if random.random() < 0.5:
                        # Horizontal then vertical
                        self._carve_horizontal_corridor(dungeon_map, prev_x, new_x, prev_y)
                        self._carve_vertical_corridor(dungeon_map, prev_y, new_y, new_x)
                    else:
                        # Vertical then horizontal
                        self._carve_vertical_corridor(dungeon_map, prev_y, new_y, prev_x)
                        self._carve_horizontal_corridor(dungeon_map, prev_x, new_x, new_y)

                # Add room to list
                self.rooms.append(new_room)

        # Place stairs in first and last rooms
        if len(self.rooms) > 0:
            # Stairs up in first room
            first_center = self.rooms[0].center()
            dungeon_map.set_tile(first_center[0], first_center[1], Tile.create_stairs_up())

            # Stairs down in last room
            last_center = self.rooms[-1].center()
            dungeon_map.set_tile(last_center[0], last_center[1], Tile.create_stairs_down())

        return dungeon_map

    def _carve_room(self, dungeon_map: Map, room: Room) -> None:
        """
        Carve out a room by setting interior tiles to floor.

        Args:
            dungeon_map: Map to modify
            room: Room to carve out

        Educational Note:
            "Carving" means replacing wall tiles with floor tiles.
            We iterate through the room's interior coordinates and set
            them to walkable floor tiles.

            We typically leave the outer edge as walls to create room
            boundaries, but the corridor connections will punch through these.
        """
        for x, y in room.inner_tiles():
            dungeon_map.set_tile(x, y, Tile.create_floor())

    def _carve_horizontal_corridor(self, dungeon_map: Map, x1: int, x2: int, y: int) -> None:
        """
        Carve a horizontal corridor from x1 to x2 at row y.

        Args:
            dungeon_map: Map to modify
            x1: Starting X coordinate
            x2: Ending X coordinate
            y: Y coordinate (row) for corridor

        Educational Note:
            Corridors connect rooms. This creates a horizontal tunnel
            by setting tiles to floor along a row.

            We use min/max to handle both left-to-right and right-to-left
            corridors without caring about direction.

        Example:
            If x1=5, x2=15, y=10, this creates a horizontal corridor
            from (5,10) to (15,10).
        """
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if dungeon_map.is_in_bounds(x, y):
                dungeon_map.set_tile(x, y, Tile.create_floor())

    def _carve_vertical_corridor(self, dungeon_map: Map, y1: int, y2: int, x: int) -> None:
        """
        Carve a vertical corridor from y1 to y2 at column x.

        Args:
            dungeon_map: Map to modify
            y1: Starting Y coordinate
            y2: Ending Y coordinate
            x: X coordinate (column) for corridor

        Educational Note:
            Similar to horizontal corridors but vertical.
            Creates a tunnel along a column connecting different rows.

        Example:
            If y1=5, y2=15, x=10, this creates a vertical corridor
            from (10,5) to (10,15).
        """
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if dungeon_map.is_in_bounds(x, y):
                dungeon_map.set_tile(x, y, Tile.create_floor())

    def get_rooms(self) -> List[Room]:
        """
        Get list of generated rooms.

        Returns:
            List of Room objects created during last generation

        Educational Note:
            Rooms are useful for:
            - Spawning enemies (place enemies in rooms)
            - Placing items (put treasure in random room)
            - Player spawn point (start in first room)
            - Quest objectives (reach last room)

        Example:
            >>> generator = DungeonGenerator(width=50, height=30)
            >>> dungeon_map = generator.generate()
            >>> rooms = generator.get_rooms()
            >>> # Spawn player in center of first room
            >>> player_x, player_y = rooms[0].center()
        """
        return self.rooms

    def get_random_room(self) -> Optional[Room]:
        """
        Get a random room from the generated dungeon.

        Returns:
            Random Room, or None if no rooms exist

        Educational Note:
            Useful for randomly placing entities or items in the dungeon.

        Example:
            >>> generator = DungeonGenerator(width=50, height=30)
            >>> dungeon_map = generator.generate()
            >>> random_room = generator.get_random_room()
            >>> if random_room:
            >>>     # Spawn enemy in this room
            >>>     enemy_x, enemy_y = random_room.center()
        """
        if not self.rooms:
            return None
        return random.choice(self.rooms)

    def get_random_floor_tile(self, dungeon_map: Map) -> Optional[Tuple[int, int]]:
        """
        Get coordinates of a random walkable floor tile.

        Args:
            dungeon_map: The generated map to search

        Returns:
            (x, y) tuple of random floor tile, or None if none exist

        Educational Note:
            Sometimes we want to place something on any valid floor tile,
            not necessarily in room centers. This method finds a random
            walkable position.

            Implementation: We iterate through all tiles and collect floor
            positions, then return a random one. For large maps, more
            efficient approaches exist (e.g., pick random room, then random
            tile in that room).

        Example:
            >>> generator = DungeonGenerator(width=50, height=30)
            >>> dungeon_map = generator.generate()
            >>> item_x, item_y = generator.get_random_floor_tile(dungeon_map)
            >>> # Place item at this random walkable position
        """
        floor_tiles = []

        for y in range(dungeon_map.height):
            for x in range(dungeon_map.width):
                if dungeon_map.is_walkable(x, y):
                    floor_tiles.append((x, y))

        if not floor_tiles:
            return None

        return random.choice(floor_tiles)
