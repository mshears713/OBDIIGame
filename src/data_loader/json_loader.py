"""
JSON Data Loader Utilities

This module provides functions for loading and parsing JSON configuration files
for floors, enemies, items, and other game content.

Educational Notes:
------------------
Data-driven design separates game content from game code. By loading content
from JSON files, we enable:
1. Non-programmers to create content
2. Easy content updates without code changes
3. Modding support
4. Content version control

This module handles:
- Safe file loading with error handling
- JSON parsing and validation
- Converting JSON data to Python objects
- Caching loaded data for performance
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging

# Set up logging for better error reporting
# Educational Note: logging is better than print() for production code
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JSONLoader:
    """
    Utility class for loading and caching JSON configuration files.

    This class provides methods to load various types of game content from JSON
    files, with built-in caching to avoid repeatedly reading the same files.

    Attributes:
        base_path: Root directory for all configuration files
        cache: Dictionary storing loaded JSON data to avoid repeated file I/O

    Educational Note:
        Caching is an important optimization technique. Reading files from disk
        is slow compared to memory access. By caching, we read each file once
        and reuse the data.

    Example:
        >>> loader = JSONLoader()
        >>> floor_data = loader.load_floor(1)
        >>> enemy_data = loader.load_enemy("corrupted_packet")
    """

    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize the JSON loader.

        Args:
            base_path: Root directory for config files (defaults to ./config)

        Educational Note:
            Using Path from pathlib is more robust than string concatenation
            for file paths. It handles different operating systems correctly.
        """
        if base_path is None:
            # Default to config/ directory relative to project root
            # __file__ is this script's location, we go up to project root
            project_root = Path(__file__).parent.parent.parent
            base_path = project_root / "config"

        self.base_path = Path(base_path)
        self.cache: Dict[str, Any] = {}

        logger.info(f"JSONLoader initialized with base path: {self.base_path}")

    def load_json_file(self, file_path: Path, use_cache: bool = True) -> Optional[Dict[str, Any]]:
        """
        Load and parse a JSON file.

        Args:
            file_path: Path to the JSON file
            use_cache: Whether to use cached data if available

        Returns:
            Parsed JSON data as dictionary, or None if loading failed

        Educational Note:
            This method demonstrates defensive programming:
            - Check if file exists before reading
            - Use try/except to handle errors gracefully
            - Log errors for debugging
            - Return None instead of crashing on errors

        Example:
            >>> data = loader.load_json_file(Path("config/floors/floor_1.json"))
            >>> if data:
            >>>     print(f"Loaded floor: {data['name']}")
        """
        # Convert to string for cache key
        cache_key = str(file_path)

        # Check cache first
        if use_cache and cache_key in self.cache:
            logger.debug(f"Loading from cache: {file_path.name}")
            return self.cache[cache_key]

        # Check if file exists
        if not file_path.exists():
            logger.error(f"JSON file not found: {file_path}")
            return None

        try:
            # Read and parse JSON file
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Clean data (remove comment fields)
            cleaned_data = self._clean_json_data(data)

            # Cache the result
            if use_cache:
                self.cache[cache_key] = cleaned_data

            logger.info(f"Successfully loaded: {file_path.name}")
            return cleaned_data

        except json.JSONDecodeError as e:
            # JSON syntax error
            logger.error(f"Invalid JSON in {file_path}: {e}")
            return None

        except IOError as e:
            # File read error
            logger.error(f"Error reading file {file_path}: {e}")
            return None

        except Exception as e:
            # Unexpected error
            logger.error(f"Unexpected error loading {file_path}: {e}")
            return None

    def _clean_json_data(self, data: Any) -> Any:
        """
        Remove comment fields from JSON data.

        Args:
            data: JSON data (dict, list, or primitive)

        Returns:
            Cleaned data with comment fields removed

        Educational Note:
            JSON doesn't natively support comments, but we use fields starting
            with "_comment" or "_educational_note" for documentation.
            This method strips those fields out before using the data.

            The function is recursive to handle nested structures.
        """
        if isinstance(data, dict):
            # Remove comment keys and recursively clean values
            return {
                key: self._clean_json_data(value)
                for key, value in data.items()
                if not key.startswith('_comment') and not key.startswith('_educational')
            }
        elif isinstance(data, list):
            # Recursively clean list items
            return [self._clean_json_data(item) for item in data]
        else:
            # Primitive types (string, number, bool, null) - return as-is
            return data

    def load_floor(self, floor_id: int) -> Optional[Dict[str, Any]]:
        """
        Load a floor configuration by ID.

        Args:
            floor_id: Unique floor identifier

        Returns:
            Floor configuration dictionary, or None if not found

        Educational Note:
            This is a convenience method that builds the file path and loads it.
            It makes the API cleaner for callers - they don't need to know
            the file naming convention.

        Example:
            >>> floor = loader.load_floor(1)
            >>> print(f"Floor name: {floor['name']}")
            Floor name: CAN Bus Level
        """
        file_path = self.base_path / "floors" / f"floor_{floor_id}.json"
        data = self.load_json_file(file_path)

        if data is None:
            logger.warning(f"Floor {floor_id} not found")
            return None

        # Validate that floor_id matches
        if data.get('floor_id') != floor_id:
            logger.warning(f"Floor ID mismatch: file says {data.get('floor_id')}, expected {floor_id}")

        return data

    def load_enemy(self, enemy_id: str) -> Optional[Dict[str, Any]]:
        """
        Load an enemy configuration by ID.

        Args:
            enemy_id: Unique enemy identifier (e.g., "corrupted_packet")

        Returns:
            Enemy configuration dictionary, or None if not found

        Example:
            >>> enemy = loader.load_enemy("corrupted_packet")
            >>> print(f"Enemy HP: {enemy['components']['health']['max_hp']}")
            Enemy HP: 10
        """
        file_path = self.base_path / "enemies" / f"{enemy_id}.json"
        data = self.load_json_file(file_path)

        if data is None:
            logger.warning(f"Enemy '{enemy_id}' not found")
            return None

        # Validate that enemy_id matches
        if data.get('enemy_id') != enemy_id:
            logger.warning(f"Enemy ID mismatch: file says {data.get('enemy_id')}, expected {enemy_id}")

        return data

    def load_item(self, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Load an item configuration by ID.

        Args:
            item_id: Unique item identifier (e.g., "signal_boost")

        Returns:
            Item configuration dictionary, or None if not found

        Example:
            >>> item = loader.load_item("signal_boost")
            >>> print(f"Item: {item['name']}")
            Item: Signal Boost
        """
        file_path = self.base_path / "items" / f"{item_id}.json"
        data = self.load_json_file(file_path)

        if data is None:
            logger.warning(f"Item '{item_id}' not found")
            return None

        # Validate that item_id matches
        if data.get('item_id') != item_id:
            logger.warning(f"Item ID mismatch: file says {data.get('item_id')}, expected {item_id}")

        return data

    def list_available_floors(self) -> List[int]:
        """
        Get list of available floor IDs.

        Returns:
            List of floor IDs that have configuration files

        Educational Note:
            This method demonstrates file system traversal and pattern matching.
            It's useful for dynamically discovering available content.

        Example:
            >>> floors = loader.list_available_floors()
            >>> print(f"Available floors: {floors}")
            Available floors: [1, 2, 3]
        """
        floors_dir = self.base_path / "floors"

        if not floors_dir.exists():
            logger.warning(f"Floors directory not found: {floors_dir}")
            return []

        floor_ids = []

        # Find all floor_*.json files
        for file_path in floors_dir.glob("floor_*.json"):
            # Extract floor number from filename
            # floor_1.json -> "1"
            try:
                floor_num_str = file_path.stem.split('_')[1]  # "floor_1" -> "1"
                floor_id = int(floor_num_str)
                floor_ids.append(floor_id)
            except (IndexError, ValueError):
                logger.warning(f"Invalid floor filename: {file_path.name}")
                continue

        return sorted(floor_ids)

    def list_available_enemies(self) -> List[str]:
        """
        Get list of available enemy IDs.

        Returns:
            List of enemy IDs that have configuration files

        Example:
            >>> enemies = loader.list_available_enemies()
            >>> print(f"Available enemies: {enemies}")
            Available enemies: ['corrupted_packet', 'signal_glitch']
        """
        enemies_dir = self.base_path / "enemies"

        if not enemies_dir.exists():
            logger.warning(f"Enemies directory not found: {enemies_dir}")
            return []

        enemy_ids = []

        # Find all .json files in enemies directory
        for file_path in enemies_dir.glob("*.json"):
            # Use filename (without .json) as enemy ID
            enemy_id = file_path.stem
            enemy_ids.append(enemy_id)

        return sorted(enemy_ids)

    def list_available_items(self) -> List[str]:
        """
        Get list of available item IDs.

        Returns:
            List of item IDs that have configuration files

        Example:
            >>> items = loader.list_available_items()
            >>> print(f"Available items: {items}")
            Available items: ['signal_boost', 'diagnostic_tool']
        """
        items_dir = self.base_path / "items"

        if not items_dir.exists():
            logger.warning(f"Items directory not found: {items_dir}")
            return []

        item_ids = []

        # Find all .json files in items directory
        for file_path in items_dir.glob("*.json"):
            item_id = file_path.stem
            item_ids.append(item_id)

        return sorted(item_ids)

    def clear_cache(self) -> None:
        """
        Clear all cached JSON data.

        Educational Note:
            During development, you might modify JSON files and want to reload
            them. Clearing the cache ensures you get fresh data.

        Example:
            >>> loader.clear_cache()  # Force reload of all JSON on next access
        """
        self.cache.clear()
        logger.info("JSON cache cleared")

    def get_cache_stats(self) -> Dict[str, int]:
        """
        Get statistics about cached data.

        Returns:
            Dictionary with cache statistics

        Educational Note:
            Monitoring cache usage helps optimize performance. If many files
            are cached but rarely used, you might want to limit cache size.

        Example:
            >>> stats = loader.get_cache_stats()
            >>> print(f"Cached files: {stats['cached_files']}")
        """
        return {
            'cached_files': len(self.cache),
            'cache_size_bytes': sum(len(str(v)) for v in self.cache.values())
        }


# Module-level convenience function
def load_floor_config(floor_id: int) -> Optional[Dict[str, Any]]:
    """
    Convenience function to load a floor without creating a JSONLoader instance.

    Args:
        floor_id: Floor ID to load

    Returns:
        Floor configuration dictionary

    Educational Note:
        This function provides a simpler API for one-off loads.
        For repeated loading, create a JSONLoader instance to benefit from caching.

    Example:
        >>> from src.data_loader.json_loader import load_floor_config
        >>> floor = load_floor_config(1)
    """
    loader = JSONLoader()
    return loader.load_floor(floor_id)
