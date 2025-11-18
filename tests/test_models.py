"""
Unit Tests for Core Data Models

This module tests the Tile and Map data models to ensure correct behavior.

Educational Notes:
    - Test file names should start with 'test_' for pytest discovery
    - Test function names should start with 'test_' and be descriptive
    - Each test should focus on a single behavior or edge case
    - Use assertions to verify expected outcomes
"""

import pytest
from src.models import Tile, Map, TileType


class TestTile:
    """
    Test suite for the Tile dataclass.

    Educational Note:
        Grouping related tests in a class improves organization and allows
        sharing setup code via fixtures if needed.
    """

    def test_tile_creation_with_all_parameters(self):
        """Test creating a tile with all parameters specified."""
        tile = Tile(
            tile_type=TileType.FLOOR,
            walkable=True,
            blocks_sight=False,
            ascii_char='.',
            name="Test Floor",
            description="A test floor tile"
        )

        assert tile.tile_type == TileType.FLOOR
        assert tile.walkable is True
        assert tile.blocks_sight is False
        assert tile.ascii_char == '.'
        assert tile.name == "Test Floor"
        assert tile.description == "A test floor tile"

    def test_tile_immutability(self):
        """Test that tiles cannot be modified after creation (frozen=True)."""
        tile = Tile.create_floor()

        # Attempting to modify a frozen dataclass should raise an error
        with pytest.raises(AttributeError):
            tile.walkable = False

    def test_create_floor_factory(self):
        """Test the floor tile factory method."""
        floor = Tile.create_floor()

        assert floor.tile_type == TileType.FLOOR
        assert floor.walkable is True
        assert floor.blocks_sight is False
        assert floor.ascii_char == '.'
        assert floor.name == "Floor"

    def test_create_wall_factory(self):
        """Test the wall tile factory method."""
        wall = Tile.create_wall()

        assert wall.tile_type == TileType.WALL
        assert wall.walkable is False
        assert wall.blocks_sight is True
        assert wall.ascii_char == '#'
        assert wall.name == "Wall"

    def test_create_door_factory(self):
        """Test the door tile factory method."""
        door = Tile.create_door()

        assert door.tile_type == TileType.DOOR
        assert door.walkable is True
        assert door.blocks_sight is False
        assert door.ascii_char == '+'

    def test_create_stairs_down_factory(self):
        """Test the stairs down factory method."""
        stairs = Tile.create_stairs_down()

        assert stairs.tile_type == TileType.STAIRS_DOWN
        assert stairs.walkable is True
        assert stairs.ascii_char == '>'

    def test_create_stairs_up_factory(self):
        """Test the stairs up factory method."""
        stairs = Tile.create_stairs_up()

        assert stairs.tile_type == TileType.STAIRS_UP
        assert stairs.walkable is True
        assert stairs.ascii_char == '<'

    def test_create_hazard_factory(self):
        """Test the hazard tile factory method."""
        hazard = Tile.create_hazard()

        assert hazard.tile_type == TileType.HAZARD
        assert hazard.walkable is True  # Walkable but dangerous
        assert hazard.ascii_char == '^'

    def test_tile_equality(self):
        """Test that identical tiles are considered equal (dataclass auto-generates __eq__)."""
        floor1 = Tile.create_floor()
        floor2 = Tile.create_floor()

        # Dataclass __eq__ compares all fields
        assert floor1 == floor2

    def test_tile_inequality(self):
        """Test that different tiles are not equal."""
        floor = Tile.create_floor()
        wall = Tile.create_wall()

        assert floor != wall


class TestMap:
    """
    Test suite for the Map dataclass.

    Educational Note:
        Map tests verify both initialization and methods for accessing/modifying
        the tile grid.
    """

    def test_map_creation_with_dimensions(self):
        """Test creating a map with specified dimensions."""
        dungeon_map = Map(width=50, height=30)

        assert dungeon_map.width == 50
        assert dungeon_map.height == 30
        assert dungeon_map.floor_id == 1  # Default value
        assert dungeon_map.floor_name == "Unnamed Floor"

    def test_map_creation_with_all_parameters(self):
        """Test creating a map with all parameters."""
        dungeon_map = Map(
            width=40,
            height=25,
            floor_id=5,
            floor_name="CAN Bus Level",
            theme="can_bus"
        )

        assert dungeon_map.width == 40
        assert dungeon_map.height == 25
        assert dungeon_map.floor_id == 5
        assert dungeon_map.floor_name == "CAN Bus Level"
        assert dungeon_map.theme == "can_bus"

    def test_map_initialize_empty_with_default(self):
        """Test initializing a map with default wall tiles."""
        dungeon_map = Map(width=10, height=10)
        dungeon_map.initialize_empty()

        # Check dimensions of tiles array
        assert len(dungeon_map.tiles) == 10  # 10 rows
        assert len(dungeon_map.tiles[0]) == 10  # 10 columns

        # Check that all tiles are walls (default)
        for y in range(10):
            for x in range(10):
                tile = dungeon_map.tiles[y][x]
                assert tile.tile_type == TileType.WALL

    def test_map_initialize_empty_with_custom_tile(self):
        """Test initializing a map with custom fill tile."""
        dungeon_map = Map(width=5, height=5)
        floor_tile = Tile.create_floor()
        dungeon_map.initialize_empty(fill_tile=floor_tile)

        # Check that all tiles are floors
        for y in range(5):
            for x in range(5):
                tile = dungeon_map.tiles[y][x]
                assert tile.tile_type == TileType.FLOOR

    def test_is_in_bounds_valid_coordinates(self):
        """Test boundary checking with valid coordinates."""
        dungeon_map = Map(width=10, height=10)

        assert dungeon_map.is_in_bounds(0, 0) is True
        assert dungeon_map.is_in_bounds(9, 9) is True
        assert dungeon_map.is_in_bounds(5, 5) is True

    def test_is_in_bounds_invalid_coordinates(self):
        """Test boundary checking with invalid coordinates."""
        dungeon_map = Map(width=10, height=10)

        # Negative coordinates
        assert dungeon_map.is_in_bounds(-1, 0) is False
        assert dungeon_map.is_in_bounds(0, -1) is False

        # Coordinates beyond bounds
        assert dungeon_map.is_in_bounds(10, 0) is False
        assert dungeon_map.is_in_bounds(0, 10) is False
        assert dungeon_map.is_in_bounds(100, 100) is False

    def test_get_tile_valid_coordinates(self):
        """Test retrieving a tile with valid coordinates."""
        dungeon_map = Map(width=10, height=10)
        dungeon_map.initialize_empty()

        tile = dungeon_map.get_tile(5, 5)
        assert tile is not None
        assert tile.tile_type == TileType.WALL

    def test_get_tile_invalid_coordinates(self):
        """Test retrieving a tile with invalid coordinates returns None."""
        dungeon_map = Map(width=10, height=10)
        dungeon_map.initialize_empty()

        assert dungeon_map.get_tile(-1, 0) is None
        assert dungeon_map.get_tile(0, -1) is None
        assert dungeon_map.get_tile(10, 5) is None
        assert dungeon_map.get_tile(5, 10) is None

    def test_set_tile_valid_coordinates(self):
        """Test setting a tile with valid coordinates."""
        dungeon_map = Map(width=10, height=10)
        dungeon_map.initialize_empty()

        floor_tile = Tile.create_floor()
        result = dungeon_map.set_tile(5, 5, floor_tile)

        assert result is True
        assert dungeon_map.get_tile(5, 5) == floor_tile

    def test_set_tile_invalid_coordinates(self):
        """Test setting a tile with invalid coordinates returns False."""
        dungeon_map = Map(width=10, height=10)
        dungeon_map.initialize_empty()

        floor_tile = Tile.create_floor()

        assert dungeon_map.set_tile(-1, 0, floor_tile) is False
        assert dungeon_map.set_tile(0, -1, floor_tile) is False
        assert dungeon_map.set_tile(10, 5, floor_tile) is False

    def test_is_walkable_for_floor_tile(self):
        """Test walkability check returns True for floor tiles."""
        dungeon_map = Map(width=10, height=10)
        dungeon_map.initialize_empty(Tile.create_floor())

        assert dungeon_map.is_walkable(5, 5) is True

    def test_is_walkable_for_wall_tile(self):
        """Test walkability check returns False for wall tiles."""
        dungeon_map = Map(width=10, height=10)
        dungeon_map.initialize_empty(Tile.create_wall())

        assert dungeon_map.is_walkable(5, 5) is False

    def test_is_walkable_out_of_bounds(self):
        """Test walkability check returns False for out-of-bounds coordinates."""
        dungeon_map = Map(width=10, height=10)
        dungeon_map.initialize_empty()

        assert dungeon_map.is_walkable(-1, 0) is False
        assert dungeon_map.is_walkable(10, 5) is False

    def test_is_blocked_sight_for_wall(self):
        """Test sight blocking returns True for walls."""
        dungeon_map = Map(width=10, height=10)
        dungeon_map.initialize_empty(Tile.create_wall())

        assert dungeon_map.is_blocked_sight(5, 5) is True

    def test_is_blocked_sight_for_floor(self):
        """Test sight blocking returns False for floors."""
        dungeon_map = Map(width=10, height=10)
        dungeon_map.initialize_empty(Tile.create_floor())

        assert dungeon_map.is_blocked_sight(5, 5) is False

    def test_is_blocked_sight_out_of_bounds(self):
        """Test sight blocking returns True for out-of-bounds (can't see through void)."""
        dungeon_map = Map(width=10, height=10)
        dungeon_map.initialize_empty()

        assert dungeon_map.is_blocked_sight(-1, 0) is True
        assert dungeon_map.is_blocked_sight(10, 5) is True

    def test_get_dimensions(self):
        """Test retrieving map dimensions as a tuple."""
        dungeon_map = Map(width=50, height=30)

        width, height = dungeon_map.get_dimensions()
        assert width == 50
        assert height == 30

    def test_map_mutability(self):
        """Test that maps can be modified (not frozen)."""
        dungeon_map = Map(width=10, height=10)

        # Should be able to modify map properties
        dungeon_map.floor_name = "New Floor Name"
        assert dungeon_map.floor_name == "New Floor Name"

        # Should be able to modify tiles
        dungeon_map.initialize_empty()
        floor_tile = Tile.create_floor()
        dungeon_map.set_tile(0, 0, floor_tile)
        assert dungeon_map.get_tile(0, 0) == floor_tile
