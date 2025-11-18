"""
Comprehensive JSON Loading and Data Validation Tests

Tests cover:
- Schema validation
- Data type validation
- Required field validation
- Edge cases and error handling
- ID mismatch handling
- Malformed JSON handling
"""

import pytest
import json
import tempfile
from pathlib import Path
from src.data_loader.json_loader import JSONLoader


class TestJSONValidation:
    """Test JSON data validation and schema checking."""

    def setup_method(self):
        """Create temporary directory with test files."""
        self.temp_dir = tempfile.mkdtemp()
        self.base_path = Path(self.temp_dir)

        # Create subdirectories
        (self.base_path / "floors").mkdir()
        (self.base_path / "enemies").mkdir()
        (self.base_path / "items").mkdir()

    def test_valid_floor_data_structure(self):
        """Test that valid floor data loads correctly."""
        floor_data = {
            "floor_id": 1,
            "name": "Test Floor",
            "description": "A test floor",
            "dimensions": {
                "width": 50,
                "height": 30
            }
        }

        file_path = self.base_path / "floors" / "floor_1.json"
        with open(file_path, 'w') as f:
            json.dump(floor_data, f)

        loader = JSONLoader(base_path=str(self.base_path))
        data = loader.load_floor(1)

        assert data is not None
        assert data['floor_id'] == 1
        assert 'name' in data
        assert 'dimensions' in data
        assert isinstance(data['dimensions'], dict)

    def test_missing_required_floor_id(self):
        """Test floor data without floor_id field."""
        floor_data = {
            "name": "Test Floor",
            "description": "Missing floor_id"
        }

        file_path = self.base_path / "floors" / "floor_1.json"
        with open(file_path, 'w') as f:
            json.dump(floor_data, f)

        loader = JSONLoader(base_path=str(self.base_path))
        data = loader.load_floor(1)

        # Should still load but floor_id will be None
        assert data is not None
        assert data.get('floor_id') is None

    def test_floor_id_mismatch(self):
        """Test when floor_id in file doesn't match requested ID."""
        floor_data = {
            "floor_id": 2,  # File is floor_1.json but contains ID 2
            "name": "Mismatched Floor"
        }

        file_path = self.base_path / "floors" / "floor_1.json"
        with open(file_path, 'w') as f:
            json.dump(floor_data, f)

        loader = JSONLoader(base_path=str(self.base_path))
        data = loader.load_floor(1)

        # Should still load (just logs warning)
        assert data is not None
        assert data['floor_id'] == 2  # Contains mismatched ID

    def test_enemy_id_validation(self):
        """Test enemy ID validation."""
        enemy_data = {
            "enemy_id": "correct_id",
            "name": "Test Enemy"
        }

        file_path = self.base_path / "enemies" / "correct_id.json"
        with open(file_path, 'w') as f:
            json.dump(enemy_data, f)

        loader = JSONLoader(base_path=str(self.base_path))
        data = loader.load_enemy("correct_id")

        assert data is not None
        assert data['enemy_id'] == "correct_id"

    def test_enemy_id_mismatch(self):
        """Test when enemy_id doesn't match filename."""
        enemy_data = {
            "enemy_id": "wrong_id",  # File is test_enemy.json
            "name": "Mismatched Enemy"
        }

        file_path = self.base_path / "enemies" / "test_enemy.json"
        with open(file_path, 'w') as f:
            json.dump(enemy_data, f)

        loader = JSONLoader(base_path=str(self.base_path))
        data = loader.load_enemy("test_enemy")

        # Loads but contains wrong ID
        assert data is not None
        assert data['enemy_id'] == "wrong_id"

    def test_item_id_validation(self):
        """Test item ID validation."""
        item_data = {
            "item_id": "test_item",
            "name": "Test Item"
        }

        file_path = self.base_path / "items" / "test_item.json"
        with open(file_path, 'w') as f:
            json.dump(item_data, f)

        loader = JSONLoader(base_path=str(self.base_path))
        data = loader.load_item("test_item")

        assert data is not None
        assert data['item_id'] == "test_item"

    def test_numeric_field_types(self):
        """Test that numeric fields have correct types."""
        floor_data = {
            "floor_id": 1,
            "dimensions": {
                "width": 50,  # Should be int
                "height": 30   # Should be int
            }
        }

        file_path = self.base_path / "floors" / "floor_1.json"
        with open(file_path, 'w') as f:
            json.dump(floor_data, f)

        loader = JSONLoader(base_path=str(self.base_path))
        data = loader.load_floor(1)

        assert isinstance(data['floor_id'], int)
        assert isinstance(data['dimensions']['width'], int)
        assert isinstance(data['dimensions']['height'], int)

    def test_string_field_types(self):
        """Test that string fields have correct types."""
        enemy_data = {
            "enemy_id": "test",
            "name": "Test Enemy",
            "description": "A test enemy"
        }

        file_path = self.base_path / "enemies" / "test.json"
        with open(file_path, 'w') as f:
            json.dump(enemy_data, f)

        loader = JSONLoader(base_path=str(self.base_path))
        data = loader.load_enemy("test")

        assert isinstance(data['enemy_id'], str)
        assert isinstance(data['name'], str)
        assert isinstance(data['description'], str)

    def test_nested_data_structures(self):
        """Test loading nested JSON structures."""
        complex_data = {
            "floor_id": 1,
            "settings": {
                "difficulty": {
                    "enemy_count": 10,
                    "spawn_rate": 0.5
                },
                "features": ["hazards", "treasures"]
            }
        }

        file_path = self.base_path / "floors" / "floor_1.json"
        with open(file_path, 'w') as f:
            json.dump(complex_data, f)

        loader = JSONLoader(base_path=str(self.base_path))
        data = loader.load_floor(1)

        assert 'settings' in data
        assert 'difficulty' in data['settings']
        assert isinstance(data['settings']['features'], list)
        assert len(data['settings']['features']) == 2

    def test_empty_json_object(self):
        """Test loading empty JSON object."""
        file_path = self.base_path / "floors" / "floor_1.json"
        with open(file_path, 'w') as f:
            json.dump({}, f)

        loader = JSONLoader(base_path=str(self.base_path))
        data = loader.load_floor(1)

        assert data == {}

    def test_null_values(self):
        """Test JSON with null values."""
        data_with_nulls = {
            "floor_id": 1,
            "description": None,
            "optional_field": None
        }

        file_path = self.base_path / "floors" / "floor_1.json"
        with open(file_path, 'w') as f:
            json.dump(data_with_nulls, f)

        loader = JSONLoader(base_path=str(self.base_path))
        data = loader.load_floor(1)

        assert data['description'] is None
        assert data['optional_field'] is None

    def test_boolean_values(self):
        """Test JSON with boolean values."""
        data_with_bools = {
            "floor_id": 1,
            "is_tutorial": True,
            "has_boss": False
        }

        file_path = self.base_path / "floors" / "floor_1.json"
        with open(file_path, 'w') as f:
            json.dump(data_with_bools, f)

        loader = JSONLoader(base_path=str(self.base_path))
        data = loader.load_floor(1)

        assert data['is_tutorial'] is True
        assert data['has_boss'] is False
        assert isinstance(data['is_tutorial'], bool)

    def test_array_values(self):
        """Test JSON with array values."""
        data_with_arrays = {
            "enemy_id": "test",
            "spawn_positions": [[10, 20], [30, 40]],
            "abilities": ["attack", "defend", "heal"]
        }

        file_path = self.base_path / "enemies" / "test.json"
        with open(file_path, 'w') as f:
            json.dump(data_with_arrays, f)

        loader = JSONLoader(base_path=str(self.base_path))
        data = loader.load_enemy("test")

        assert isinstance(data['spawn_positions'], list)
        assert len(data['spawn_positions']) == 2
        assert data['abilities'] == ["attack", "defend", "heal"]


class TestJSONErrorHandling:
    """Test error handling for malformed and invalid JSON."""

    def setup_method(self):
        """Create temporary directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.base_path = Path(self.temp_dir)
        (self.base_path / "floors").mkdir()
        (self.base_path / "enemies").mkdir()
        (self.base_path / "items").mkdir()

    def test_malformed_json_syntax(self):
        """Test loading JSON with syntax errors."""
        file_path = self.base_path / "floors" / "floor_1.json"

        # Write invalid JSON (missing closing brace)
        with open(file_path, 'w') as f:
            f.write('{"floor_id": 1, "name": "Test"')

        loader = JSONLoader(base_path=str(self.base_path))
        data = loader.load_floor(1)

        # Should return None on parse error
        assert data is None

    def test_empty_file(self):
        """Test loading empty file."""
        file_path = self.base_path / "floors" / "floor_1.json"

        # Create empty file
        with open(file_path, 'w') as f:
            pass

        loader = JSONLoader(base_path=str(self.base_path))
        data = loader.load_floor(1)

        assert data is None

    def test_non_json_content(self):
        """Test loading file with non-JSON content."""
        file_path = self.base_path / "floors" / "floor_1.json"

        with open(file_path, 'w') as f:
            f.write("This is not JSON content")

        loader = JSONLoader(base_path=str(self.base_path))
        data = loader.load_floor(1)

        assert data is None

    def test_json_array_instead_of_object(self):
        """Test JSON file containing array instead of object.

        Note: Current implementation expects dict and will crash on list.
        This should be fixed in Step 38 (boundary checks) to validate data type.
        """
        file_path = self.base_path / "floors" / "floor_1.json"

        with open(file_path, 'w') as f:
            json.dump([1, 2, 3], f)

        loader = JSONLoader(base_path=str(self.base_path))

        # Current behavior: crashes with AttributeError
        # TODO: Should validate data is dict and return None if not
        with pytest.raises(AttributeError):
            data = loader.load_floor(1)

    def test_unicode_content(self):
        """Test loading JSON with unicode characters."""
        data_with_unicode = {
            "floor_id": 1,
            "name": "Test Floor 测试",
            "description": "Unicode: émojis 🎮"
        }

        file_path = self.base_path / "floors" / "floor_1.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data_with_unicode, f, ensure_ascii=False)

        loader = JSONLoader(base_path=str(self.base_path))
        data = loader.load_floor(1)

        assert data is not None
        assert "测试" in data['name']
        assert "🎮" in data['description']

    def test_very_large_numbers(self):
        """Test JSON with very large numbers."""
        data_with_large_nums = {
            "floor_id": 1,
            "max_value": 999999999999999999,
            "min_value": -999999999999999999
        }

        file_path = self.base_path / "floors" / "floor_1.json"
        with open(file_path, 'w') as f:
            json.dump(data_with_large_nums, f)

        loader = JSONLoader(base_path=str(self.base_path))
        data = loader.load_floor(1)

        assert data is not None
        assert data['max_value'] == 999999999999999999

    def test_special_characters_in_strings(self):
        """Test JSON with special characters."""
        data_with_special = {
            "enemy_id": "test",
            "special_chars": "Quotes: \"quoted\", Backslash: \\, Newline: \n, Tab: \t"
        }

        file_path = self.base_path / "enemies" / "test.json"
        with open(file_path, 'w') as f:
            json.dump(data_with_special, f)

        loader = JSONLoader(base_path=str(self.base_path))
        data = loader.load_enemy("test")

        assert data is not None
        assert '"quoted"' in data['special_chars']
        assert "\n" in data['special_chars']


class TestJSONCacheValidation:
    """Test caching behavior and validation."""

    def setup_method(self):
        """Create temporary directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.base_path = Path(self.temp_dir)
        (self.base_path / "floors").mkdir()

    def test_cache_used_on_second_load(self):
        """Test that second load uses cache."""
        floor_data = {"floor_id": 1, "name": "Test"}

        file_path = self.base_path / "floors" / "floor_1.json"
        with open(file_path, 'w') as f:
            json.dump(floor_data, f)

        loader = JSONLoader(base_path=str(self.base_path))

        # First load
        data1 = loader.load_floor(1)

        # Modify file
        floor_data['name'] = "Modified"
        with open(file_path, 'w') as f:
            json.dump(floor_data, f)

        # Second load should use cache (not see modification)
        data2 = loader.load_floor(1)

        assert data2['name'] == "Test"  # Cached value
        assert data1 is data2  # Same object reference

    def test_bypass_cache(self):
        """Test loading without cache."""
        floor_data = {"floor_id": 1, "name": "Test"}

        file_path = self.base_path / "floors" / "floor_1.json"
        with open(file_path, 'w') as f:
            json.dump(floor_data, f)

        loader = JSONLoader(base_path=str(self.base_path))

        # First load
        loader.load_floor(1)

        # Modify file
        floor_data['name'] = "Modified"
        with open(file_path, 'w') as f:
            json.dump(floor_data, f)

        # Load with cache bypass
        data = loader.load_json_file(file_path, use_cache=False)

        assert data['name'] == "Modified"  # Fresh from file

    def test_clear_cache(self):
        """Test clearing cache."""
        floor_data = {"floor_id": 1, "name": "Test"}

        file_path = self.base_path / "floors" / "floor_1.json"
        with open(file_path, 'w') as f:
            json.dump(floor_data, f)

        loader = JSONLoader(base_path=str(self.base_path))

        # Load and cache
        loader.load_floor(1)

        # Clear cache
        loader.clear_cache()

        # Modify file
        floor_data['name'] = "Modified"
        with open(file_path, 'w') as f:
            json.dump(floor_data, f)

        # Load again - should read fresh file
        data = loader.load_floor(1)

        assert data['name'] == "Modified"

    def test_cache_stats(self):
        """Test cache statistics."""
        floor_data = {"floor_id": 1, "name": "Test"}

        file_path = self.base_path / "floors" / "floor_1.json"
        with open(file_path, 'w') as f:
            json.dump(floor_data, f)

        loader = JSONLoader(base_path=str(self.base_path))

        # Initially empty
        stats = loader.get_cache_stats()
        assert stats['cached_files'] == 0

        # Load file
        loader.load_floor(1)

        # Should be cached
        stats = loader.get_cache_stats()
        assert stats['cached_files'] == 1
        assert stats['cache_size_bytes'] > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
