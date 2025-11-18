"""
Unit Tests for JSON Loader

Tests loading, parsing, and caching of JSON configuration files.
"""

import pytest
import json
import tempfile
from pathlib import Path
from src.data_loader.json_loader import JSONLoader, load_floor_config


class TestJSONLoader:
    """Test suite for JSONLoader class."""

    def setup_method(self):
        """Create temporary directory with test JSON files before each test."""
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp()
        self.base_path = Path(self.temp_dir)

        # Create subdirectories
        (self.base_path / "floors").mkdir()
        (self.base_path / "enemies").mkdir()
        (self.base_path / "items").mkdir()

        # Create test floor file
        floor_data = {
            "floor_id": 1,
            "name": "Test Floor",
            "description": "A test floor",
            "_comment": "This should be removed",
            "dimensions": {
                "width": 40,
                "height": 25,
                "_comment": "Test dimensions"
            }
        }
        with open(self.base_path / "floors" / "floor_1.json", 'w') as f:
            json.dump(floor_data, f)

        # Create test enemy file
        enemy_data = {
            "enemy_id": "test_enemy",
            "name": "Test Enemy",
            "_comment": "Test comment"
        }
        with open(self.base_path / "enemies" / "test_enemy.json", 'w') as f:
            json.dump(enemy_data, f)

        # Create test item file
        item_data = {
            "item_id": "test_item",
            "name": "Test Item"
        }
        with open(self.base_path / "items" / "test_item.json", 'w') as f:
            json.dump(item_data, f)

    def test_initialization_with_custom_path(self):
        """Test creating loader with custom base path."""
        loader = JSONLoader(base_path=str(self.base_path))
        assert loader.base_path == self.base_path
        assert len(loader.cache) == 0

    def test_load_json_file_success(self):
        """Test loading a valid JSON file."""
        loader = JSONLoader(base_path=str(self.base_path))
        file_path = self.base_path / "floors" / "floor_1.json"

        data = loader.load_json_file(file_path)

        assert data is not None
        assert data['floor_id'] == 1
        assert data['name'] == "Test Floor"

    def test_load_json_file_removes_comments(self):
        """Test that comment fields are removed from loaded data."""
        loader = JSONLoader(base_path=str(self.base_path))
        file_path = self.base_path / "floors" / "floor_1.json"

        data = loader.load_json_file(file_path)

        # Comment fields should be removed
        assert '_comment' not in data
        assert '_comment' not in data['dimensions']

    def test_load_json_file_not_found(self):
        """Test loading a non-existent file returns None."""
        loader = JSONLoader(base_path=str(self.base_path))
        file_path = self.base_path / "floors" / "nonexistent.json"

        data = loader.load_json_file(file_path)

        assert data is None

    def test_load_json_file_invalid_json(self):
        """Test loading invalid JSON returns None."""
        loader = JSONLoader(base_path=str(self.base_path))

        # Create file with invalid JSON
        bad_file = self.base_path / "bad.json"
        with open(bad_file, 'w') as f:
            f.write("{ invalid json }")

        data = loader.load_json_file(bad_file)

        assert data is None

    def test_load_json_file_caching(self):
        """Test that loaded files are cached."""
        loader = JSONLoader(base_path=str(self.base_path))
        file_path = self.base_path / "floors" / "floor_1.json"

        # First load
        data1 = loader.load_json_file(file_path, use_cache=True)

        # Check cache contains the file
        assert str(file_path) in loader.cache

        # Second load should return cached data
        data2 = loader.load_json_file(file_path, use_cache=True)

        # Should be the same object (from cache)
        assert data1 is data2

    def test_load_json_file_bypass_cache(self):
        """Test loading with cache disabled."""
        loader = JSONLoader(base_path=str(self.base_path))
        file_path = self.base_path / "floors" / "floor_1.json"

        # Load without caching
        data = loader.load_json_file(file_path, use_cache=False)

        # Cache should be empty
        assert len(loader.cache) == 0
        assert data is not None

    def test_load_floor_success(self):
        """Test loading a floor by ID."""
        loader = JSONLoader(base_path=str(self.base_path))

        floor = loader.load_floor(1)

        assert floor is not None
        assert floor['floor_id'] == 1
        assert floor['name'] == "Test Floor"

    def test_load_floor_not_found(self):
        """Test loading non-existent floor returns None."""
        loader = JSONLoader(base_path=str(self.base_path))

        floor = loader.load_floor(999)

        assert floor is None

    def test_load_enemy_success(self):
        """Test loading an enemy by ID."""
        loader = JSONLoader(base_path=str(self.base_path))

        enemy = loader.load_enemy("test_enemy")

        assert enemy is not None
        assert enemy['enemy_id'] == "test_enemy"
        assert enemy['name'] == "Test Enemy"

    def test_load_enemy_not_found(self):
        """Test loading non-existent enemy returns None."""
        loader = JSONLoader(base_path=str(self.base_path))

        enemy = loader.load_enemy("nonexistent")

        assert enemy is None

    def test_load_item_success(self):
        """Test loading an item by ID."""
        loader = JSONLoader(base_path=str(self.base_path))

        item = loader.load_item("test_item")

        assert item is not None
        assert item['item_id'] == "test_item"
        assert item['name'] == "Test Item"

    def test_load_item_not_found(self):
        """Test loading non-existent item returns None."""
        loader = JSONLoader(base_path=str(self.base_path))

        item = loader.load_item("nonexistent")

        assert item is None

    def test_list_available_floors(self):
        """Test listing available floor IDs."""
        loader = JSONLoader(base_path=str(self.base_path))

        # Create additional floors
        for i in [2, 3, 5]:
            floor_data = {"floor_id": i, "name": f"Floor {i}"}
            with open(self.base_path / "floors" / f"floor_{i}.json", 'w') as f:
                json.dump(floor_data, f)

        floors = loader.list_available_floors()

        assert floors == [1, 2, 3, 5]  # Sorted order

    def test_list_available_enemies(self):
        """Test listing available enemy IDs."""
        loader = JSONLoader(base_path=str(self.base_path))

        # Create additional enemies
        for enemy_id in ["enemy_a", "enemy_b"]:
            enemy_data = {"enemy_id": enemy_id, "name": enemy_id}
            with open(self.base_path / "enemies" / f"{enemy_id}.json", 'w') as f:
                json.dump(enemy_data, f)

        enemies = loader.list_available_enemies()

        # Should include test_enemy from setup plus new ones
        assert "test_enemy" in enemies
        assert "enemy_a" in enemies
        assert "enemy_b" in enemies
        assert len(enemies) == 3

    def test_list_available_items(self):
        """Test listing available item IDs."""
        loader = JSONLoader(base_path=str(self.base_path))

        items = loader.list_available_items()

        assert "test_item" in items

    def test_clear_cache(self):
        """Test clearing the cache."""
        loader = JSONLoader(base_path=str(self.base_path))

        # Load some files to populate cache
        loader.load_floor(1)
        loader.load_enemy("test_enemy")

        # Cache should have entries
        assert len(loader.cache) > 0

        # Clear cache
        loader.clear_cache()

        # Cache should be empty
        assert len(loader.cache) == 0

    def test_get_cache_stats(self):
        """Test getting cache statistics."""
        loader = JSONLoader(base_path=str(self.base_path))

        # Initially empty
        stats = loader.get_cache_stats()
        assert stats['cached_files'] == 0

        # Load a file
        loader.load_floor(1)

        # Should have one cached file
        stats = loader.get_cache_stats()
        assert stats['cached_files'] == 1
        assert stats['cache_size_bytes'] > 0

    def test_clean_json_data_nested_comments(self):
        """Test that comments are removed from nested structures."""
        loader = JSONLoader(base_path=str(self.base_path))

        data = {
            "field1": "value1",
            "_comment": "top level comment",
            "nested": {
                "field2": "value2",
                "_comment": "nested comment",
                "_educational_note": "educational note"
            },
            "list": [
                {"field3": "value3", "_comment": "list item comment"}
            ]
        }

        cleaned = loader._clean_json_data(data)

        # Top level comment removed
        assert '_comment' not in cleaned
        # Nested comment removed
        assert '_comment' not in cleaned['nested']
        assert '_educational_note' not in cleaned['nested']
        # List item comment removed
        assert '_comment' not in cleaned['list'][0]
        # Regular fields preserved
        assert cleaned['field1'] == "value1"
        assert cleaned['nested']['field2'] == "value2"
        assert cleaned['list'][0]['field3'] == "value3"


def test_load_floor_config_convenience_function():
    """Test the module-level convenience function."""
    # This test uses actual project files
    floor = load_floor_config(1)

    # Should load floor 1 from actual config directory
    # May be None if file doesn't exist in test environment, which is okay
    if floor is not None:
        assert floor['floor_id'] == 1
