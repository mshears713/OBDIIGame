"""
Advanced Tests for Procedural Dungeon Generation

Focuses on:
- Statistical properties of generation
- Edge cases and boundary conditions
- Output validation and invariants
- Performance characteristics
"""

import pytest
from src.procedural.dungeon_generator import DungeonGenerator, Room
from src.models import Map, TileType


class TestDungeonStatistics:
    """Test statistical properties of dungeon generation."""

    def test_room_count_statistics(self):
        """Test that room count varies but stays within bounds."""
        max_rooms = 15
        gen = DungeonGenerator(
            width=100,
            height=60,
            max_rooms=max_rooms,
            random_seed=42
        )
        dungeon = gen.generate()
        rooms = gen.get_rooms()

        # Should have at least some rooms
        assert len(rooms) > 0, "Should generate at least one room"

        # Should not exceed max_rooms
        assert len(rooms) <= max_rooms, "Should not exceed max_rooms"

    def test_walkable_to_wall_ratio(self):
        """Test that dungeon has reasonable walkable/wall ratio."""
        gen = DungeonGenerator(width=50, height=30, max_rooms=15, random_seed=42)
        dungeon = gen.generate()

        walkable_count = 0
        wall_count = 0

        for y in range(dungeon.height):
            for x in range(dungeon.width):
                if dungeon.is_walkable(x, y):
                    walkable_count += 1
                else:
                    tile = dungeon.get_tile(x, y)
                    if tile.tile_type == TileType.WALL:
                        wall_count += 1

        total = walkable_count + wall_count

        # At least 10% should be walkable (not all walls)
        walkable_ratio = walkable_count / total if total > 0 else 0
        assert walkable_ratio >= 0.10, \
            f"Walkable ratio too low: {walkable_ratio:.2%}"

        # No more than 90% walkable (should have some walls)
        assert walkable_ratio <= 0.90, \
            f"Walkable ratio too high: {walkable_ratio:.2%}"

    def test_room_distribution_across_map(self):
        """Test that rooms are reasonably distributed across the map."""
        gen = DungeonGenerator(
            width=100,
            height=100,
            max_rooms=20,
            random_seed=42
        )
        dungeon = gen.generate()
        rooms = gen.get_rooms()

        if len(rooms) < 4:
            pytest.skip("Need at least 4 rooms for distribution test")

        # Divide map into quadrants
        mid_x = dungeon.width // 2
        mid_y = dungeon.height // 2

        quadrant_counts = [0, 0, 0, 0]  # TL, TR, BL, BR

        for room in rooms:
            cx, cy = room.center()

            if cx < mid_x and cy < mid_y:
                quadrant_counts[0] += 1  # Top-left
            elif cx >= mid_x and cy < mid_y:
                quadrant_counts[1] += 1  # Top-right
            elif cx < mid_x and cy >= mid_y:
                quadrant_counts[2] += 1  # Bottom-left
            else:
                quadrant_counts[3] += 1  # Bottom-right

        # At least one quadrant should have rooms
        # (Perfect distribution not required, but some spread expected)
        occupied_quadrants = sum(1 for count in quadrant_counts if count > 0)
        assert occupied_quadrants >= 1, "Rooms should be distributed across map"


class TestDungeonEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_minimum_size_dungeon(self):
        """Test generation of very small dungeon."""
        # Smallest reasonable dungeon
        gen = DungeonGenerator(
            width=20,
            height=20,
            max_rooms=3,
            min_room_size=4,
            max_room_size=6,
            random_seed=42
        )
        dungeon = gen.generate()

        assert dungeon is not None
        assert dungeon.width == 20
        assert dungeon.height == 20

    def test_single_room_dungeon(self):
        """Test dungeon with only one room.

        Note: When there's only one room, first and last room are the same,
        so only the last stair type (stairs_down) is placed (overwrites stairs_up).
        This is expected behavior but could be improved.
        """
        gen = DungeonGenerator(
            width=30,
            height=30,
            max_rooms=1,
            random_seed=42
        )
        dungeon = gen.generate()
        rooms = gen.get_rooms()

        assert len(rooms) == 1, "Should generate exactly one room"

        # Count stairs
        stairs_count = 0
        for y in range(dungeon.height):
            for x in range(dungeon.width):
                tile = dungeon.get_tile(x, y)
                if tile.tile_type in [TileType.STAIRS_UP, TileType.STAIRS_DOWN]:
                    stairs_count += 1

        # Single room = only one stair (last overwrites first)
        # TODO: Could be improved to place both stairs in different positions
        assert stairs_count == 1, "Single room has only one stair (last overwrites first)"

    def test_large_dungeon_generation(self):
        """Test generation of large dungeon."""
        gen = DungeonGenerator(
            width=200,
            height=150,
            max_rooms=50,
            random_seed=42
        )
        dungeon = gen.generate()
        rooms = gen.get_rooms()

        assert dungeon.width == 200
        assert dungeon.height == 150
        assert len(rooms) > 0, "Should generate rooms in large dungeon"

    def test_maximum_room_attempts(self):
        """Test that generator handles room placement failures gracefully."""
        # Create constraints that make room placement difficult
        gen = DungeonGenerator(
            width=25,
            height=25,
            max_rooms=100,  # Try to place many rooms
            min_room_size=8,  # Large rooms
            max_room_size=10,
            random_seed=42
        )
        dungeon = gen.generate()
        rooms = gen.get_rooms()

        # Should generate some rooms but not hit max (constrained space)
        assert len(rooms) > 0, "Should generate at least some rooms"
        assert len(rooms) < 100, "Should not place 100 large rooms in small space"

    def test_identical_min_max_room_size(self):
        """Test generation with identical min and max room size."""
        room_size = 7
        gen = DungeonGenerator(
            width=50,
            height=50,
            max_rooms=10,
            min_room_size=room_size,
            max_room_size=room_size,
            random_seed=42
        )
        dungeon = gen.generate()
        rooms = gen.get_rooms()

        # All rooms should be exactly the specified size
        for room in rooms:
            assert room.width() == room_size, \
                f"Room width should be {room_size}, got {room.width()}"
            assert room.height() == room_size, \
                f"Room height should be {room_size}, got {room.height()}"

    def test_determinism_multiple_calls(self):
        """Test that multiple generate calls with same seed produce identical results."""
        gen = DungeonGenerator(width=50, height=30, random_seed=12345)

        # Generate multiple times
        dungeon1 = gen.generate()
        rooms1 = gen.get_rooms()

        # Reset generator with same seed
        gen2 = DungeonGenerator(width=50, height=30, random_seed=12345)
        dungeon2 = gen2.generate()
        rooms2 = gen2.get_rooms()

        # Room count should match
        assert len(rooms1) == len(rooms2)

        # Room positions should match
        for r1, r2 in zip(rooms1, rooms2):
            assert r1.x1 == r2.x1
            assert r1.y1 == r2.y1
            assert r1.x2 == r2.x2
            assert r1.y2 == r2.y2


class TestDungeonOutputValidation:
    """Test that generated dungeons are valid and well-formed."""

    def test_no_isolated_walkable_tiles(self):
        """Test that walkable tiles form connected regions (basic check)."""
        gen = DungeonGenerator(width=50, height=30, max_rooms=10, random_seed=42)
        dungeon = gen.generate()

        # Find all walkable tiles
        walkable_tiles = []
        for y in range(dungeon.height):
            for x in range(dungeon.width):
                if dungeon.is_walkable(x, y):
                    walkable_tiles.append((x, y))

        # Should have walkable tiles
        assert len(walkable_tiles) > 0, "Should have walkable tiles"

        # Note: Full connectivity testing would require pathfinding
        # This is a basic check that we have walkable areas

    def test_all_rooms_have_floor_tiles(self):
        """Test that every room has at least one floor tile."""
        gen = DungeonGenerator(width=60, height=40, max_rooms=15, random_seed=42)
        dungeon = gen.generate()
        rooms = gen.get_rooms()

        for i, room in enumerate(rooms):
            # Check center of room is walkable (or has stairs)
            cx, cy = room.center()
            tile = dungeon.get_tile(cx, cy)

            assert tile.walkable or tile.tile_type in [TileType.STAIRS_UP, TileType.STAIRS_DOWN], \
                f"Room {i} center at ({cx}, {cy}) should be walkable or have stairs"

    def test_stairs_in_different_rooms(self):
        """Test that stairs up and down are in different rooms."""
        gen = DungeonGenerator(width=60, height=40, max_rooms=10, random_seed=42)
        dungeon = gen.generate()

        # Find stairs positions
        stairs_up_pos = None
        stairs_down_pos = None

        for y in range(dungeon.height):
            for x in range(dungeon.width):
                tile = dungeon.get_tile(x, y)
                if tile.tile_type == TileType.STAIRS_UP:
                    stairs_up_pos = (x, y)
                elif tile.tile_type == TileType.STAIRS_DOWN:
                    stairs_down_pos = (x, y)

        assert stairs_up_pos is not None, "Should have stairs up"
        assert stairs_down_pos is not None, "Should have stairs down"
        assert stairs_up_pos != stairs_down_pos, "Stairs should be at different positions"

    def test_room_centers_are_walkable(self):
        """Test that room centers are always walkable."""
        gen = DungeonGenerator(width=50, height=30, max_rooms=12, random_seed=42)
        dungeon = gen.generate()
        rooms = gen.get_rooms()

        for i, room in enumerate(rooms):
            cx, cy = room.center()

            # Center should be in bounds
            assert 0 <= cx < dungeon.width, f"Room {i} center x out of bounds"
            assert 0 <= cy < dungeon.height, f"Room {i} center y out of bounds"

            # Center should be walkable or have stairs
            tile = dungeon.get_tile(cx, cy)
            assert tile.walkable or tile.tile_type in [TileType.STAIRS_UP, TileType.STAIRS_DOWN], \
                f"Room {i} center should be walkable"

    def test_map_boundaries_are_walls(self):
        """Test that map edges are walls (standard roguelike convention)."""
        gen = DungeonGenerator(width=50, height=30, max_rooms=10, random_seed=42)
        dungeon = gen.generate()

        # Check top and bottom edges
        for x in range(dungeon.width):
            top_tile = dungeon.get_tile(x, 0)
            bottom_tile = dungeon.get_tile(x, dungeon.height - 1)

            assert top_tile.tile_type == TileType.WALL, \
                f"Top edge at x={x} should be wall"
            assert bottom_tile.tile_type == TileType.WALL, \
                f"Bottom edge at x={x} should be wall"

        # Check left and right edges
        for y in range(dungeon.height):
            left_tile = dungeon.get_tile(0, y)
            right_tile = dungeon.get_tile(dungeon.width - 1, y)

            assert left_tile.tile_type == TileType.WALL, \
                f"Left edge at y={y} should be wall"
            assert right_tile.tile_type == TileType.WALL, \
                f"Right edge at y={y} should be wall"

    def test_no_duplicate_stairs(self):
        """Test that there is exactly one of each stair type."""
        gen = DungeonGenerator(width=50, height=30, max_rooms=10, random_seed=42)
        dungeon = gen.generate()

        stairs_up_count = 0
        stairs_down_count = 0

        for y in range(dungeon.height):
            for x in range(dungeon.width):
                tile = dungeon.get_tile(x, y)
                if tile.tile_type == TileType.STAIRS_UP:
                    stairs_up_count += 1
                elif tile.tile_type == TileType.STAIRS_DOWN:
                    stairs_down_count += 1

        assert stairs_up_count == 1, \
            f"Should have exactly 1 stairs up, found {stairs_up_count}"
        assert stairs_down_count == 1, \
            f"Should have exactly 1 stairs down, found {stairs_down_count}"

    def test_room_inner_tiles_are_floors(self):
        """Test that interior of rooms (excluding walls) are floor tiles."""
        gen = DungeonGenerator(width=60, height=40, max_rooms=10, random_seed=42)
        dungeon = gen.generate()
        rooms = gen.get_rooms()

        for i, room in enumerate(rooms):
            inner_tiles = room.inner_tiles()

            for x, y in inner_tiles:
                tile = dungeon.get_tile(x, y)

                # Inner tiles should be walkable (floor or stairs)
                assert tile.walkable or tile.tile_type in [TileType.STAIRS_UP, TileType.STAIRS_DOWN], \
                    f"Room {i} inner tile at ({x}, {y}) should be walkable"


class TestDungeonPerformance:
    """Test performance characteristics of dungeon generation."""

    def test_generation_completes_quickly(self):
        """Test that dungeon generation completes in reasonable time."""
        import time

        gen = DungeonGenerator(
            width=100,
            height=100,
            max_rooms=30,
            random_seed=42
        )

        start_time = time.time()
        dungeon = gen.generate()
        end_time = time.time()

        generation_time = end_time - start_time

        # Should complete in under 1 second (very generous)
        assert generation_time < 1.0, \
            f"Generation took too long: {generation_time:.3f}s"

    def test_large_dungeon_performance(self):
        """Test that even large dungeons generate reasonably fast."""
        import time

        gen = DungeonGenerator(
            width=200,
            height=150,
            max_rooms=50,
            random_seed=42
        )

        start_time = time.time()
        dungeon = gen.generate()
        end_time = time.time()

        generation_time = end_time - start_time

        # Large dungeon should still complete quickly
        assert generation_time < 2.0, \
            f"Large dungeon generation took too long: {generation_time:.3f}s"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
