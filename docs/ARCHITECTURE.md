# Core Architecture Documentation

## Overview

This document explains the core architecture of the Modular Python Roguelike game, focusing on the foundational systems established in Phase 1.

## Table of Contents

1. [Architectural Patterns](#architectural-patterns)
2. [Core Systems](#core-systems)
3. [Data Flow](#data-flow)
4. [Design Decisions](#design-decisions)
5. [Extension Points](#extension-points)

---

## Architectural Patterns

### Entity-Component-System (ECS)

The game uses ECS architecture for maximum modularity and flexibility.

#### Components

**Location:** `src/components/`

Components are data containers representing specific aspects of game entities:

- **Component** (base class): Abstract base for all components
- **PositionComponent**: Spatial location (x, y coordinates)
- **RenderComponent**: Visual representation (character, color, visibility)

**Key Principles:**
- Components store data, not logic
- Components are independent and reusable
- One component type per entity (can be extended if needed)

**Example:**
```python
from src.components import PositionComponent, RenderComponent

# Create components
position = PositionComponent(x=10, y=5)
render = RenderComponent(char='@', color='white', render_order=3)
```

#### Entities

**Location:** `src/entities/entity.py`

Entities are containers for components with a unique ID:

```python
from src.entities.entity import Entity

# Create entity and add components
player = Entity(tags=['player'])
player.add_component(PositionComponent(x=10, y=5))
player.add_component(RenderComponent(char='@', color='white'))

# Query components
if player.has_component(PositionComponent):
    pos = player.get_component(PositionComponent)
    print(f"Player at ({pos.x}, {pos.y})")
```

**Key Features:**
- Auto-incrementing entity IDs
- Component management (add, remove, query)
- Tag system for categorization
- Serialization support for save/load

#### Systems

**Location:** `src/systems/`

Systems implement game logic by operating on entities with specific components:

- **ASCIIRenderer**: Renders entities with PositionComponent + RenderComponent

**Key Principles:**
- Systems process entities based on component requirements
- Systems are stateless (except for rendering state)
- Each system has a single, clear responsibility

**Example:**
```python
from src.systems.renderer import ASCIIRenderer

renderer = ASCIIRenderer(width=80, height=24)
output = renderer.render(dungeon_map, entities)
print(output)
```

### Data-Driven Design

Game content is defined in JSON files, not hardcoded.

#### JSON Configuration

**Location:** `config/`

- `config/floors/`: Dungeon floor definitions
- `config/enemies/`: Enemy type configurations
- `config/items/`: Item definitions
- `config/recipes/`: Crafting recipes (future)

**Benefits:**
- Non-programmers can create content
- Easy content iteration without code changes
- Modding support
- Version control friendly

#### JSON Loading

**Location:** `src/data_loader/`

Two main classes handle data loading:

1. **JSONLoader**: Loads and caches JSON files
2. **FloorBuilder**: Converts JSON configs to Map objects

**Example:**
```python
from src.data_loader.floor_builder import create_floor

# Load and build a floor from JSON
dungeon_map = create_floor(floor_id=1)
print(f"Built {dungeon_map.floor_name}")
```

---

## Core Systems

### Map and Tile System

**Location:** `src/models.py`

#### Tile

Immutable dataclass representing a single dungeon cell:

- **Attributes:**
  - `tile_type`: Enum (FLOOR, WALL, DOOR, etc.)
  - `walkable`: Can entities move through?
  - `blocks_sight`: Does it block vision?
  - `ascii_char`: Display character
  - `name`, `description`: Metadata

- **Factory Methods:**
  ```python
  from src.models import Tile

  floor = Tile.create_floor()
  wall = Tile.create_wall()
  stairs = Tile.create_stairs_down()
  ```

#### Map

Mutable dataclass containing a 2D grid of tiles:

- **Attributes:**
  - `width`, `height`: Map dimensions
  - `tiles`: 2D list of Tile objects
  - `floor_id`, `floor_name`, `theme`: Metadata

- **Methods:**
  ```python
  from src.models import Map

  dungeon = Map(width=40, height=25, floor_id=1)
  dungeon.initialize_empty()

  # Tile access
  tile = dungeon.get_tile(x=5, y=10)
  dungeon.set_tile(x=5, y=10, Tile.create_floor())

  # Queries
  if dungeon.is_walkable(x=5, y=10):
      player.move_to(x=5, y=10)
  ```

### Rendering System

**Location:** `src/systems/renderer.py`

The ASCIIRenderer converts game state to terminal output:

```python
renderer = ASCIIRenderer(width=80, height=24)

# Basic rendering
output = renderer.render(dungeon_map, entities)
print(output)

# With camera offset (for scrolling)
output = renderer.render(dungeon_map, entities, camera_x=10, camera_y=5)

# Direct to console
renderer.render_to_console(dungeon_map, entities)

# With decorative border
output = renderer.render_with_border(dungeon_map, entities, title="Floor 1")
```

**Rendering Process:**
1. Render base map tiles
2. Sort entities by render_order
3. Overlay visible entities
4. Convert to string output

### Data Loading System

**Location:** `src/data_loader/`

#### JSONLoader

Handles loading and caching JSON files:

```python
from src.data_loader.json_loader import JSONLoader

loader = JSONLoader()

# Load specific configs
floor_config = loader.load_floor(1)
enemy_config = loader.load_enemy("corrupted_packet")
item_config = loader.load_item("signal_boost")

# Discover available content
floors = loader.list_available_floors()
enemies = loader.list_available_enemies()
```

**Features:**
- Automatic caching for performance
- Comment field removal
- Error handling and logging
- File discovery

#### FloorBuilder

Converts JSON floor configs to Map objects:

```python
from src.data_loader.floor_builder import FloorBuilder

builder = FloorBuilder()

# Build single floor
dungeon_map = builder.build_floor(1)

# Get metadata without building full map
metadata = builder.get_floor_metadata(1)

# Build all available floors
all_floors = builder.build_all_available_floors()
```

**Phase 1 Behavior:**
- Creates simple bordered rectangular rooms
- Places stairs based on config
- Phase 2 will add procedural generation

---

## Data Flow

### Game Initialization Flow

```
1. main.py starts
2. Load configuration files (JSONLoader)
3. Build initial floor (FloorBuilder)
4. Create player entity
5. Initialize systems (Renderer, etc.)
6. Enter game loop
```

### Rendering Flow

```
1. Game state update
2. Collect all entities
3. Renderer processes:
   - Render map tiles to 2D array
   - Sort entities by render_order
   - Overlay entities on array
   - Convert to string
4. Display output to terminal
```

### Entity Creation Flow

```
1. Create Entity instance
2. Add required components:
   - PositionComponent (for location)
   - RenderComponent (for display)
   - Additional components (Health, AI, etc.)
3. Add entity to game world
4. Systems automatically process based on components
```

### Floor Loading Flow

```
JSON Config → JSONLoader → FloorBuilder → Map Object
                ↓
            Validates
            Caches
            Cleans comments
```

---

## Design Decisions

### Why ECS?

**Chosen:** Entity-Component-System
**Alternative:** Traditional inheritance hierarchy

**Rationale:**
- **Flexibility:** Mix and match components freely
- **Reusability:** Components work across entity types
- **Testability:** Test components in isolation
- **Performance:** Data-oriented design (future optimization)
- **Educational:** Demonstrates modern game architecture

**Trade-offs:**
- More complex initially than inheritance
- Requires discipline to avoid putting logic in components
- Python's dynamic nature makes some ECS benefits less pronounced

### Why Dataclasses?

**Chosen:** Python dataclasses for data models
**Alternative:** Regular classes or namedtuples

**Rationale:**
- **Conciseness:** Auto-generates __init__, __repr__, etc.
- **Readability:** Clear declaration of fields and types
- **Type Safety:** Integrates with type hints
- **Immutability:** Can freeze dataclasses (Tile)
- **Educational:** Modern Python feature (3.7+)

**Trade-offs:**
- Requires Python 3.7+
- Less flexible than hand-written classes
- Frozen dataclasses can't be modified (sometimes desired)

### Why JSON for Configuration?

**Chosen:** JSON files for game content
**Alternative:** Python files, YAML, TOML, SQLite

**Rationale:**
- **Simplicity:** Easy to parse, widely supported
- **Human-readable:** Non-programmers can edit
- **No code execution:** Safe (unlike Python configs)
- **Tooling:** Extensive JSON ecosystem
- **Educational:** Standard data format

**Trade-offs:**
- No native comment support (worked around with _comment fields)
- Verbose compared to YAML
- No type enforcement (need separate validation)

### Why ASCII Rendering?

**Chosen:** ASCII/text-based rendering
**Alternative:** Graphical UI (Pygame, tkinter)

**Rationale:**
- **Simplicity:** No external dependencies
- **Portability:** Works on any terminal
- **Focus:** Emphasizes gameplay over graphics
- **Performance:** Extremely fast
- **Educational:** Classic roguelike tradition

**Trade-offs:**
- Limited visual appeal
- No mouse input
- Terminal compatibility issues (colors, etc.)

---

## Extension Points

### Adding New Components

1. Create component class in `src/components/`
2. Inherit from `Component`
3. Implement `to_dict()` and `from_dict()` for serialization
4. Add to component registry for deserialization

**Example:**
```python
from src.components.base import Component
from typing import Dict, Any

class HealthComponent(Component):
    def __init__(self, current_hp: int, max_hp: int):
        super().__init__()
        self.current_hp = current_hp
        self.max_hp = max_hp

    def to_dict(self) -> Dict[str, Any]:
        return {
            'component_type': self.component_type,
            'current_hp': self.current_hp,
            'max_hp': self.max_hp
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HealthComponent':
        return cls(
            current_hp=data.get('current_hp', 100),
            max_hp=data.get('max_hp', 100)
        )
```

### Adding New Systems

1. Create system class in `src/systems/`
2. Define which components it requires
3. Implement processing logic
4. Integrate into game loop

**Example:**
```python
class MovementSystem:
    def process(self, entity: Entity, dx: int, dy: int, dungeon_map: Map) -> bool:
        """Process movement for entities with PositionComponent."""
        if not entity.has_component(PositionComponent):
            return False

        position = entity.get_component(PositionComponent)
        new_x = position.x + dx
        new_y = position.y + dy

        # Check if movement is valid
        if dungeon_map.is_walkable(new_x, new_y):
            position.set_position(new_x, new_y)
            return True

        return False
```

### Adding New Content

1. Create JSON file in appropriate `config/` subdirectory
2. Follow existing JSON schema
3. Use `_comment` fields for documentation
4. Test loading with JSONLoader

**Example:**
```json
{
  "_comment": "New enemy type",
  "enemy_id": "new_enemy",
  "name": "New Enemy",
  "visual": {
    "ascii_char": "N",
    "color": "green"
  },
  "components": {
    "health": {"current_hp": 20, "max_hp": 20},
    "combat": {"damage": 5, "defense": 2}
  }
}
```

### Adding New Tile Types

1. Add enum value to `TileType` in `src/models.py`
2. Create factory method on `Tile` class
3. Update renderer if special handling needed

**Example:**
```python
class TileType(Enum):
    # ... existing types ...
    LAVA = auto()  # New tile type

# In Tile class:
@staticmethod
def create_lava() -> 'Tile':
    return Tile(
        tile_type=TileType.LAVA,
        walkable=True,  # Can walk but takes damage
        blocks_sight=False,
        ascii_char='~',
        name="Lava",
        description="Molten rock - dangerous to traverse!"
    )
```

---

## Testing

### Test Structure

Tests mirror source structure:
- `tests/components/` → `src/components/`
- `tests/systems/` → `src/systems/`
- `tests/entities/` → `src/entities/`

### Running Tests

```bash
# All tests
pytest

# Specific module
pytest tests/components/test_position.py

# With coverage
pytest --cov=src

# Verbose output
pytest -v
```

### Test Statistics (Phase 1)

- **Total Tests:** 173
- **Models:** 28 tests
- **Components:** 66 tests (base + position + render)
- **Entities:** 37 tests
- **Systems:** 19 tests
- **Data Loader:** 37 tests (JSON + FloorBuilder)

---

## Next Steps (Phase 2)

Future architecture enhancements:

1. **Procedural Generation:** BSP algorithm for dynamic dungeons
2. **Game Loop:** Turn-based input and state management
3. **Combat System:** Damage calculation and resolution
4. **AI System:** Enemy behavior and pathfinding
5. **Inventory System:** Item management and equipment

See `README.md` Phase 2 section for details.

---

## References

- **README.md:** Project overview and implementation plan
- **claude.md:** AI agent development guide
- **config/floors/README.md:** Floor configuration documentation
- **Source code:** Extensive inline educational comments
