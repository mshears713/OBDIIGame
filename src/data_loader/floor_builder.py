"""
Floor Builder - Creates Map objects from JSON configuration

This module integrates the JSON loader with the Map data model, converting
floor configuration files into playable dungeon maps.

Educational Notes:
------------------
The FloorBuilder acts as a bridge between data and game objects:
    JSON Config -> FloorBuilder -> Map Object

This separation of concerns allows:
- Data to change without affecting map logic
- Map structure to evolve without breaking configs
- Easy testing of both data loading and map creation

In Phase 2, this module will handle procedural generation based on the
generation parameters in the floor config. For Phase 1, we create simple
empty maps with correct dimensions.
"""

from typing import Optional, Dict, Any
from src.models import Map, Tile
from src.data_loader.json_loader import JSONLoader
import logging

logger = logging.getLogger(__name__)


class FloorBuilder:
    """
    Builds Map objects from JSON floor configurations.

    This class handles converting JSON configuration data into actual Map
    instances that can be used in the game.

    Attributes:
        json_loader: JSONLoader instance for loading floor configs

    Educational Note:
        The builder pattern is common in game development. It separates the
        complex process of object construction from the object itself.
        This makes the construction process easier to test and modify.

    Example:
        >>> builder = FloorBuilder()
        >>> dungeon_map = builder.build_floor(floor_id=1)
        >>> print(f"Built map: {dungeon_map.floor_name}")
        Built map: CAN Bus Level
    """

    def __init__(self, json_loader: Optional[JSONLoader] = None):
        """
        Initialize the floor builder.

        Args:
            json_loader: Optional JSONLoader instance (creates new one if not provided)

        Educational Note:
            Accepting an optional JSONLoader allows dependency injection - useful
            for testing with mock loaders or sharing a loader across systems.
        """
        self.json_loader = json_loader if json_loader else JSONLoader()

    def build_floor(self, floor_id: int) -> Optional[Map]:
        """
        Build a Map from a floor configuration file.

        Args:
            floor_id: ID of the floor to build

        Returns:
            Map instance, or None if floor config not found

        Educational Note:
            This method demonstrates the integration flow:
            1. Load JSON config
            2. Validate required fields
            3. Create Map with config parameters
            4. Initialize map tiles
            5. Return ready-to-use Map object

            In Phase 2, step 4 will involve procedural generation.
            For Phase 1, we create simple empty maps.

        Example:
            >>> builder = FloorBuilder()
            >>> floor = builder.build_floor(1)
            >>> if floor:
            >>>     print(f"Floor dimensions: {floor.width}x{floor.height}")
            Floor dimensions: 40x25
        """
        # Load floor configuration
        config = self.json_loader.load_floor(floor_id)

        if config is None:
            logger.error(f"Cannot build floor {floor_id}: configuration not found")
            return None

        # Validate required fields
        if not self._validate_floor_config(config):
            logger.error(f"Invalid configuration for floor {floor_id}")
            return None

        # Extract map parameters
        width = config['dimensions']['width']
        height = config['dimensions']['height']
        floor_name = config.get('name', f"Floor {floor_id}")
        theme = config.get('theme', 'default')

        # Create Map instance
        dungeon_map = Map(
            width=width,
            height=height,
            floor_id=floor_id,
            floor_name=floor_name,
            theme=theme
        )

        # Initialize map tiles
        # Educational Note: For Phase 1, we create a simple empty map.
        # In Phase 2, this will call procedural generation based on
        # config['generation'] parameters.
        self._initialize_simple_map(dungeon_map, config)

        logger.info(f"Successfully built floor {floor_id}: {floor_name} ({width}x{height})")

        return dungeon_map

    def _validate_floor_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate that floor configuration has required fields.

        Args:
            config: Floor configuration dictionary

        Returns:
            True if valid, False otherwise

        Educational Note:
            Validation prevents crashes from malformed data. It's better to
            fail early with a clear error message than crash mysteriously later.

            The validation here is basic - in production, you might use a
            JSON schema validator for more comprehensive checks.
        """
        required_fields = ['floor_id', 'dimensions']

        # Check top-level required fields
        for field in required_fields:
            if field not in config:
                logger.error(f"Missing required field: {field}")
                return False

        # Check dimensions sub-fields
        dimensions = config.get('dimensions', {})
        if 'width' not in dimensions or 'height' not in dimensions:
            logger.error("Missing width or height in dimensions")
            return False

        # Validate dimension values
        width = dimensions['width']
        height = dimensions['height']

        if not isinstance(width, int) or not isinstance(height, int):
            logger.error("Width and height must be integers")
            return False

        if width <= 0 or height <= 0:
            logger.error("Width and height must be positive")
            return False

        # Add reasonable limits to prevent memory issues
        MAX_DIMENSION = 200
        if width > MAX_DIMENSION or height > MAX_DIMENSION:
            logger.error(f"Map dimensions too large (max {MAX_DIMENSION})")
            return False

        return True

    def _initialize_simple_map(self, dungeon_map: Map, config: Dict[str, Any]) -> None:
        """
        Initialize a simple rectangular map for Phase 1.

        Args:
            dungeon_map: Map instance to initialize
            config: Floor configuration (for future use)

        Educational Note:
            This is a placeholder implementation for Phase 1.
            It creates a simple bordered room:
            - Walls around the perimeter
            - Floor tiles in the interior
            - A stairs down tile in the center

            In Phase 2, this will be replaced with procedural generation
            using the config['generation'] parameters.
        """
        # Fill entire map with walls first
        dungeon_map.initialize_empty(Tile.create_wall())

        # Create a simple room by making interior tiles floors
        # Leave 1-tile border of walls
        for y in range(1, dungeon_map.height - 1):
            for x in range(1, dungeon_map.width - 1):
                dungeon_map.set_tile(x, y, Tile.create_floor())

        # Place stairs down in center of map (if enabled in config)
        stairs_config = config.get('stairs', {})
        stairs_down_config = stairs_config.get('stairs_down', {})

        if stairs_down_config.get('enabled', True):
            center_x = dungeon_map.width // 2
            center_y = dungeon_map.height // 2
            dungeon_map.set_tile(center_x, center_y, Tile.create_stairs_down())

        # Place stairs up near top-left if enabled
        stairs_up_config = stairs_config.get('stairs_up', {})
        if stairs_up_config.get('enabled', False):
            # Place in top-left quadrant
            up_x = dungeon_map.width // 4
            up_y = dungeon_map.height // 4
            dungeon_map.set_tile(up_x, up_y, Tile.create_stairs_up())

        logger.debug(f"Initialized simple map layout for {dungeon_map.floor_name}")

    def build_all_available_floors(self) -> Dict[int, Map]:
        """
        Build all floors that have configuration files.

        Returns:
            Dictionary mapping floor_id to Map instance

        Educational Note:
            This method is useful for:
            - Pre-loading all floors at game start (slow but simple)
            - Testing all floor configs at once
            - Content validation tools

            For large games, you'd typically load floors on-demand
            to save memory.

        Example:
            >>> builder = FloorBuilder()
            >>> all_floors = builder.build_all_available_floors()
            >>> print(f"Loaded {len(all_floors)} floors")
            Loaded 2 floors
        """
        available_floor_ids = self.json_loader.list_available_floors()
        floors = {}

        for floor_id in available_floor_ids:
            dungeon_map = self.build_floor(floor_id)
            if dungeon_map is not None:
                floors[floor_id] = dungeon_map
            else:
                logger.warning(f"Failed to build floor {floor_id}")

        logger.info(f"Built {len(floors)} floors")
        return floors

    def get_floor_metadata(self, floor_id: int) -> Optional[Dict[str, Any]]:
        """
        Get metadata about a floor without building the full Map.

        Args:
            floor_id: ID of floor to get metadata for

        Returns:
            Dictionary with floor metadata (name, description, etc.)

        Educational Note:
            Sometimes you need information about a floor without loading
            the entire map. This is useful for:
            - Displaying floor selection menus
            - Showing previews
            - Validating content

        Example:
            >>> builder = FloorBuilder()
            >>> meta = builder.get_floor_metadata(1)
            >>> print(meta['name'])
            CAN Bus Level
        """
        config = self.json_loader.load_floor(floor_id)

        if config is None:
            return None

        # Extract just the metadata we need
        return {
            'floor_id': config.get('floor_id'),
            'name': config.get('name'),
            'description': config.get('description'),
            'theme': config.get('theme'),
            'difficulty_level': config.get('difficulty', {}).get('level', 1),
            'dimensions': config.get('dimensions'),
            'metadata': config.get('metadata', {})
        }


# Module-level convenience function
def create_floor(floor_id: int) -> Optional[Map]:
    """
    Convenience function to create a floor without managing a FloorBuilder.

    Args:
        floor_id: ID of floor to create

    Returns:
        Map instance, or None if creation failed

    Educational Note:
        Like the JSON loader convenience function, this provides a simpler
        API for one-off floor creation. For repeated use, create a FloorBuilder
        instance to benefit from the shared JSONLoader cache.

    Example:
        >>> from src.data_loader.floor_builder import create_floor
        >>> floor = create_floor(1)
        >>> if floor:
        >>>     print(f"Created {floor.floor_name}")
    """
    builder = FloorBuilder()
    return builder.build_floor(floor_id)
