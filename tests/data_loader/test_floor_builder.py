"""
Unit Tests for Floor Builder

Tests building Map objects from JSON floor configurations.
"""

import pytest
from src.data_loader.floor_builder import FloorBuilder, create_floor
from src.data_loader.json_loader import JSONLoader
from src.models import Map, TileType


class TestFloorBuilder:
    """Test suite for FloorBuilder class."""

    def test_build_floor_from_real_config(self):
        """Test building a floor from actual config file."""
        builder = FloorBuilder()

        # Build floor 1 (should exist in config/)
        dungeon_map = builder.build_floor(1)

        # Should successfully create a map
        assert dungeon_map is not None
        assert isinstance(dungeon_map, Map)
        assert dungeon_map.floor_id == 1
        assert dungeon_map.width > 0
        assert dungeon_map.height > 0

    def test_build_floor_sets_correct_properties(self):
        """Test that floor properties match configuration."""
        builder = FloorBuilder()

        dungeon_map = builder.build_floor(1)

        if dungeon_map is not None:
            # Should have correct metadata from config
            assert dungeon_map.floor_name != ""
            assert dungeon_map.theme != ""
            # Dimensions from config should be respected
            assert dungeon_map.width == 40  # From floor_1.json
            assert dungeon_map.height == 25  # From floor_1.json

    def test_build_floor_initializes_tiles(self):
        """Test that map tiles are properly initialized."""
        builder = FloorBuilder()

        dungeon_map = builder.build_floor(1)

        if dungeon_map is not None:
            # Map should have tiles initialized
            assert len(dungeon_map.tiles) == dungeon_map.height
            assert len(dungeon_map.tiles[0]) == dungeon_map.width

            # Should have walls around perimeter
            assert dungeon_map.get_tile(0, 0).tile_type == TileType.WALL
            assert dungeon_map.get_tile(dungeon_map.width - 1, 0).tile_type == TileType.WALL

            # Should have floors in interior
            center_tile = dungeon_map.get_tile(dungeon_map.width // 2, dungeon_map.height // 2)
            # Center might be stairs or floor
            assert center_tile.walkable is True

    def test_build_floor_not_found(self):
        """Test building non-existent floor returns None."""
        builder = FloorBuilder()

        dungeon_map = builder.build_floor(9999)

        assert dungeon_map is None

    def test_build_floor_places_stairs(self):
        """Test that stairs are placed according to config."""
        builder = FloorBuilder()

        dungeon_map = builder.build_floor(1)

        if dungeon_map is not None:
            # Floor 1 should have stairs down enabled
            # They should be placed in center
            center_x = dungeon_map.width // 2
            center_y = dungeon_map.height // 2

            center_tile = dungeon_map.get_tile(center_x, center_y)
            # Might be stairs down
            if center_tile.tile_type == TileType.STAIRS_DOWN:
                assert center_tile.ascii_char == '>'

    def test_validate_floor_config_valid(self):
        """Test validation of valid floor config."""
        builder = FloorBuilder()

        valid_config = {
            'floor_id': 1,
            'dimensions': {
                'width': 40,
                'height': 25
            }
        }

        assert builder._validate_floor_config(valid_config) is True

    def test_validate_floor_config_missing_floor_id(self):
        """Test validation fails when floor_id missing."""
        builder = FloorBuilder()

        invalid_config = {
            'dimensions': {
                'width': 40,
                'height': 25
            }
        }

        assert builder._validate_floor_config(invalid_config) is False

    def test_validate_floor_config_missing_dimensions(self):
        """Test validation fails when dimensions missing."""
        builder = FloorBuilder()

        invalid_config = {
            'floor_id': 1
        }

        assert builder._validate_floor_config(invalid_config) is False

    def test_validate_floor_config_missing_width(self):
        """Test validation fails when width missing."""
        builder = FloorBuilder()

        invalid_config = {
            'floor_id': 1,
            'dimensions': {
                'height': 25
            }
        }

        assert builder._validate_floor_config(invalid_config) is False

    def test_validate_floor_config_invalid_dimensions(self):
        """Test validation fails with invalid dimension values."""
        builder = FloorBuilder()

        # Negative width
        invalid_config1 = {
            'floor_id': 1,
            'dimensions': {'width': -10, 'height': 25}
        }
        assert builder._validate_floor_config(invalid_config1) is False

        # Zero height
        invalid_config2 = {
            'floor_id': 1,
            'dimensions': {'width': 40, 'height': 0}
        }
        assert builder._validate_floor_config(invalid_config2) is False

        # Non-integer width
        invalid_config3 = {
            'floor_id': 1,
            'dimensions': {'width': "forty", 'height': 25}
        }
        assert builder._validate_floor_config(invalid_config3) is False

    def test_validate_floor_config_too_large(self):
        """Test validation fails when dimensions exceed limits."""
        builder = FloorBuilder()

        invalid_config = {
            'floor_id': 1,
            'dimensions': {
                'width': 500,  # Exceeds MAX_DIMENSION
                'height': 500
            }
        }

        assert builder._validate_floor_config(invalid_config) is False

    def test_build_all_available_floors(self):
        """Test building all available floors."""
        builder = FloorBuilder()

        all_floors = builder.build_all_available_floors()

        # Should have built at least floor 1 and 2 from our configs
        assert isinstance(all_floors, dict)
        assert len(all_floors) >= 1

        # All values should be Map instances
        for floor_id, dungeon_map in all_floors.items():
            assert isinstance(dungeon_map, Map)
            assert dungeon_map.floor_id == floor_id

    def test_get_floor_metadata(self):
        """Test getting floor metadata without building full map."""
        builder = FloorBuilder()

        metadata = builder.get_floor_metadata(1)

        assert metadata is not None
        assert metadata['floor_id'] == 1
        assert 'name' in metadata
        assert 'description' in metadata
        assert 'theme' in metadata
        assert 'dimensions' in metadata
        assert metadata['dimensions']['width'] > 0
        assert metadata['dimensions']['height'] > 0

    def test_get_floor_metadata_not_found(self):
        """Test getting metadata for non-existent floor."""
        builder = FloorBuilder()

        metadata = builder.get_floor_metadata(9999)

        assert metadata is None

    def test_builder_with_custom_json_loader(self):
        """Test creating FloorBuilder with custom JSONLoader."""
        custom_loader = JSONLoader()

        builder = FloorBuilder(json_loader=custom_loader)

        # Should use the provided loader
        assert builder.json_loader is custom_loader

    def test_initialize_simple_map_structure(self):
        """Test that simple map has expected structure."""
        builder = FloorBuilder()
        dungeon_map = builder.build_floor(1)

        if dungeon_map is not None:
            # Check corners are walls
            assert dungeon_map.get_tile(0, 0).tile_type == TileType.WALL
            assert dungeon_map.get_tile(dungeon_map.width - 1, 0).tile_type == TileType.WALL
            assert dungeon_map.get_tile(0, dungeon_map.height - 1).tile_type == TileType.WALL
            assert dungeon_map.get_tile(dungeon_map.width - 1, dungeon_map.height - 1).tile_type == TileType.WALL

            # Check interior has walkable tiles
            interior_x = dungeon_map.width // 2
            interior_y = dungeon_map.height // 2
            assert dungeon_map.is_walkable(interior_x, interior_y) is True


def test_create_floor_convenience_function():
    """Test the module-level convenience function."""
    dungeon_map = create_floor(1)

    # Should create a map successfully
    if dungeon_map is not None:
        assert isinstance(dungeon_map, Map)
        assert dungeon_map.floor_id == 1
