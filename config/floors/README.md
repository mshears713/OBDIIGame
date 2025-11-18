# Floor Configuration Files

This directory contains JSON configuration files defining dungeon floors.

## Educational Purpose

These JSON files demonstrate **data-driven game design** - a key principle in modern game development where game content is separated from game code.

### Benefits of Data-Driven Design:

1. **Designer-Friendly**: Non-programmers can create content by editing JSON
2. **Rapid Iteration**: Change game balance without recompiling code
3. **Modding Support**: Players can create custom floors
4. **Version Control**: Easy to track content changes in git
5. **Testing**: Can load test floors for specific scenarios

## File Structure

Each floor JSON file contains:

### Required Fields

- `floor_id` (integer): Unique identifier for this floor
- `name` (string): Display name shown to players
- `description` (string): Flavor text describing the floor
- `theme` (string): Visual/mechanical theme identifier
- `dimensions`: Map size configuration
  - `width` (integer): Map width in tiles
  - `height` (integer): Map height in tiles

### Generation Parameters

- `generation`: Procedural generation settings
  - `algorithm` (string): Algorithm to use ("bsp", "cellular", etc.)
  - `room_count_min/max` (integer): Range of rooms to generate
  - `room_size_min/max` (integer): Range of room dimensions
  - `corridor_width` (integer): Width of connecting corridors

### Tile Configuration

- `tile_distribution`: Special tile placement
  - `hazard_tiles` (float 0-1): Percentage of floor tiles to make hazardous
  - `door_tiles` (float 0-1): Percentage of room connections that are doors

### Entity Spawning

- `enemy_spawns` (array): List of enemy types to spawn
  - `enemy_type` (string): Enemy identifier (matches enemy config file)
  - `count_min/max` (integer): Number range to spawn
  - `spawn_weight` (integer): Relative probability (higher = more common)

- `item_spawns` (array): List of items to place
  - `item_type` (string): Item identifier
  - `count_min/max` (integer): Number range to spawn
  - `spawn_weight` (integer): Relative probability

### Stair Placement

- `stairs`: Staircase configuration
  - `stairs_down`: Configuration for descending stairs
    - `enabled` (boolean): Whether to place stairs down
    - `placement` (string): "random_room", "specific_coords", "opposite_corner"
  - `stairs_up`: Configuration for ascending stairs

### Difficulty Scaling

- `difficulty`: Difficulty parameters
  - `level` (integer): Difficulty tier (1 = easy, higher = harder)
  - `enemy_health_multiplier` (float): Multiply enemy HP by this factor
  - `enemy_damage_multiplier` (float): Multiply enemy damage

### Metadata (Optional)

- `metadata`: Additional information
  - `author` (string): Content creator
  - `version` (string): Content version
  - `tags` (array): Categorization tags

## Educational Notes

Comments in JSON are not standard, but we use fields starting with `_comment` or `_educational_note` to provide inline documentation. The JSON loader will ignore these fields.

## Creating New Floors

To create a new floor:

1. Copy an existing floor JSON file
2. Change the `floor_id` to a unique number
3. Modify the `name` and `description`
4. Adjust generation parameters for desired layout
5. Configure enemy and item spawns for desired difficulty
6. Test by loading in game

## Example: Simple Test Floor

```json
{
  "floor_id": 99,
  "name": "Test Chamber",
  "description": "A simple test environment",
  "theme": "test",
  "dimensions": {"width": 20, "height": 15},
  "generation": {
    "algorithm": "bsp",
    "room_count_min": 3,
    "room_count_max": 5,
    "room_size_min": 4,
    "room_size_max": 8,
    "corridor_width": 1
  },
  "tile_distribution": {
    "hazard_tiles": 0.01,
    "door_tiles": 0.0
  },
  "enemy_spawns": [],
  "item_spawns": [],
  "stairs": {
    "stairs_down": {"enabled": false},
    "stairs_up": {"enabled": false}
  },
  "difficulty": {
    "level": 1,
    "enemy_health_multiplier": 1.0,
    "enemy_damage_multiplier": 1.0
  }
}
```

This creates an empty dungeon for testing movement, rendering, etc.

## Schema Validation

Future enhancement: Add JSON schema file (`floor_schema.json`) for automatic validation of floor configurations.

## References

- See `config/enemies/` for enemy type definitions
- See `config/items/` for item type definitions
- See `src/data_loader/` for JSON loading implementation
