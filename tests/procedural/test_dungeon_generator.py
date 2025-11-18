"""
Tests for Procedural Dungeon Generation

Educational Notes:
------------------
Testing procedural generation is tricky because output is randomized.
We test by:
1. Using fixed seeds for reproducibility
2. Testing invariants (properties that should always be true)
3. Checking statistical properties over multiple runs
4. Validating structure (connectivity, playability)
"""

import pytest
from src.procedural.dungeon_generator import DungeonGenerator, Room
from src.models import Map, TileType


class TestRoom:
    """Test the Room data class."""

    def test_room_initialization(self):
        """Test Room creates with correct coordinates."""
        room = Room(x1=5, y1=10, x2=15, y2=20)
        assert room.x1 == 5
        assert room.y1 == 10
        assert room.x2 == 15
        assert room.y2 == 20

    def test_room_width(self):
        """Test room width calculation."""
        room = Room(x1=5, y1=10, x2=15, y2=20)
        assert room.width() == 10

    def test_room_height(self):
        """Test room height calculation."""
        room = Room(x1=5, y1=10, x2=15, y2=20)
        assert room.height() == 10

    def test_room_center(self):
        """Test room center calculation."""
        room = Room(x1=0, y1=0, x2=10, y2=10)
        center_x, center_y = room.center()
        assert center_x == 5
        assert center_y == 5

    def test_room_center_odd_dimensions(self):
        """Test center calculation with odd dimensions (uses floor division)."""
        room = Room(x1=0, y1=0, x2=11, y2=11)
        center_x, center_y = room.center()
        assert center_x == 5  # (0 + 11) // 2 = 5
        assert center_y == 5

    def test_room_intersects_overlapping(self):
        """Test intersection detection for overlapping rooms."""
        room1 = Room(x1=0, y1=0, x2=10, y2=10)
        room2 = Room(x1=5, y1=5, x2=15, y2=15)  # Overlaps
        assert room1.intersects(room2) is True
        assert room2.intersects(room1) is True  # Symmetric

    def test_room_intersects_separate(self):
        """Test intersection detection for separate rooms."""
        room1 = Room(x1=0, y1=0, x2=10, y2=10)
        room2 = Room(x1=20, y1=20, x2=30, y2=30)  # Far apart
        assert room1.intersects(room2) is False
        assert room2.intersects(room1) is False

    def test_room_intersects_adjacent(self):
        """Test intersection for adjacent (touching) rooms."""
        room1 = Room(x1=0, y1=0, x2=10, y2=10)
        room2 = Room(x1=10, y1=0, x2=20, y2=10)  # Shares edge at x=10
        # Rooms sharing an edge should intersect (inclusive bounds)
        assert room1.intersects(room2) is True

    def test_room_inner_tiles(self):
        """Test getting interior tiles (excluding walls)."""
        room = Room(x1=5, y1=5, x2=8, y2=8)
        inner = room.inner_tiles()

        # Interior should be 2x2 = 4 tiles
        # x from 6 to 7, y from 6 to 7
        assert len(inner) == 4
        assert (6, 6) in inner
        assert (7, 6) in inner
        assert (6, 7) in inner
        assert (7, 7) in inner

        # Edges should not be included
        assert (5, 5) not in inner  # Corner
        assert (8, 8) not in inner  # Corner

    def test_room_all_tiles(self):
        """Test getting all tiles including walls."""
        room = Room(x1=5, y1=5, x2=7, y2=7)
        all_tiles = room.all_tiles()

        # Should be 3x3 = 9 tiles
        assert len(all_tiles) == 9

        # Check corners included
        assert (5, 5) in all_tiles
        assert (7, 7) in all_tiles


class TestDungeonGenerator:
    """Test the DungeonGenerator class."""

    def test_generator_initialization(self):
        """Test generator creates with correct parameters."""
        gen = DungeonGenerator(
            width=50,
            height=30,
            max_rooms=10,
            min_room_size=5,
            max_room_size=12
        )
        assert gen.width == 50
        assert gen.height == 30
        assert gen.max_rooms == 10
        assert gen.min_room_size == 5
        assert gen.max_room_size == 12

    def test_generate_creates_map(self):
        """Test that generate() returns a Map object."""
        gen = DungeonGenerator(width=50, height=30)
        dungeon = gen.generate()

        assert isinstance(dungeon, Map)
        assert dungeon.width == 50
        assert dungeon.height == 30

    def test_generate_with_seed_is_deterministic(self):
        """Test that same seed produces identical dungeons."""
        # Generate first dungeon
        gen1 = DungeonGenerator(width=50, height=30, random_seed=12345)
        dungeon1 = gen1.generate()

        # Generate second dungeon with same seed
        gen2 = DungeonGenerator(width=50, height=30, random_seed=12345)
        dungeon2 = gen2.generate()

        # Dungeons should be identical
        for y in range(30):
            for x in range(50):
                tile1 = dungeon1.get_tile(x, y)
                tile2 = dungeon2.get_tile(x, y)
                assert tile1.tile_type == tile2.tile_type

    def test_generate_creates_rooms(self):
        """Test that generation creates some rooms."""
        gen = DungeonGenerator(width=50, height=30, max_rooms=20, random_seed=42)
        dungeon = gen.generate()
        rooms = gen.get_rooms()

        # Should create at least some rooms
        assert len(rooms) > 0

    def test_rooms_do_not_overlap(self):
        """Test that generated rooms don't intersect."""
        gen = DungeonGenerator(width=80, height=50, max_rooms=30, random_seed=42)
        dungeon = gen.generate()
        rooms = gen.get_rooms()

        # Check all pairs of rooms
        for i, room1 in enumerate(rooms):
            for room2 in rooms[i+1:]:
                # Rooms should not intersect
                assert not room1.intersects(room2), \
                    f"Rooms overlap: {room1} and {room2}"

    def test_dungeon_has_walkable_tiles(self):
        """Test that dungeon contains walkable floor tiles."""
        gen = DungeonGenerator(width=50, height=30, random_seed=42)
        dungeon = gen.generate()

        # Count walkable tiles
        walkable_count = 0
        for y in range(dungeon.height):
            for x in range(dungeon.width):
                if dungeon.is_walkable(x, y):
                    walkable_count += 1

        # Should have some walkable tiles (rooms and corridors)
        assert walkable_count > 0

    def test_dungeon_has_walls(self):
        """Test that dungeon contains wall tiles."""
        gen = DungeonGenerator(width=50, height=30, random_seed=42)
        dungeon = gen.generate()

        # Count wall tiles
        wall_count = 0
        for y in range(dungeon.height):
            for x in range(dungeon.width):
                tile = dungeon.get_tile(x, y)
                if tile.tile_type == TileType.WALL:
                    wall_count += 1

        # Should have walls (not all floor)
        assert wall_count > 0

    def test_stairs_placed_in_dungeon(self):
        """Test that stairs up and down are placed."""
        gen = DungeonGenerator(width=50, height=30, max_rooms=10, random_seed=42)
        dungeon = gen.generate()

        # Count stairs
        stairs_up_count = 0
        stairs_down_count = 0

        for y in range(dungeon.height):
            for x in range(dungeon.width):
                tile = dungeon.get_tile(x, y)
                if tile.tile_type == TileType.STAIRS_UP:
                    stairs_up_count += 1
                elif tile.tile_type == TileType.STAIRS_DOWN:
                    stairs_down_count += 1

        # Should have exactly one of each (in first and last room)
        assert stairs_up_count == 1, "Should have exactly one stairs up"
        assert stairs_down_count == 1, "Should have exactly one stairs down"

    def test_get_random_room(self):
        """Test getting a random room."""
        gen = DungeonGenerator(width=50, height=30, random_seed=42)
        dungeon = gen.generate()

        random_room = gen.get_random_room()

        # Should return a room
        assert random_room is not None
        assert isinstance(random_room, Room)

        # Room should be in the rooms list
        assert random_room in gen.get_rooms()

    def test_get_random_room_empty_dungeon(self):
        """Test get_random_room with no rooms (edge case)."""
        gen = DungeonGenerator(width=10, height=10, max_rooms=0)
        dungeon = gen.generate()

        random_room = gen.get_random_room()

        # Should return None when no rooms exist
        assert random_room is None

    def test_get_random_floor_tile(self):
        """Test getting random floor tile coordinates."""
        gen = DungeonGenerator(width=50, height=30, random_seed=42)
        dungeon = gen.generate()

        tile_coords = gen.get_random_floor_tile(dungeon)

        # Should return coordinates
        assert tile_coords is not None
        x, y = tile_coords

        # Coordinates should be in bounds
        assert 0 <= x < dungeon.width
        assert 0 <= y < dungeon.height

        # Tile at those coordinates should be walkable
        assert dungeon.is_walkable(x, y)

    def test_room_size_constraints(self):
        """Test that generated rooms respect size constraints."""
        min_size = 6
        max_size = 10
        gen = DungeonGenerator(
            width=80,
            height=50,
            max_rooms=30,
            min_room_size=min_size,
            max_room_size=max_size,
            random_seed=42
        )
        dungeon = gen.generate()
        rooms = gen.get_rooms()

        for room in rooms:
            # Room dimensions should be within constraints
            assert room.width() >= min_size
            assert room.width() <= max_size
            assert room.height() >= min_size
            assert room.height() <= max_size

    def test_rooms_within_bounds(self):
        """Test that all rooms are within map boundaries."""
        gen = DungeonGenerator(width=50, height=30, random_seed=42)
        dungeon = gen.generate()
        rooms = gen.get_rooms()

        for room in rooms:
            # Room should be completely within map bounds
            assert room.x1 >= 0
            assert room.y1 >= 0
            assert room.x2 < dungeon.width
            assert room.y2 < dungeon.height

    def test_multiple_generations_produce_different_results(self):
        """Test that generating without seed produces varied dungeons."""
        gen1 = DungeonGenerator(width=50, height=30)
        dungeon1 = gen1.generate()
        rooms1 = gen1.get_rooms()

        gen2 = DungeonGenerator(width=50, height=30)
        dungeon2 = gen2.generate()
        rooms2 = gen2.get_rooms()

        # Without fixed seeds, dungeons should likely be different
        # Check room count or positions differ
        different = (
            len(rooms1) != len(rooms2) or
            (len(rooms1) > 0 and rooms1[0].center() != rooms2[0].center())
        )

        # Note: This test has small chance of false positive if random
        # generations happen to match, but probability is very low
        assert different, "Two unseeded generations should produce different dungeons"


class TestDungeonConnectivity:
    """
    Tests for dungeon connectivity and playability.

    Educational Note:
        A playable dungeon must be connected - the player should be able
        to reach all rooms. These tests verify structural integrity.
    """

    def test_dungeon_has_path_between_rooms(self):
        """
        Test that there's a walkable path between consecutive rooms.

        Educational Note:
            This is a simplified connectivity test. We verify corridors
            connect adjacent rooms by checking walkability along the
            corridor path. A more robust test would use pathfinding.
        """
        gen = DungeonGenerator(width=80, height=50, max_rooms=10, random_seed=42)
        dungeon = gen.generate()
        rooms = gen.get_rooms()

        if len(rooms) < 2:
            pytest.skip("Not enough rooms generated for connectivity test")

        # Check that consecutive rooms have walkable tiles between them
        # This is a weak test - just verifies some floor exists
        # Better test would use actual pathfinding algorithm
        for i in range(len(rooms) - 1):
            room1 = rooms[i]
            room2 = rooms[i + 1]

            # Get centers
            x1, y1 = room1.center()
            x2, y2 = room2.center()

            # Both centers should be walkable (or stairs)
            tile1 = dungeon.get_tile(x1, y1)
            tile2 = dungeon.get_tile(x2, y2)

            assert tile1.walkable or tile1.tile_type == TileType.STAIRS_UP, \
                f"Room {i} center should be walkable"
            assert tile2.walkable or tile2.tile_type == TileType.STAIRS_DOWN, \
                f"Room {i+1} center should be walkable"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
